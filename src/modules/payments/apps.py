from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.payments"

    def ready(self) -> None:
        import modules.payments.infrastructure.admin
        import modules.payments.infrastructure.models  # noqa: F401
