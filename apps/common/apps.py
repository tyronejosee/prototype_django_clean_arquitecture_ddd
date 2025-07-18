from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name = "apps.common"
