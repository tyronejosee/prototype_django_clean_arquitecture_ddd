import re
from dataclasses import dataclass

from apps.users.domain.exceptions import UserDomainError


@dataclass(frozen=True)
class Email:
    value: str

    EMAIL_PATTERN = r"[^@]+@[^@]+\.[^@]+"

    def __post_init__(self) -> None:
        if not re.match(self.EMAIL_PATTERN, self.value):
            raise UserDomainError("Invalid email format.")

    def __str__(self) -> str:
        return self.value
