from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.cart"

    def ready(self) -> None:
        import apps.cart.infrastructure.admin
        import apps.cart.infrastructure.models  # noqa: F401
