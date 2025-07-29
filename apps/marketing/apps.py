from django.apps import AppConfig


class MarketingConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.marketing"

    def ready(self) -> None:
        import apps.marketing.infrastructure.admin
        import apps.marketing.infrastructure.models  # noqa: F401
