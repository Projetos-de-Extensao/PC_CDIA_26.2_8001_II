"""Index a folder of event photos: detect faces, compute embeddings and save
Photo + Face rows, without a pre-built .pkl.

For each image not indexed yet:
  1. read EXIF (taken_at, camera, lens, ISO...) into Photo.metadata;
  2. downscale to --max-side for detection (much faster on 24 MP photos)
     and map the face boxes back to the original size;
  3. save the photo and its faces in one transaction;
  4. optionally write a 320x180 JPEG thumbnail (same as make_thumb.py).

Photos without any detected face are skipped (they can never be a search
result). Running the command again only processes new files.

Example (inside the web container):
    python manage.py index_photos --event evento-2 --name "Nome do evento" \\
        --starts-on 2026-05-01 --ends-on 2026-05-03 --prefix evento2/ \\
        --images-dir /photos/dataset/evento2 --thumbnails-dir /photos/thumb-out/evento2
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from gallery.management.commands.import_pkl import _normalized_prefix, read_exif
from gallery.models import Event, Face, Photo

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
THUMBNAIL_SIZE = (320, 180)


class Command(BaseCommand):
    help = "Detect faces in a folder of photos and save them under one event."

    def add_arguments(self, parser):
        parser.add_argument("--event", required=True, help="Slug of the event (created if --name is given).")
        parser.add_argument("--name", help="Create the event with this name if it does not exist.")
        parser.add_argument("--starts-on", help="Event start date (YYYY-MM-DD), used when creating.")
        parser.add_argument("--ends-on", help="Event end date (YYYY-MM-DD), used when creating.")
        parser.add_argument("--venue", default="", help="Event venue, used when creating.")
        parser.add_argument("--prefix", default="", help="Folder of this event's photos, e.g. evento2/.")
        parser.add_argument("--images-dir", required=True, help="Folder with the original photos.")
        parser.add_argument("--thumbnails-dir", help="Write thumbnails here (must be writable).")
        parser.add_argument("--max-side", type=int, default=2000, help="Longest side used for detection.")
        parser.add_argument("--limit", type=int, default=0, help="Process at most N new photos (0 = all).")

    def _get_event(self, options) -> Event:
        event = Event.objects.filter(slug=options["event"]).first()
        if event is not None:
            return event
        if not (options["name"] and options["starts_on"] and options["ends_on"]):
            raise CommandError(
                f"Event not found: {options['event']}. Pass --name, --starts-on and --ends-on to create it."
            )
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
        import face_engine as fe  # heavy (dlib); only loaded by this command
        from PIL import Image, ImageOps

        images_dir = Path(options["images_dir"])
        if not images_dir.is_dir():
            raise CommandError(f"--images-dir is not a folder: {images_dir}")
        thumbs_dir = Path(options["thumbnails_dir"]) if options["thumbnails_dir"] else None
        if thumbs_dir is not None:
            thumbs_dir.mkdir(parents=True, exist_ok=True)

        event = self._get_event(options)
        prefix = _normalized_prefix(options["prefix"])
        done = set(Photo.objects.filter(image_name__startswith=prefix).values_list("image_name", flat=True))

        files = sorted(
            p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        )
        pending = [p for p in files if f"{prefix}{p.name}" not in done]
        if options["limit"]:
            pending = pending[: options["limit"]]
        self.stdout.write(f"{len(files)} image(s) in folder, {len(pending)} to index.")

        photos_saved = faces_saved = skipped = 0
        for count, path in enumerate(pending, start=1):
            try:
                with Image.open(path) as opened:
                    image = ImageOps.exif_transpose(opened).convert("RGB")
            except Exception as exc:  # unreadable file
                self.stderr.write(self.style.WARNING(f"Skipping {path.name}: {exc}"))
                skipped += 1
                continue

            scale = min(1.0, options["max_side"] / max(image.size))
            small = image if scale == 1.0 else image.resize(
                (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
            )
            pixels = np.asarray(small)
            boxes = fe.detect_faces(pixels)
            embeddings = fe.compute_embeddings(pixels, boxes) if boxes else []

            if thumbs_dir is not None:
                thumb = image.copy()
                thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                thumb.save(thumbs_dir / f"{path.stem}.jpg", "JPEG", quality=90)

            if not embeddings:
                skipped += 1
            else:
                taken_at, metadata = read_exif(path)
                with transaction.atomic():
                    photo = Photo.objects.create(
                        event=event,
                        image_name=f"{prefix}{path.name}",
                        taken_at=taken_at,
                        metadata=metadata,
                    )
                    Face.objects.bulk_create(
                        Face(
                            photo=photo,
                            face_index=index,
                            bbox={k: int(round(v / scale)) for k, v in box.items()},
                            embedding=embedding.tolist(),
                        )
                        for index, (box, embedding) in enumerate(zip(boxes, embeddings))
                    )
                photos_saved += 1
                faces_saved += len(embeddings)

            if count % 25 == 0 or count == len(pending):
                self.stdout.write(f"  {count}/{len(pending)}: {photos_saved} photo(s), {faces_saved} face(s)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Event {event.slug}: {photos_saved} photo(s) with {faces_saved} face(s) saved, "
                f"{skipped} without faces or unreadable."
            )
        )
