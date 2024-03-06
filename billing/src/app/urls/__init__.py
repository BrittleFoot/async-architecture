from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("api/", include("app.urls.api.v1")),
    path("admin/", admin.site.urls),
    path(
        "openapi/",
        get_schema_view(
            title="", description="OpenAPI schema", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]
