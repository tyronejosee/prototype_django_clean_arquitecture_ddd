from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users_users"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["email"]

    def __str__(self) -> str:
        return str(self.email)
