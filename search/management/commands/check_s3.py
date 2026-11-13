"""Diagnose why event photos do not show up from S3.

Checks, in order: settings, AWS credentials (instance role), and for one
photo of each published event, whether its thumbnail and original exist at
the keys the app builds. Prints the fix for the first problem it finds.

Usage (on the EC2):  docker compose exec web python manage.py check_s3
"""

from __future__ import annotations

from django.core.management.base import BaseCommand

from gallery.models import Event, Photo
from search.runtime import local_photos_enabled
from search.s3 import bucket_name, image_prefix, object_key, s3_client, thumbnail_prefix


class Command(BaseCommand):
    help = "Check the S3 settings, credentials and photo keys used by the selfie page."

    def ok(self, text):
        self.stdout.write(self.style.SUCCESS(f"OK    {text}"))

    def fail(self, text, fix):
        self.stdout.write(self.style.ERROR(f"FAIL  {text}"))
        self.stdout.write(f"      fix: {fix}")

    def handle(self, *args, **options):
        import os

        bucket = bucket_name()
        region = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION") or "(not set, using us-east-1)"
        self.stdout.write(f"S3_BUCKET={bucket or '(empty)'}  region={region}")
        self.stdout.write(f"S3_IMAGE_PREFIX={image_prefix()}  S3_THUMBNAIL_PREFIX={thumbnail_prefix()}")
        self.stdout.write(f"LOCAL_PHOTOS_ENABLED -> {local_photos_enabled()}")

        if not bucket:
            self.fail(
                "S3_BUCKET is empty inside the container",
                "add S3_BUCKET=<bucket> and AWS_DEFAULT_REGION=<region> to .env, then `docker compose up -d` "
                "(restart is not enough: .env is read when the container is created)",
            )
            return

        import boto3

        credentials = boto3.Session().get_credentials()
        if credentials is None:
            self.fail(
                "no AWS credentials found",
                "EC2 > instance > Actions > Security > Modify IAM role (LabInstanceProfile on Learner Lab), and "
                "Actions > Instance settings > Modify instance metadata options > hop limit = 2",
            )
            return
        self.ok(f"credentials from: {credentials.method}")

        client = s3_client()
        try:
            location = client.get_bucket_location(Bucket=bucket).get("LocationConstraint") or "us-east-1"
            self.ok(f"bucket {bucket} found (region {location})")
            if os.getenv("AWS_DEFAULT_REGION") and os.getenv("AWS_DEFAULT_REGION") != location:
                self.fail(
                    f"AWS_DEFAULT_REGION={os.getenv('AWS_DEFAULT_REGION')} but the bucket is in {location}",
                    f"set AWS_DEFAULT_REGION={location} in .env, then `docker compose up -d`",
                )
        except Exception as exc:  # AccessDenied on GetBucketLocation is common and not fatal
            self.stdout.write(f"NOTE  could not read the bucket region ({type(exc).__name__}); continuing")

        events = Event.objects.filter(published=True)
        if not events:
            self.fail("no published events in the database", "restore the events dump (see AP2_GUIDE.md section 12)")
            return

        problems = 0
        for event in events:
            photo = Photo.objects.filter(event=event, faces__isnull=False).order_by("image_name").first()
            if photo is None:
                self.fail(f"{event.slug}: no photos with faces", "import or restore this event's faces")
                problems += 1
                continue
            for label, key in (
                ("thumbnail", object_key(photo.image_name, thumbnail=True)),
                ("original", object_key(photo.image_name)),
            ):
                try:
                    size = client.head_object(Bucket=bucket, Key=key)["ContentLength"]
                    self.ok(f"{event.slug} {label}: s3://{bucket}/{key} ({size:,} bytes)")
                except Exception as exc:
                    code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
                    if code in {"404", "NoSuchKey", "NotFound"}:
                        fix = (
                            f"upload the file so the key is exactly {key} "
                            "(use Upload > Add files inside the folder, not Add folder)"
                        )
                    elif code in {"403", "AccessDenied", "Forbidden"}:
                        fix = "the instance role needs s3:GetObject on arn:aws:s3:::%s/*" % bucket
                    else:
                        fix = str(exc)
                    if label == "original":
                        fix += "  (originals only matter for the 'alta resolução' link)"
                    self.fail(f"{event.slug} {label}: s3://{bucket}/{key} -> {code}", fix)
                    problems += 1

        if problems == 0:
            self.stdout.write(self.style.SUCCESS("All checks passed: previews should load from S3."))
