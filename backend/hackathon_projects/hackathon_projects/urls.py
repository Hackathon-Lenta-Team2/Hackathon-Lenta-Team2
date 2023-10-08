from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include("api.v_1.urls", namespace="api")),
]

urlpatterns += [
    path(
        "docs-auto/schema/", SpectacularAPIView.as_view(), name="schema"
    ),
    path("docs-auto/", SpectacularRedocView.as_view(), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
