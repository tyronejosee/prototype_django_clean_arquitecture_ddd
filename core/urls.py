"""URLs config for the project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .health_chech import health_check

urlpatterns: list = [
    path("", health_check),
    path("admin/", admin.site.urls),
    path("api/", include("apps.cart.presentation.routers")),
    path("api/", include("apps.catalog.presentation.routers")),
    path("api/", include("apps.orders.presentation.routers")),
    path("api/", include("apps.payments.presentation.routers")),
    path("api/", include("apps.users.presentation.routers")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
