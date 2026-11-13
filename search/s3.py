from __future__ import annotations

import logging
import os
from functools import lru_cache

from .runtime import safe_relative_path, thumbnail_name

logger = logging.getLogger(__name__)


def _normalized_prefix(prefix: str) -> str:
    cleaned = (prefix or "").strip().strip("/")
    return f"{cleaned}/" if cleaned else ""


def bucket_name() -> str:
    return os.getenv("S3_BUCKET", "").strip()


def image_prefix() -> str:
    return os.getenv("S3_IMAGE_PREFIX", "dataset/").strip()


def thumbnail_prefix() -> str:
    return os.getenv("S3_THUMBNAIL_PREFIX", "thumb/").strip()


def object_key(image_name: str, *, thumbnail: bool = False) -> str | None:
    """S3 key of a photo: <S3_IMAGE_PREFIX><event folder>/<file>, or the
    thumbnail under <S3_THUMBNAIL_PREFIX> with a .jpg suffix."""
    relative = safe_relative_path(image_name)
    if relative is None:
        return None
    if thumbnail:
        return f"{_normalized_prefix(thumbnail_prefix())}{thumbnail_name(relative)}"
    return f"{_normalized_prefix(image_prefix())}{relative}"


@lru_cache(maxsize=1)
def s3_client():
    import boto3
    from botocore.config import Config

    # Regional, virtual-hosted URLs with SigV4 work for buckets in any region.
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION") or "us-east-1",
        config=Config(signature_version="s3v4", s3={"addressing_style": "virtual"}),
    )


def _presign(key: str | None, expires_seconds: int) -> str | None:
    bucket = bucket_name()
    if not bucket or key is None:
        return None
    try:
        return s3_client().generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_seconds
        )
    except Exception:  # missing credentials or bad configuration: show no preview instead of a 500
        logger.exception("Could not sign S3 URL for %s (run: python manage.py check_s3)", key)
        return None


def build_presigned_get_url(image_name: str, expires_seconds: int = 300) -> str | None:
    return _presign(object_key(image_name), expires_seconds)


def build_presigned_thumbnail_url(image_name: str, expires_seconds: int = 300) -> str | None:
    return _presign(object_key(image_name, thumbnail=True), expires_seconds)
