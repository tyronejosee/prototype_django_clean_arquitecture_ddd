from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from apps.users.domain.exceptions import UserDomainError
from apps.users.domain.value_objects.email import Email
from apps.users.domain.value_objects.username import Username


@dataclass(kw_only=True, slots=True)
class User:
    id: UUID
    password: str
    email: Email
    username: Username
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    last_login: datetime | None = None
    date_joined: datetime | None = None

    # Constants
    MIN_FIRST_NAME_LENGTH: int = field(init=False, default=2)
    MIN_LAST_NAME_LENGTH: int = field(init=False, default=2)

    # Messages
    NAME_REQUIRED_MSG: str = "First or last name required."
    FIRST_NAME_TOO_SHORT_MSG: str = "First name is too short."
    LAST_NAME_TOO_SHORT_MSG: str = "Last name is too short."
    SUPERUSER_MUST_BE_STAFF_MSG: str = "A superuser must also be staff."
    INACTIVE_WITH_LAST_LOGIN_MSG: str = "Inactive user can't have last login."

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.first_name and not self.last_name:
            raise UserDomainError(self.NAME_REQUIRED_MSG)

        if self.first_name and len(self.first_name) < self.MIN_FIRST_NAME_LENGTH:
            raise UserDomainError(self.FIRST_NAME_TOO_SHORT_MSG)

        if self.last_name and len(self.last_name) < self.MIN_LAST_NAME_LENGTH:
            raise UserDomainError(self.LAST_NAME_TOO_SHORT_MSG)

        if self.is_superuser and not self.is_staff:
            raise UserDomainError(self.SUPERUSER_MUST_BE_STAFF_MSG)

        if not self.is_active and self.last_login:
            raise UserDomainError(self.INACTIVE_WITH_LAST_LOGIN_MSG)
