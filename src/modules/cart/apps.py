from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.cart"

    def ready(self) -> None:
        import src.modules.cart.infrastructure.admin
        import src.modules.cart.infrastructure.models  # noqa: F401
