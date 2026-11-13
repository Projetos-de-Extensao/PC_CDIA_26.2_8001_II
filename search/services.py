"""Selfie search for the web page. The vector search itself lives in
gallery.services.find_similar_photos (pgvector); this module only resolves
the photo URLs and the confidence label for each match."""

from __future__ import annotations

from django.urls import reverse

from gallery.models import Event
from gallery.services import find_similar_photos, get_match_threshold

from .runtime import local_photos_enabled, safe_relative_path, thumbnail_name
from .s3 import build_presigned_get_url, build_presigned_thumbnail_url

__all__ = ["get_match_threshold", "search_event_photos", "confidence_tier"]


def confidence_tier(distance: float) -> str:
    if distance < 0.45:
        return "high"
    if distance < 0.55:
        return "likely"
    return "possible"


def _photo_urls(image_name: str) -> tuple[str | None, str | None]:
    thumbnail_url = build_presigned_thumbnail_url(image_name)
    original_url = build_presigned_get_url(image_name)
    if thumbnail_url and original_url:
        return thumbnail_url, original_url

    relative = safe_relative_path(image_name)
    if relative is None or not local_photos_enabled():
        return None, None
    return (
        reverse("local_photo_thumbnail", kwargs={"image_name": thumbnail_name(relative)}),
        reverse("local_photo_preview", kwargs={"image_name": relative}),
    )


def search_event_photos(query_embedding, event: Event, threshold: float | None = None) -> list[dict]:
    """Photos of one event that contain a face close to the selfie."""
    matches = find_similar_photos(query_embedding, threshold=threshold, event=event, limit=200)
    results = []
    for match in matches:
        preview_url, original_url = _photo_urls(match["image_name"])
        results.append(
            {
                "image_name": match["image_name"],
                "best_distance": match["best_distance"],
                "confidence_tier": confidence_tier(match["best_distance"]),
                "matching_faces": match["matching_faces"],
                "preview_url": preview_url,
                "original_url": original_url,
            }
        )
    return results
