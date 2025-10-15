"""URLs config for the project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from src.core.health_chech import health_check

urlpatterns: list = [
    path("", RedirectView.as_view(url="docs", permanent=False)),
    path("health-check", health_check),
    path("admin/", admin.site.urls),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/", include("src.modules.cart.presentation.routers")),
    path("api/", include("src.modules.catalog.presentation.routers")),
    path("api/", include("src.modules.marketing.presentation.routers")),
    path("api/", include("src.modules.orders.presentation.routers")),
    path("api/", include("src.modules.payments.presentation.routers")),
    path("api/", include("src.modules.users.presentation.routers")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom attributes for admin
admin.site.site_header = "Marketly"
admin.site.site_title = "Marketly"
admin.site.index_title = "Admin"
