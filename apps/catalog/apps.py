from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.catalog"

    def ready(self) -> None:
        import apps.catalog.infrastructure.models  # noqa
        import apps.catalog.infrastructure.admin  # noqa
