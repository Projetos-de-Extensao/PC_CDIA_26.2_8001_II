from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

from django.conf import settings


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def is_running_on_aws() -> bool:
    return any(
        os.getenv(name)
        for name in (
            "AWS_EXECUTION_ENV",
            "ELASTIC_BEANSTALK_ENVIRONMENT_NAME",
            "ECS_CONTAINER_METADATA_URI",
            "ECS_CONTAINER_METADATA_URI_V4",
        )
    )


def local_photo_images_dir() -> Path:
    configured = os.getenv("LOCAL_PHOTO_IMAGES_DIR") or os.getenv("DATASET_IMAGES_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path(settings.BASE_DIR) / "dataset"


def local_photo_thumbnails_dir() -> Path:
    configured = os.getenv("LOCAL_PHOTO_THUMBNAILS_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path(settings.BASE_DIR) / "thumb"


def local_photos_enabled() -> bool:
    """Serve photos from local folders (development) instead of S3."""
    return (
        _env_flag("LOCAL_PHOTOS_ENABLED", True)
        and not is_running_on_aws()
        and local_photo_images_dir().is_dir()
    )


def safe_relative_path(image_name: str) -> str | None:
    """Normalise a stored photo path like 'sbrt2025/THF_0193.jpg'.

    Returns None for anything that could escape the photo folder
    (absolute paths, '..', backslashes, empty names).
    """
    if not image_name or "\\" in image_name:
        return None
    path = PurePosixPath(image_name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path.as_posix()


def thumbnail_name(image_name: str) -> str:
    """Thumbnails keep the photo's folder and are always JPEG (see make_thumb.py)."""
    return str(PurePosixPath(image_name).with_suffix(".jpg"))
