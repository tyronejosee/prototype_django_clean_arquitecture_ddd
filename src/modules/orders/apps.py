from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.orders"

    def ready(self) -> None:
        import modules.orders.infrastructure.admin
        import modules.orders.infrastructure.models  # noqa: F401
