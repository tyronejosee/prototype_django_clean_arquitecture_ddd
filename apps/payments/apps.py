from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.payments"

    def ready(self) -> None:
        import apps.payments.infrastructure.admin
        import apps.payments.infrastructure.models  # noqa: F401
