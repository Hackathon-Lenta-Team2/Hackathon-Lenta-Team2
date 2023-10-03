from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.doc_schema import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls.authtoken")),
    path("api/v1/", include("api.v_1.urls", namespace="api")),
]

urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
