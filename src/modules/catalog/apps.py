from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.catalog"

    def ready(self) -> None:
        import modules.catalog.infrastructure.admin
        import modules.catalog.infrastructure.models  # noqa: F401
