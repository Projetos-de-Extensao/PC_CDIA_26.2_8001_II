from __future__ import annotations

from rest_framework import serializers

from .models import EMBEDDING_DIMENSIONS, Event, Face, Photo, Photographer, Session, Tag


class EmbeddingField(serializers.ListField):
    child = serializers.FloatField()

    def to_representation(self, data):
        return [round(float(value), 6) for value in data]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "event", "title", "day", "room"]

    def validate(self, attrs):
        event = attrs.get("event") or getattr(self.instance, "event", None)
        day = attrs.get("day") or getattr(self.instance, "day", None)
        if event and day and not (event.starts_on <= day <= event.ends_on):
            raise serializers.ValidationError({"day": "O dia da sessão precisa estar dentro do evento."})
        return attrs


class EventSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    photo_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "name", "slug", "venue", "starts_on", "ends_on", "published", "sessions", "photo_count", "created_at",
        ]

    def validate(self, attrs):
        starts_on = attrs.get("starts_on") or getattr(self.instance, "starts_on", None)
        ends_on = attrs.get("ends_on") or getattr(self.instance, "ends_on", None)
        if starts_on and ends_on and ends_on < starts_on:
            raise serializers.ValidationError({"ends_on": "A data de fim é anterior à de início."})
        return attrs


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ["id", "name", "email"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class FaceSerializer(serializers.ModelSerializer):
    embedding = EmbeddingField(min_length=EMBEDDING_DIMENSIONS, max_length=EMBEDDING_DIMENSIONS)

    class Meta:
        model = Face
        fields = ["id", "photo", "face_index", "bbox", "embedding"]


class FaceSummarySerializer(serializers.ModelSerializer):
    """Nested in photos; leaves out the 128-value embedding."""

    class Meta:
        model = Face
        fields = ["id", "face_index", "bbox"]


class PhotoSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Tag.objects.all(), required=False)
    faces = FaceSummarySerializer(many=True, read_only=True)
    event_detail = serializers.StringRelatedField(source="event", read_only=True)
    photographer_detail = PhotographerSerializer(source="photographer", read_only=True)

    class Meta:
        model = Photo
        fields = [
            "id",
            "event",
            "event_detail",
            "session",
            "photographer",
            "photographer_detail",
            "image_name",
            "taken_at",
            "metadata",
            "tags",
            "faces",
            "created_at",
        ]

    def validate_metadata(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("metadata precisa ser um objeto JSON.")
        return value


class FaceInputSerializer(serializers.Serializer):
    face_index = serializers.IntegerField(min_value=0)
    bbox = serializers.JSONField(required=False)
    # Length is a business rule checked inside the ingest transaction.
    embedding = serializers.ListField(child=serializers.FloatField())


class PhotoIngestSerializer(serializers.Serializer):
    event = serializers.SlugRelatedField(slug_field="slug", queryset=Event.objects.all())
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all(), required=False, allow_null=True)
    photographer = serializers.PrimaryKeyRelatedField(
        queryset=Photographer.objects.all(), required=False, allow_null=True
    )
    image_name = serializers.CharField(max_length=512)
    taken_at = serializers.DateTimeField(required=False, allow_null=True)
    metadata = serializers.DictField(required=False)
    tags = serializers.ListField(child=serializers.SlugField(max_length=50), required=False)
    faces = FaceInputSerializer(many=True)

    def validate_image_name(self, value):
        if Photo.objects.filter(image_name=value).exists():
            raise serializers.ValidationError("Já existe uma foto com este arquivo.")
        return value


class SimilaritySearchSerializer(serializers.Serializer):
    embedding = serializers.ListField(
        child=serializers.FloatField(), min_length=EMBEDDING_DIMENSIONS, max_length=EMBEDDING_DIMENSIONS,
        required=False,
    )
    image = serializers.ImageField(required=False)
    threshold = serializers.FloatField(required=False, min_value=0.0, max_value=2.0)
    event = serializers.SlugRelatedField(slug_field="slug", queryset=Event.objects.all(), required=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=200, default=50)

    def validate(self, attrs):
        if not attrs.get("embedding") and not attrs.get("image"):
            raise serializers.ValidationError("Envie 'embedding' (128 valores) ou 'image'.")
        return attrs
