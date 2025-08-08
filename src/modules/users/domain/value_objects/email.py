import re
from dataclasses import dataclass

from src.modules.users.domain.exceptions import UserDomainError


@dataclass(frozen=True)
class Email:
    value: str

    # Constants
    EMAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"

    # Messages
    EMAIL_INVALID_FORMAT_MSG = "Invalid email format."

    def __post_init__(self) -> None:
        self._validate()

    def __str__(self) -> str:
        return self.value

    def _validate(self) -> None:
        if not re.match(self.EMAIL_PATTERN, self.value):
            raise UserDomainError(self.EMAIL_INVALID_FORMAT_MSG)
