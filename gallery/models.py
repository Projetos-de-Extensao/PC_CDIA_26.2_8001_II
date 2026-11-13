"""PhotoMatch data model.

Relational (ACID) core:   Event -> Session, Event -> Photo, Photographer -> Photo,
                          Photo <-> Tag (many-to-many), Photo -> Face.
Document (JSONB):         Photo.metadata (camera, lens, EXIF, free attributes),
                          with a GIN index for containment queries.
Vector (pgvector):        Face.embedding, 128-d face descriptor used for
                          similarity search (L2 distance).
"""

from __future__ import annotations

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from pgvector.django import VectorField

EMBEDDING_DIMENSIONS = 128


class Event(models.Model):
    name = models.CharField("nome", max_length=200)
    slug = models.SlugField(unique=True)
    venue = models.CharField("local", max_length=200, blank=True)
    starts_on = models.DateField("início")
    ends_on = models.DateField("fim")
    published = models.BooleanField(
        "publicado", default=True, help_text="Aparece na página de busca por selfie."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-starts_on"]
        verbose_name = "evento"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ends_on__gte=models.F("starts_on")),
                name="event_ends_after_start",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField("título", max_length=200)
    day = models.DateField("dia")
    room = models.CharField("sala", max_length=100, blank=True)

    class Meta:
        ordering = ["day", "title"]
        verbose_name = "sessão"
        verbose_name_plural = "sessões"

    def __str__(self) -> str:
        return f"{self.event.slug} · {self.title}"


class Photographer(models.Model):
    name = models.CharField("nome", max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "fotógrafo"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.SlugField("nome", max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="photos")
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, blank=True, related_name="photos"
    )
    photographer = models.ForeignKey(
        Photographer, on_delete=models.SET_NULL, null=True, blank=True, related_name="photos"
    )
    image_name = models.CharField("arquivo", max_length=512, unique=True)
    taken_at = models.DateTimeField("capturada em", null=True, blank=True)
    metadata = models.JSONField("metadados", default=dict, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="photos")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-taken_at", "image_name"]
        verbose_name = "foto"
        indexes = [
            GinIndex(fields=["metadata"], name="photo_metadata_gin"),
        ]

    def __str__(self) -> str:
        return self.image_name


class Face(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="faces")
    face_index = models.PositiveSmallIntegerField()
    bbox = models.JSONField(default=dict)
    embedding = VectorField(dimensions=EMBEDDING_DIMENSIONS)

    class Meta:
        ordering = ["photo_id", "face_index"]
        verbose_name = "rosto"
        constraints = [
            models.UniqueConstraint(fields=["photo", "face_index"], name="uniq_photo_face_index"),
        ]

    def __str__(self) -> str:
        return f"{self.photo.image_name}#{self.face_index}"
