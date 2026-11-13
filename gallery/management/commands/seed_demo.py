"""Load clearly-labelled demo data so the API, admin and search can be shown
without the real event photos (which stay in S3 / out of Git).

Embeddings are synthetic: three "demo people" are random 128-d vectors and
each face in a photo is one of them plus small noise, so a similarity search
with a person's vector returns that person's photos.
"""

from __future__ import annotations

import datetime as dt

import numpy as np
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from gallery.models import EMBEDDING_DIMENSIONS, Event, Photo, Photographer, Session
from gallery.services import ingest_photo

DEMO_SLUG = "demo-2026"
CAMERAS = [
    {"make": "Canon", "model": "EOS R6"},
    {"make": "Nikon", "model": "Z6 II"},
    {"make": "Sony", "model": "A7 IV"},
]


def demo_people(rng: np.random.Generator, count: int = 3) -> np.ndarray:
    # Real face_recognition descriptors have values around ±0.2; spreading the
    # demo people apart keeps them farther than the 0.6 match threshold.
    return rng.normal(0.0, 0.1, size=(count, EMBEDDING_DIMENSIONS))


class Command(BaseCommand):
    help = "Create a demo event with sessions, photographers, tagged photos and synthetic faces."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete the demo event first.")
        parser.add_argument("--photos", type=int, default=24)

    def handle(self, *args, **options):
        if options["reset"]:
            Event.objects.filter(slug=DEMO_SLUG).delete()
        if Event.objects.filter(slug=DEMO_SLUG).exists():
            self.stdout.write("Demo data already present (use --reset to recreate).")
            return

        rng = np.random.default_rng(2026)
        people = demo_people(rng)
        start = dt.date(2026, 11, 10)

        with transaction.atomic():
            event = Event.objects.create(
                name="Evento de demonstração 2026",
                slug=DEMO_SLUG,
                venue="[Local de demonstração]",
                starts_on=start,
                ends_on=start + dt.timedelta(days=2),
                # Synthetic data: available in the API, hidden from the selfie page.
                published=False,
            )
            sessions = [
                Session.objects.create(event=event, title=title, day=start + dt.timedelta(days=offset), room=room)
                for offset, title, room in [
                    (0, "Abertura", "Auditório"),
                    (1, "Sessão técnica: visão computacional", "Sala 2"),
                    (2, "Encerramento e premiação", "Auditório"),
                ]
            ]
            photographers = [
                Photographer.objects.get_or_create(email=f"fotografo{i}@demo.invalid", defaults={"name": f"Fotógrafo demo {i}"})[0]
                for i in (1, 2)
            ]

            tag_pool = ["palestra", "plateia", "coffee-break", "premiacao", "networking"]
            for index in range(options["photos"]):
                session = sessions[index % len(sessions)]
                taken_at = timezone.make_aware(
                    dt.datetime.combine(session.day, dt.time(9 + index % 9, (index * 7) % 60))
                )
                person_ids = rng.choice(len(people), size=int(rng.integers(1, 4)), replace=False)
                faces = [
                    {
                        "face_index": face_index,
                        "bbox": {"top": 40 * face_index, "left": 60, "bottom": 40 * face_index + 120, "right": 180},
                        "embedding": (people[pid] + rng.normal(0.0, 0.02, EMBEDDING_DIMENSIONS)).tolist(),
                    }
                    for face_index, pid in enumerate(person_ids)
                ]
                camera = CAMERAS[index % len(CAMERAS)]
                ingest_photo(
                    event=event,
                    session=session,
                    photographer=photographers[index % len(photographers)],
                    image_name=f"demo/{session.day:%Y%m%d}_{index:03d}.jpg",
                    taken_at=taken_at,
                    metadata={
                        "camera": camera,
                        "iso": int(rng.choice([400, 800, 1600, 3200])),
                        "lens_mm": int(rng.choice([24, 35, 50, 85])),
                        "orientation": "landscape" if index % 4 else "portrait",
                        "demo_people": [int(pid) for pid in person_ids],
                    },
                    tags=list(rng.choice(tag_pool, size=2, replace=False)),
                    faces=faces,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo event '{DEMO_SLUG}' created with {Photo.objects.filter(event=event).count()} photos."
            )
        )
