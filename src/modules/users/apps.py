from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "modules.users"

    def ready(self) -> None:
        import modules.users.infrastructure.admin
        import modules.users.infrastructure.models  # noqa: F401
