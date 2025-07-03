from uuid import uuid4
from datetime import datetime

from ....domain.entities.user import User
from ....domain.value_objects.email import Email
from ....domain.factories.user import UserFactory


def test_from_dict_creates_user() -> None:
    data = {
        "id": uuid4(),
        "email": "test@example.com",
        "password": "hashed_pass",
        "first_name": "Example",
        "last_name": "Example",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "last_login": None,
        "date_joined": datetime.now(),
    }
    user = UserFactory.from_dict(data)
    assert isinstance(user, User)
    assert user.email == Email("test@example.com")
    assert user.first_name == "Example"
    assert user.last_name == "Example"


class DummyModel:
    def __init__(self) -> None:
        self.id = uuid4()
        self.email = Email("model@example.com")
        self.password = "hashed_pass"
        self.first_name = "Analia"
        self.last_name = "Lopez"
        self.is_active = True
        self.is_staff = True
        self.is_superuser = False
        self.last_login = None
        self.date_joined = datetime.now()


def test_from_model_creates_user() -> None:
    model = DummyModel()
    user = UserFactory.from_model(model)
    assert isinstance(user, User)
    assert user.email == model.email
    assert user.first_name == model.first_name
    assert user.is_staff is True
