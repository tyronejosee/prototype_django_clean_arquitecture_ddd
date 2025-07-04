from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self) -> None:
        import apps.users.infrastructure.admin  # noqa: F401
        import apps.users.infrastructure.models  # noqa: F401
