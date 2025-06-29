"""URLs config for the project."""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns: list = [
    path("admin/", admin.site.urls),
    # path("api/", include("apps.users.urls")),
    # path("api/", include("apps.catalog.interfaces.routers")),
    # path("api/", include("apps.cart.interfaces.routers")),
    # path("api/", include("apps.orders.interfaces.routers")),
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
