from __future__ import annotations

import datetime as dt

import numpy as np
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from rest_framework.test import APIClient

from .models import EMBEDDING_DIMENSIONS, Event, Face, Photo, Session, Tag


def vector(seed: int, scale: float = 0.1) -> list[float]:
    return np.random.default_rng(seed).normal(0.0, scale, EMBEDDING_DIMENSIONS).tolist()


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("tester", password="not-a-real-password")
        self.client.force_authenticate(self.user)
        self.event = Event.objects.create(
            name="Evento teste", slug="teste", starts_on=dt.date(2026, 11, 10), ends_on=dt.date(2026, 11, 12)
        )
        self.session = Session.objects.create(event=self.event, title="Abertura", day=dt.date(2026, 11, 10))

    def ingest_payload(self, **overrides):
        payload = {
            "event": "teste",
            "session": self.session.id,
            "image_name": "foto_001.jpg",
            "taken_at": "2026-11-10T10:00:00-03:00",
            "metadata": {"camera": {"make": "Canon"}, "iso": 800},
            "tags": ["palestra", "plateia"],
            "faces": [
                {"face_index": 0, "bbox": {"top": 1}, "embedding": vector(1)},
                {"face_index": 1, "bbox": {"top": 2}, "embedding": vector(2)},
            ],
        }
        payload.update(overrides)
        return payload


class IngestTransactionTests(ApiTestCase):
    def test_ingest_writes_photo_tags_and_faces(self):
        response = self.client.post("/api/photos/ingest/", self.ingest_payload(), format="json")

        self.assertEqual(response.status_code, 201, response.data)
        photo = Photo.objects.get(image_name="foto_001.jpg")
        self.assertEqual(photo.faces.count(), 2)
        self.assertEqual(sorted(photo.tags.values_list("name", flat=True)), ["palestra", "plateia"])
        self.assertEqual(len(response.data["faces"]), 2)

    def test_bad_embedding_rolls_back_every_table(self):
        faces = [
            {"face_index": 0, "embedding": vector(1)},
            {"face_index": 1, "embedding": [0.1, 0.2]},  # wrong dimension -> rule 4
        ]
        response = self.client.post("/api/photos/ingest/", self.ingest_payload(faces=faces), format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("embedding", response.data["detail"])
        self.assertFalse(Photo.objects.exists())
        self.assertFalse(Face.objects.exists())
        self.assertFalse(Tag.objects.exists())  # tags created earlier in the transaction are gone too

    def test_duplicate_face_index_rolls_back(self):
        faces = [{"face_index": 0, "embedding": vector(1)}, {"face_index": 0, "embedding": vector(2)}]
        response = self.client.post("/api/photos/ingest/", self.ingest_payload(faces=faces), format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Photo.objects.exists())

    def test_photo_outside_event_dates_is_rejected(self):
        response = self.client.post(
            "/api/photos/ingest/", self.ingest_payload(taken_at="2026-12-25T10:00:00-03:00"), format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Photo.objects.exists())

    def test_session_from_other_event_is_rejected(self):
        other = Event.objects.create(
            name="Outro", slug="outro", starts_on=dt.date(2026, 11, 10), ends_on=dt.date(2026, 11, 12)
        )
        response = self.client.post("/api/photos/ingest/", self.ingest_payload(event=other.slug), format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Photo.objects.exists())


class JsonbFilterTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        Photo.objects.create(event=self.event, image_name="a.jpg", metadata={"camera": {"make": "Canon"}, "iso": 800})
        Photo.objects.create(event=self.event, image_name="b.jpg", metadata={"camera": {"make": "Nikon"}, "iso": 1600})

    def test_filter_by_nested_json_key(self):
        response = self.client.get("/api/photos/?metadata__camera__make=Nikon")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([p["image_name"] for p in response.data["results"]], ["b.jpg"])

    def test_filter_matches_typed_json_value(self):
        response = self.client.get("/api/photos/?metadata__iso=800")

        self.assertEqual([p["image_name"] for p in response.data["results"]], ["a.jpg"])

    def test_metadata_has_gin_index(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT indexdef FROM pg_indexes WHERE tablename = 'gallery_photo' AND indexname = 'photo_metadata_gin'"
            )
            row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertIn("gin", row[0].lower())


class CrudAndSearchTests(ApiTestCase):
    def test_event_crud(self):
        created = self.client.post(
            "/api/events/",
            {"name": "Novo", "slug": "novo", "starts_on": "2026-12-01", "ends_on": "2026-12-02"},
            format="json",
        )
        self.assertEqual(created.status_code, 201, created.data)
        updated = self.client.patch("/api/events/novo/", {"venue": "Auditório"}, format="json")
        self.assertEqual(updated.data["venue"], "Auditório")
        self.assertEqual(self.client.delete("/api/events/novo/").status_code, 204)

    def test_event_end_before_start_is_rejected(self):
        response = self.client.post(
            "/api/events/",
            {"name": "Errado", "slug": "errado", "starts_on": "2026-12-02", "ends_on": "2026-12-01"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_anonymous_users_cannot_write(self):
        anonymous = APIClient()
        self.assertEqual(anonymous.get("/api/events/").status_code, 200)
        self.assertEqual(anonymous.post("/api/events/", {}, format="json").status_code, 403)

    def test_vector_search_returns_closest_photo_first(self):
        self.client.post("/api/photos/ingest/", self.ingest_payload(), format="json")
        query = (np.array(vector(2)) + 0.01).tolist()

        response = APIClient().post("/api/search/", {"embedding": query}, format="json")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["results"][0]["image_name"], "foto_001.jpg")
        self.assertEqual(response.data["results"][0]["best_face_index"], 1)

    def test_seed_demo_is_idempotent(self):
        call_command("seed_demo", photos=6, verbosity=0)
        call_command("seed_demo", photos=6, verbosity=0)

        self.assertEqual(Photo.objects.filter(event__slug="demo-2026").count(), 6)
        self.assertTrue(Face.objects.filter(photo__event__slug="demo-2026").exists())
