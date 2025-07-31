from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "src.modules.users"

    def ready(self) -> None:
        import src.modules.users.infrastructure.admin
        import src.modules.users.infrastructure.models  # noqa: F401
