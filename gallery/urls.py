from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("events", views.EventViewSet, basename="event")
router.register("sessions", views.SessionViewSet, basename="session")
router.register("photographers", views.PhotographerViewSet, basename="photographer")
router.register("tags", views.TagViewSet, basename="tag")
router.register("photos", views.PhotoViewSet, basename="photo")
router.register("faces", views.FaceViewSet, basename="face")

urlpatterns = [
    path("search/", views.similarity_search, name="similarity-search"),
    path("", include(router.urls)),
]
