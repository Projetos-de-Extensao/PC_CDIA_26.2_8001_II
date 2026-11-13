from __future__ import annotations

import mimetypes
from pathlib import Path

from django.db.models import Count
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render

from gallery.models import Event

from .forms import QueryUploadForm
from .runtime import (
    is_running_on_aws,
    local_photo_images_dir,
    local_photo_thumbnails_dir,
    safe_relative_path,
)
from .services import get_match_threshold, search_event_photos


def published_events():
    """Events shown on the page: published and with at least one indexed face."""
    return (
        Event.objects.filter(published=True)
        .annotate(
            photo_total=Count("photos", distinct=True),
            face_total=Count("photos__faces", distinct=True),
        )
        .filter(face_total__gt=0)
        .order_by("-starts_on", "name")
    )


def _selected_event(events, slug: str | None):
    if slug:
        return next((event for event in events if event.slug == slug), None)
    return events[0] if len(events) == 1 else None


def home_view(request):
    events = list(published_events())
    requested_slug = request.POST.get("event") if request.method == "POST" else request.GET.get("evento")
    selected = _selected_event(events, requested_slug)

    context: dict = {
        "form": QueryUploadForm(),
        "events": events,
        "selected_event": selected,
        "results": [],
        "has_query": False,
        "no_match_message": "",
        "error_message": "",
        "error_state": "",
    }

    if request.method != "POST":
        return render(request, "search/home.html", context)

    context["has_query"] = True
    if selected is None:
        context["error_state"] = "errorEvent"
        context["error_message"] = "Escolha um evento antes de buscar."
        return render(request, "search/home.html", context, status=400)

    form = QueryUploadForm(request.POST, request.FILES)
    context["form"] = form
    if not form.is_valid():
        context["error_state"] = "errorSelfie"
        context["error_message"] = form.errors.get("__all__", ["Envie uma selfie."])[0]
        return render(request, "search/home.html", context, status=400)

    uploaded = form.cleaned_data.get("selfie_capture") or form.cleaned_data.get("selfie_file")
    try:
        import face_engine as fe
    except (ModuleNotFoundError, SystemExit):
        context["error_state"] = "error"
        context["error_message"] = "A busca facial não está disponível neste servidor."
        return render(request, "search/home.html", context, status=500)

    query_img = fe.load_image_rgb(uploaded.read())
    query_embedding, _query_bboxes = fe.get_query_embedding(query_img)
    if query_embedding is None:
        context["error_state"] = "errorNoFace"
        context["error_message"] = "Nenhum rosto encontrado na foto enviada. Tente outra foto."
        return render(request, "search/home.html", context, status=422)

    results = search_event_photos(query_embedding.tolist(), selected, threshold=get_match_threshold())
    if not results:
        context["no_match_message"] = "Nenhuma foto correspondente encontrada."
    context["results"] = results
    return render(request, "search/home.html", context)


def health_view(_request):
    return JsonResponse({"status": "ok"}, status=200)


def _local_photo_response(image_name: str, photo_dir: Path):
    if is_running_on_aws():
        raise Http404("Not found")

    relative = safe_relative_path(image_name)
    if relative is None:
        raise Http404("Not found")

    base = photo_dir.resolve()
    photo_path = (base / relative).resolve()
    if base not in photo_path.parents or not photo_path.is_file():
        raise Http404("Photo not found")

    content_type, _encoding = mimetypes.guess_type(str(photo_path))
    return FileResponse(photo_path.open("rb"), content_type=content_type or "application/octet-stream")


def local_photo_preview_view(_request, image_name: str):
    return _local_photo_response(image_name, local_photo_images_dir())


def local_photo_thumbnail_view(_request, image_name: str):
    return _local_photo_response(image_name, local_photo_thumbnails_dir())
