from uuid import uuid4
from datetime import datetime

from ..entities.user import User
from ..value_objects.email import Email


class UserFactory:
    @staticmethod
    def from_dict(data: dict) -> User:
        return User(
            id=data.get("id", uuid4()),
            email=Email(data["email"]),
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            is_active=data.get("is_active", True),
            is_staff=data.get("is_staff", False),
            is_superuser=data.get("is_superuser", False),
            last_login=data.get("last_login"),
            date_joined=data.get("date_joined", datetime.now()),
        )

    @staticmethod
    def from_model(data) -> User:
        return User(
            id=data.id,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=data.is_active,
            is_staff=data.is_staff,
            is_superuser=data.is_superuser,
            last_login=data.last_login,
            date_joined=data.date_joined,
        )
