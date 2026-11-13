"""Business operations that touch more than one table."""

from __future__ import annotations

import os
from collections import defaultdict
from typing import Any

from django.db import IntegrityError, transaction
from django.utils import timezone
from pgvector.django import L2Distance

from .models import EMBEDDING_DIMENSIONS, Event, Face, Photo, Photographer, Session, Tag

MAX_FACES_PER_PHOTO = 50


class BusinessRuleError(Exception):
    """Raised inside a transaction to abort it; the API maps it to HTTP 400."""


def ingest_photo(
    *,
    event: Event,
    image_name: str,
    faces: list[dict[str, Any]],
    session: Session | None = None,
    photographer: Photographer | None = None,
    taken_at=None,
    metadata: dict | None = None,
    tags: list[str] | None = None,
) -> Photo:
    """Register a photo with its tags and detected faces as one atomic unit.

    Writes to Photo, Tag, Photo.tags (join table) and Face. If any rule below
    fails, nothing is kept: the photo, newly created tags and faces are all
    rolled back.

    Rules:
      1. The session, when given, belongs to the same event.
      2. taken_at, when given, falls within the event dates.
      3. The photo has between 1 and MAX_FACES_PER_PHOTO faces (a photo with
         no detected face is useless for PhotoMatch search).
      4. Each embedding has exactly EMBEDDING_DIMENSIONS values.
      5. face_index values are unique within the photo.
    """
    with transaction.atomic():
        photo = Photo.objects.create(
            event=event,
            session=session,
            photographer=photographer,
            image_name=image_name,
            taken_at=taken_at,
            metadata=metadata or {},
        )

        tag_objects = [Tag.objects.get_or_create(name=name.strip().lower())[0] for name in tags or []]
        photo.tags.set(tag_objects)

        if session is not None and session.event_id != event.id:
            raise BusinessRuleError("A sessão informada não pertence a este evento.")

        if taken_at is not None:
            local_day = timezone.localtime(taken_at).date() if timezone.is_aware(taken_at) else taken_at.date()
            if not (event.starts_on <= local_day <= event.ends_on):
                raise BusinessRuleError("A data da foto está fora do período do evento.")

        if not faces:
            raise BusinessRuleError("A foto precisa ter pelo menos um rosto detectado.")
        if len(faces) > MAX_FACES_PER_PHOTO:
            raise BusinessRuleError(f"A foto tem mais de {MAX_FACES_PER_PHOTO} rostos.")

        face_objects = []
        for face in faces:
            embedding = list(face["embedding"])
            if len(embedding) != EMBEDDING_DIMENSIONS:
                raise BusinessRuleError(
                    f"Cada embedding precisa ter {EMBEDDING_DIMENSIONS} valores (recebido: {len(embedding)})."
                )
            face_objects.append(
                Face(
                    photo=photo,
                    face_index=face["face_index"],
                    bbox=face.get("bbox") or {},
                    embedding=embedding,
                )
            )

        try:
            # Savepoint so the IntegrityError can be turned into a rule error
            # while the outer atomic block still rolls everything back.
            with transaction.atomic():
                Face.objects.bulk_create(face_objects)
        except IntegrityError as exc:
            raise BusinessRuleError("face_index repetido na mesma foto.") from exc

    return photo


def get_match_threshold() -> float:
    return float(os.getenv("MATCH_THRESHOLD", "0.60"))


def find_similar_photos(
    query_embedding,
    *,
    threshold: float | None = None,
    event: Event | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Vector search: photos containing a face close to the query (L2 distance)."""
    threshold = get_match_threshold() if threshold is None else threshold
    vector = list(query_embedding)

    faces = Face.objects.annotate(distance=L2Distance("embedding", vector)).filter(distance__lte=threshold)
    if event is not None:
        faces = faces.filter(photo__event=event)
    rows = faces.order_by("distance").values("photo_id", "photo__image_name", "face_index", "distance")[
        : limit * 5
    ]

    best: dict[int, dict[str, Any]] = {}
    counts: dict[int, int] = defaultdict(int)
    for row in rows:
        photo_id = row["photo_id"]
        counts[photo_id] += 1
        if photo_id not in best:
            best[photo_id] = {
                "photo_id": photo_id,
                "image_name": row["photo__image_name"],
                "best_distance": round(float(row["distance"]), 4),
                "best_face_index": row["face_index"],
            }

    results = sorted(best.values(), key=lambda item: item["best_distance"])[:limit]
    for item in results:
        item["matching_faces"] = counts[item["photo_id"]]
    return results
