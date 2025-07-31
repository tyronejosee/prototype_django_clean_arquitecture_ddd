from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.marketing"

    def ready(self) -> None:
        import src.modules.marketing.infrastructure.admin
        import src.modules.marketing.infrastructure.models  # noqa: F401
