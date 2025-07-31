"""URLs config for the project."""

from core.health_chech import health_check
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns: list = [
    path("", health_check),
    path("admin/", admin.site.urls),
    path("api/", include("modules.cart.presentation.routers")),
    path("api/", include("modules.catalog.presentation.routers")),
    path("api/", include("modules.marketing.presentation.routers")),
    path("api/", include("modules.orders.presentation.routers")),
    path("api/", include("modules.payments.presentation.routers")),
    path("api/", include("modules.users.presentation.routers")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
