from uuid import uuid4
from datetime import datetime


def valid_user_dict() -> dict:
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "password": "plain_password",
        "first_name": "Carlos",
        "last_name": "Ramirez",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "last_login": None,
        "date_joined": datetime.now(),
    }
