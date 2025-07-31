from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.orders"

    def ready(self) -> None:
        import src.modules.orders.infrastructure.admin
        import src.modules.orders.infrastructure.models  # noqa: F401
