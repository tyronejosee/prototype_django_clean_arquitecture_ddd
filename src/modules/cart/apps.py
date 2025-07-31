from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.cart"

    def ready(self) -> None:
        import modules.cart.infrastructure.admin
        import modules.cart.infrastructure.models  # noqa: F401
