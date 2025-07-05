import re
from dataclasses import dataclass

from apps.users.domain.exceptions import UserDomainError


@dataclass(frozen=True)
class Username:
    value: str

    # Constants
    MIN_LENGTH = 4
    MAX_LENGTH = 30
    VALID_PATTERN = r"^[a-zA-Z0-9_.-]+$"

    # Messages
    USERNAME_REQUIRED_MSG = "Username is required."
    USERNAME_TOO_SHORT_MSG = "Username is too short."
    USERNAME_TOO_LONG_MSG = "Username is too long."
    USERNAME_INVALID_FORMAT_MSG = "Invalid username format."

    def __post_init__(self) -> None:
        if not self.value:
            raise UserDomainError(self.USERNAME_REQUIRED_MSG)

        if len(self.value) < self.MIN_LENGTH:
            raise UserDomainError(self.USERNAME_TOO_SHORT_MSG)

        if len(self.value) > self.MAX_LENGTH:
            raise UserDomainError(self.USERNAME_TOO_LONG_MSG)

        if not re.match(self.VALID_PATTERN, self.value):
            raise UserDomainError(self.USERNAME_INVALID_FORMAT_MSG)

    def __str__(self) -> str:
        return self.value
