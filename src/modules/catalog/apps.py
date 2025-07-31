from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.catalog"

    def ready(self) -> None:
        import src.modules.catalog.infrastructure.admin
        import src.modules.catalog.infrastructure.models  # noqa: F401
