from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("gallery.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("search.urls")),
]
