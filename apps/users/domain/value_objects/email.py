import re
from dataclasses import dataclass

from apps.users.domain.exceptions import UserDomainError


@dataclass(frozen=True)
class Email:
    value: str

    # Constants
    EMAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"

    # Messages
    EMAIL_INVALID_FORMAT_MSG = "Invalid email format."

    def __post_init__(self) -> None:
        if not re.match(self.EMAIL_PATTERN, self.value):
            raise UserDomainError(self.EMAIL_INVALID_FORMAT_MSG)

    def __str__(self) -> str:
        return self.value
