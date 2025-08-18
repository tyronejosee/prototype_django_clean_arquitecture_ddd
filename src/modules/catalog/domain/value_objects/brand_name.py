from dataclasses import dataclass
from typing import ClassVar

from src.modules.catalog.domain.exceptions import BrandDomainError


@dataclass(frozen=True)
class BrandName:
    value: str

    # Constants
    FORBIDDEN_WORDS: ClassVar[set] = {"forbidden", "badword", "invalid", "test"}

    # Messages
    BRAND_NAME_REQUIRED_MSG: str = "Brand name is required."
    NAME_FORBIDDEN_WORD_MSG: str = "Brand name '{value}' is not allowed."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.value or not self.value.strip():
            raise BrandDomainError(self.BRAND_NAME_REQUIRED_MSG)

        if self.value.strip().lower() in self.FORBIDDEN_WORDS:
            raise BrandDomainError(self.NAME_FORBIDDEN_WORD_MSG.format(value=self.value))
