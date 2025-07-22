from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.orders"

    def ready(self) -> None:
        import apps.orders.infrastructure.admin
        import apps.orders.infrastructure.models  # noqa: F401
