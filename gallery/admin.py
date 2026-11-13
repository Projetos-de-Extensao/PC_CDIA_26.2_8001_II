from django.contrib import admin

from .models import Event, Face, Photo, Photographer, Session, Tag


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0


class FaceInline(admin.TabularInline):
    model = Face
    extra = 0
    fields = ["face_index", "bbox"]
    readonly_fields = ["face_index", "bbox"]
    can_delete = False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "venue", "starts_on", "ends_on", "published"]
    list_editable = ["published"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name", "venue"]
    inlines = [SessionInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["title", "event", "day", "room"]
    list_filter = ["event", "day"]


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]
    search_fields = ["name", "email"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ["image_name", "event", "session", "photographer", "taken_at", "face_count"]
    list_filter = ["event", "tags"]
    search_fields = ["image_name"]
    filter_horizontal = ["tags"]
    inlines = [FaceInline]

    @admin.display(description="rostos")
    def face_count(self, obj):
        return obj.faces.count()


@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ["__str__", "photo", "face_index"]
    raw_id_fields = ["photo"]
    exclude = ["embedding"]
