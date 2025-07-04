import re
from dataclasses import dataclass

from apps.users.domain.exceptions import UserDomainError


@dataclass(frozen=True)
class Username:
    value: str

    MIN_LENGTH = 4
    MAX_LENGTH = 30
    VALID_PATTERN = r"^[a-zA-Z0-9_.-]+$"

    def __post_init__(self) -> None:
        if not self.value:
            raise UserDomainError("Username is required.")

        if len(self.value) < self.MIN_LENGTH:
            raise UserDomainError("Username is too short.")

        if len(self.value) > self.MAX_LENGTH:
            raise UserDomainError("Username is too long.")

        if not re.match(self.VALID_PATTERN, self.value):
            raise UserDomainError(
                "Username can only contain letters, numbers, "
                "underscores, hyphens, and dots."
            )

    def __str__(self) -> str:
        return self.value
