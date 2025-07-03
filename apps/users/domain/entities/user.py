from uuid import UUID
from datetime import datetime

from ..value_objects.email import Email
from ..exceptions import UserDomainException


class User:
    def __init__(
        self,
        id: UUID,
        password: str,
        email: Email,
        first_name: str = "",
        last_name: str = "",
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False,
        last_login: datetime | None = None,
        date_joined: datetime | None = None,
    ) -> None:
        self.id = id
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_staff = is_staff
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.last_login = last_login
        self.date_joined = date_joined

        self._validate()

    def _validate(self) -> None:
        if not self.first_name and not self.last_name:
            raise UserDomainException(
                "User must have at least a first name or last name."
            )

        if self.first_name and len(self.first_name) < 5:
            raise UserDomainException("First name is too short.")

        if self.last_name and len(self.last_name) < 5:
            raise UserDomainException("Last name is too short.")

        if self.is_superuser and not self.is_staff:
            raise UserDomainException("A superuser must also be staff.")

        if not self.is_active and self.last_login:
            raise UserDomainException(
                "Inactive user should not have a last login timestamp."
            )
