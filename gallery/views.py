from __future__ import annotations

import json
import re

from django.db.models import Count, Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Event, Face, Photo, Photographer, Session, Tag
from .serializers import (
    EventSerializer,
    FaceSerializer,
    PhotoIngestSerializer,
    PhotographerSerializer,
    PhotoSerializer,
    SessionSerializer,
    SimilaritySearchSerializer,
    TagSerializer,
)
from .services import BusinessRuleError, find_similar_photos, ingest_photo

METADATA_PARAM = re.compile(r"^metadata__([A-Za-z0-9_]+(?:__[A-Za-z0-9_]+)*)$")


def metadata_filter(params) -> Q:
    """Translate ?metadata__a__b=v into a JSONB containment test (metadata @> {"a": {"b": v}}).

    Containment (@>) is the operator the GIN index on Photo.metadata serves.
    Values are matched both as text and, when they parse as JSON, as typed
    values, so ?metadata__iso=800 matches {"iso": 800} and {"iso": "800"}.
    """
    query = Q()
    for param, raw_value in params.items():
        match = METADATA_PARAM.match(param)
        if not match:
            continue
        keys = match.group(1).split("__")

        def nest(value):
            for key in reversed(keys):
                value = {key: value}
            return value

        condition = Q(metadata__contains=nest(raw_value))
        try:
            typed = json.loads(raw_value)
        except ValueError:
            typed = raw_value
        if typed != raw_value:
            condition |= Q(metadata__contains=nest(typed))
        query &= condition
    return query


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Event.objects.annotate(photo_count=Count("photos", distinct=True))
            .prefetch_related("sessions")
            .order_by("-starts_on", "slug")
        )


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer

    def get_queryset(self):
        queryset = Session.objects.select_related("event")
        if event := self.request.query_params.get("event"):
            queryset = queryset.filter(event__slug=event)
        return queryset


class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """CRUD for photos.

    Filters: ?event=<slug>, ?session=<id>, ?tag=<name>, ?has_metadata=<key>,
    and any JSONB key with ?metadata__<key>[__<subkey>]=<value>.
    """

    serializer_class = PhotoSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = (
            Photo.objects.select_related("event", "session", "photographer")
            .prefetch_related("tags", "faces")
            .filter(metadata_filter(params))
        )
        if event := params.get("event"):
            queryset = queryset.filter(event__slug=event)
        if session := params.get("session"):
            queryset = queryset.filter(session_id=session)
        if tag := params.get("tag"):
            queryset = queryset.filter(tags__name=tag)
        if key := params.get("has_metadata"):
            queryset = queryset.filter(metadata__has_key=key)
        return queryset.distinct()

    @action(detail=False, methods=["post"], url_path="ingest")
    def ingest(self, request):
        """Create a photo, its tags and its faces in one transaction (rolls back on any rule violation)."""
        serializer = PhotoIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            photo = ingest_photo(**serializer.validated_data)
        except BusinessRuleError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        photo = self.get_queryset().get(pk=photo.pk)
        return Response(PhotoSerializer(photo).data, status=status.HTTP_201_CREATED)


class FaceViewSet(viewsets.ModelViewSet):
    serializer_class = FaceSerializer

    def get_queryset(self):
        queryset = Face.objects.select_related("photo")
        if photo := self.request.query_params.get("photo"):
            queryset = queryset.filter(photo_id=photo)
        return queryset


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def similarity_search(request):
    """Vector search (pgvector): send a 128-value 'embedding' or an 'image' with a face."""
    serializer = SimilaritySearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    embedding = data.get("embedding")
    if embedding is None:
        import face_engine as fe  # heavy (dlib); only loaded for image queries

        query_img = fe.load_image_rgb(data["image"].read())
        query_embedding, _ = fe.get_query_embedding(query_img)
        if query_embedding is None:
            raise ValidationError({"image": "Nenhum rosto detectado na imagem."})
        embedding = query_embedding.tolist()

    results = find_similar_photos(
        embedding, threshold=data.get("threshold"), event=data.get("event"), limit=data["limit"]
    )
    return Response({"count": len(results), "results": results})
