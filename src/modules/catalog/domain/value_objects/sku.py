import re
from dataclasses import dataclass

from src.modules.catalog.domain.exceptions import ProductDomainError


@dataclass(frozen=True)
class SKU:
    value: str

    # Constants
    MIN_LENGTH = 4
    MAX_LENGTH = 32
    REGEX_PATTERN = r"^[A-Z0-9\-]+$"

    # Messages
    SKU_REQUIRED_MSG = "SKU is required."
    SKU_TOO_SHORT_MSG = "SKU must be at least '{min_length}' characters."
    SKU_TOO_LONG_MSG = "SKU must be at most '{max_length}' characters."
    SKU_INVALID_FORMAT_MSG = "SKU format is invalid. Only uppercase letters, numbers and dashes are allowed."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        # Normalize the value
        object.__setattr__(self, "value", self.value.strip() if self.value else "")
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise ProductDomainError(self.SKU_REQUIRED_MSG)

        if len(self.value) < self.MIN_LENGTH:
            message = self.SKU_TOO_SHORT_MSG.format(min_length=self.MIN_LENGTH)
            raise ProductDomainError(message)

        if len(self.value) > self.MAX_LENGTH:
            message = self.SKU_TOO_LONG_MSG.format(max_length=self.MAX_LENGTH)
            raise ProductDomainError(message)

        if not re.fullmatch(self.REGEX_PATTERN, self.value):
            raise ProductDomainError(self.SKU_INVALID_FORMAT_MSG)
