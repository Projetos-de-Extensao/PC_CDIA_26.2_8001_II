from __future__ import annotations

import datetime as dt
import pickle
import tempfile
from pathlib import Path

import numpy as np
from django.core.management import call_command
from django.test import TestCase, override_settings

from gallery.models import EMBEDDING_DIMENSIONS, Event, Face, Photo
from gallery.services import find_similar_photos

from .runtime import safe_relative_path, thumbnail_name


def vector(seed: int) -> list[float]:
    return np.random.default_rng(seed).normal(0.0, 0.1, EMBEDDING_DIMENSIONS).tolist()


def make_event(slug: str, published: bool = True, with_face_seed: int | None = None) -> Event:
    event = Event.objects.create(
        name=slug.upper(), slug=slug, starts_on=dt.date(2025, 9, 29), ends_on=dt.date(2025, 10, 2), published=published
    )
    if with_face_seed is not None:
        photo = Photo.objects.create(event=event, image_name=f"{slug}/foto.jpg")
        Face.objects.create(photo=photo, face_index=0, embedding=vector(with_face_seed))
    return event


@override_settings(ALLOWED_HOSTS=["testserver"])
class EventPickerTests(TestCase):
    def test_page_lists_only_published_events_with_faces(self):
        make_event("sbrt-2025", with_face_seed=1)
        make_event("outro-evento", with_face_seed=2)
        make_event("rascunho", published=False, with_face_seed=3)
        make_event("sem-fotos")

        response = self.client.get("/")

        slugs = [event.slug for event in response.context["events"]]
        self.assertEqual(sorted(slugs), ["outro-evento", "sbrt-2025"])
        self.assertIsNone(response.context["selected_event"])  # two options: the user must choose
        self.assertContains(response, 'value="sbrt-2025"')
        self.assertNotContains(response, 'value="rascunho"')

    def test_event_in_query_string_is_preselected(self):
        make_event("sbrt-2025", with_face_seed=1)
        make_event("outro-evento", with_face_seed=2)

        response = self.client.get("/?evento=outro-evento")

        self.assertEqual(response.context["selected_event"].slug, "outro-evento")

    def test_post_without_event_is_rejected_when_there_is_a_choice(self):
        make_event("sbrt-2025", with_face_seed=1)
        make_event("outro-evento", with_face_seed=2)

        response = self.client.post("/", {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.context["error_state"], "errorEvent")


class EventScopedSearchTests(TestCase):
    def test_search_only_returns_photos_of_the_chosen_event(self):
        first = make_event("sbrt-2025", with_face_seed=7)
        second = make_event("outro-evento", with_face_seed=7)  # same face in both events

        results = find_similar_photos(vector(7), event=second)

        self.assertEqual([r["image_name"] for r in results], ["outro-evento/foto.jpg"])
        self.assertEqual(len(find_similar_photos(vector(7), event=first)), 1)
        self.assertEqual(len(find_similar_photos(vector(7))), 2)


class PhotoPathTests(TestCase):
    def test_safe_relative_path(self):
        self.assertEqual(safe_relative_path("sbrt2025/THF_0193.jpg"), "sbrt2025/THF_0193.jpg")
        self.assertEqual(safe_relative_path("a//b.jpg"), "a/b.jpg")  # harmless, normalised
        self.assertEqual(safe_relative_path("./a.jpg"), "a.jpg")
        for unsafe in ["../etc/passwd", "/etc/passwd", "a/../../b.jpg", "a\\b.jpg", ""]:
            self.assertIsNone(safe_relative_path(unsafe), unsafe)

    def test_thumbnail_keeps_folder_and_uses_jpg(self):
        self.assertEqual(thumbnail_name("evento2/IMG_1.png"), "evento2/IMG_1.jpg")

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_local_photo_view_blocks_traversal(self):
        with tempfile.TemporaryDirectory() as root:
            photos = Path(root) / "dataset"
            (photos / "sbrt2025").mkdir(parents=True)
            (photos / "sbrt2025" / "a.jpg").write_bytes(b"jpeg")
            (Path(root) / "secret.txt").write_text("secret")
            with self.settings(), self.modify_env(LOCAL_PHOTO_IMAGES_DIR=str(photos)):
                self.assertEqual(self.client.get("/photos/sbrt2025/a.jpg").status_code, 200)
                self.assertEqual(self.client.get("/photos/../secret.txt").status_code, 404)
                self.assertEqual(self.client.get("/photos/sbrt2025/..%2F..%2Fsecret.txt").status_code, 404)

    def modify_env(self, **values):
        from unittest import mock

        return mock.patch.dict("os.environ", values)


class ImportPklTests(TestCase):
    def test_import_creates_event_and_prefixes_photo_paths(self):
        rows = [
            {"image_name": "IMG_1.jpg", "face_index": 0, "bbox": {"top": 1}, "embedding": np.array(vector(1))},
            {"image_name": "IMG_1.jpg", "face_index": 1, "bbox": {"top": 2}, "embedding": np.array(vector(2))},
            {"image_name": "IMG_2.jpg", "face_index": 0, "bbox": {}, "embedding": np.array(vector(3))},
            {"image_name": "bad.jpg", "face_index": 0, "embedding": np.zeros(5)},  # wrong size: skipped
        ]
        with tempfile.TemporaryDirectory() as root:
            shard = Path(root) / "faces.pkl"
            shard.write_bytes(pickle.dumps(rows))
            call_command(
                "import_pkl", event="evento-2", name="Evento 2", starts_on="2026-05-01", ends_on="2026-05-03",
                prefix="evento2", glob_pattern=str(shard), stdout=open(Path(root) / "out.txt", "w"),
            )

        event = Event.objects.get(slug="evento-2")
        self.assertTrue(event.published)
        self.assertEqual(
            sorted(event.photos.values_list("image_name", flat=True)), ["evento2/IMG_1.jpg", "evento2/IMG_2.jpg"]
        )
        self.assertEqual(Face.objects.filter(photo__event=event).count(), 3)
