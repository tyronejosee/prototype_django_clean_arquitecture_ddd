from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.marketing"

    def ready(self) -> None:
        import modules.marketing.infrastructure.admin
        import modules.marketing.infrastructure.models  # noqa: F401
