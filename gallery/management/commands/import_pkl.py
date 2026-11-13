"""Import face embeddings produced by face_engine.build_database (PKL shards).

Each shard is a list of {"image_name", "face_index", "bbox", "embedding", "day"?}.
Photos are created under one event; faces are attached to their photo.

Each event keeps its photos in its own folder (``--prefix``), so file names
from different events never collide. The stored ``Photo.image_name`` is
``<prefix><file name>`` and is used as the relative path both in S3
(``S3_IMAGE_PREFIX`` / ``S3_THUMBNAIL_PREFIX``) and in the local photo folders.

With ``--images-dir`` the command also reads each photo's EXIF data and fills
``taken_at`` and the JSONB ``metadata`` (camera, lens, ISO, focal length...).

Example:
    python manage.py import_pkl --event sbrt-2025 --name "SBrT 2025" \\
        --starts-on 2025-09-29 --ends-on 2025-10-02 \\
        --prefix sbrt2025/ --glob /photos/sbrt2025.pkl --images-dir /photos/dataset/sbrt2025
"""

from __future__ import annotations

import datetime as dt
import glob
import os
import pickle
from pathlib import Path

import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from gallery.models import EMBEDDING_DIMENSIONS, Event, Face, Photo

EXIF_IFD = 0x8769
EXIF_TAGS = {
    0x010F: "make",
    0x0110: "model",
    0x9003: "date_time_original",
    0x0132: "date_time",
    0x8827: "iso",
    0x920A: "focal_length_mm",
    0x829D: "f_number",
    0x829A: "exposure_s",
    0xA434: "lens",
}


def _default_glob_pattern() -> str:
    configured = os.getenv("PKL_SHARD_GLOB", "").strip()
    if configured:
        return configured
    return str(Path(os.getenv("MODELS_DIR", "/tmp/models")) / "*.pkl")


def _normalized_prefix(prefix: str) -> str:
    cleaned = (prefix or "").strip().strip("/")
    return f"{cleaned}/" if cleaned else ""


def _number(value):
    try:
        number = float(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return int(number) if number.is_integer() else round(number, 4)


def read_exif(path: Path) -> tuple[dt.datetime | None, dict]:
    """Return (taken_at, metadata) from a photo's EXIF header. Never raises."""
    try:
        from PIL import Image

        with Image.open(path) as image:
            width, height = image.size
            exif = image.getexif()
            values = {**dict(exif), **dict(exif.get_ifd(EXIF_IFD))}
    except Exception:  # unreadable or missing file: import the faces anyway
        return None, {}

    raw = {name: values.get(tag) for tag, name in EXIF_TAGS.items() if values.get(tag) not in (None, "")}
    metadata: dict = {"width": width, "height": height}
    camera = {k: str(raw[k]).strip() for k in ("make", "model") if k in raw}
    if camera:
        metadata["camera"] = camera
    if "lens" in raw:
        metadata["lens"] = str(raw["lens"]).strip()
    for key in ("iso", "focal_length_mm", "f_number", "exposure_s"):
        value = raw.get(key)
        if isinstance(value, tuple):  # some cameras store ISO as a tuple
            value = value[0] if value else None
        if _number(value) is not None:
            metadata[key] = _number(value)

    taken_at = None
    stamp = raw.get("date_time_original") or raw.get("date_time")
    if stamp:
        try:
            taken_at = timezone.make_aware(dt.datetime.strptime(str(stamp), "%Y:%m:%d %H:%M:%S"))
        except ValueError:
            taken_at = None
    return taken_at, metadata


class Command(BaseCommand):
    help = "Import face embeddings from PKL shards into the Photo and Face rows of one event."

    def add_arguments(self, parser):
        parser.add_argument("--event", required=True, help="Slug of the event (created if --name is given).")
        parser.add_argument("--name", help="Create the event with this name if it does not exist.")
        parser.add_argument("--starts-on", help="Event start date (YYYY-MM-DD), used when creating.")
        parser.add_argument("--ends-on", help="Event end date (YYYY-MM-DD), used when creating.")
        parser.add_argument("--venue", default="", help="Event venue, used when creating.")
        parser.add_argument("--prefix", default="", help="Folder of this event's photos, e.g. sbrt2025/.")
        parser.add_argument("--images-dir", help="Folder with the original photos, to read EXIF data.")
        parser.add_argument("--glob", dest="glob_pattern", default=_default_glob_pattern())
        parser.add_argument("--batch-size", type=int, default=1000)

    def _get_event(self, options) -> Event:
        event = Event.objects.filter(slug=options["event"]).first()
        if event is not None:
            return event
        if not options["name"]:
            raise CommandError(f"Event not found: {options['event']} (pass --name to create it)")
        if not (options["starts_on"] and options["ends_on"]):
            raise CommandError("--starts-on and --ends-on are required to create the event")
        event = Event.objects.create(
            slug=options["event"],
            name=options["name"],
            venue=options["venue"],
            starts_on=dt.date.fromisoformat(options["starts_on"]),
            ends_on=dt.date.fromisoformat(options["ends_on"]),
        )
        self.stdout.write(f"Created event {event.slug}")
        return event

    def handle(self, *args, **options):
        event = self._get_event(options)
        prefix = _normalized_prefix(options["prefix"])
        images_dir = Path(options["images_dir"]) if options["images_dir"] else None
        if images_dir is not None and not images_dir.is_dir():
            raise CommandError(f"--images-dir is not a folder: {images_dir}")

        shard_paths = sorted(glob.glob(options["glob_pattern"]))
        if not shard_paths:
            raise CommandError(f"No PKL shards found for pattern: {options['glob_pattern']}")

        total_faces = 0
        total_photos = 0
        for shard in shard_paths:
            with open(shard, "rb") as fp:
                records = pickle.load(fp)
            if not isinstance(records, list):
                self.stderr.write(self.style.WARNING(f"Skipping non-list shard: {shard}"))
                continue

            with transaction.atomic():
                photos: dict[str, Photo] = {}
                faces: list[Face] = []
                for row in records:
                    if not isinstance(row, dict):
                        continue
                    file_name = Path(str(row.get("image_name", "")).strip()).name
                    embedding = np.asarray(row.get("embedding", []), dtype=np.float32)
                    if not file_name or embedding.shape != (EMBEDDING_DIMENSIONS,):
                        continue

                    photo = photos.get(file_name)
                    if photo is None:
                        taken_at, metadata = (None, {})
                        if images_dir is not None:
                            taken_at, metadata = read_exif(images_dir / file_name)
                        photo, created = Photo.objects.get_or_create(
                            image_name=f"{prefix}{file_name}",
                            defaults={"event": event, "taken_at": taken_at, "metadata": metadata},
                        )
                        total_photos += int(created)
                        photos[file_name] = photo

                    faces.append(
                        Face(
                            photo=photo,
                            face_index=int(row.get("face_index", 0)),
                            bbox={k: int(v) for k, v in (row.get("bbox") or {}).items()},
                            embedding=embedding.tolist(),
                        )
                    )
                created_faces = Face.objects.bulk_create(
                    faces, batch_size=options["batch_size"], ignore_conflicts=True
                )
            total_faces += len(created_faces)
            self.stdout.write(f"{Path(shard).name}: {len(photos)} photo(s), {len(created_faces)} face(s)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Event {event.slug}: {total_photos} new photo(s), {total_faces} face(s) inserted."
            )
        )
