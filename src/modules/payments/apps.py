from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.payments"

    def ready(self) -> None:
        import src.modules.payments.infrastructure.admin
        import src.modules.payments.infrastructure.models  # noqa: F401
