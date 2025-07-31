from datetime import UTC, datetime
from uuid import uuid4


def valid_user_dict() -> dict:
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "username": "testuser",
        "password": "plain_password",
        "first_name": "Carlos",
        "last_name": "Ramirez",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "last_login": None,
        "date_joined": datetime.now(UTC),
    }
