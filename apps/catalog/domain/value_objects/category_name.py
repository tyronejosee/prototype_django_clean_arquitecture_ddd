from dataclasses import dataclass
from typing import ClassVar

from apps.catalog.domain.exceptions import CategoryDomainError


@dataclass(frozen=True)
class CategoryName:
    value: str

    # Constants
    FORBIDDEN_WORDS: ClassVar[set] = {"forbidden", "badword", "invalid", "test"}

    # Messages
    CATEGORY_NAME_REQUIRED_MSG: str = "Category name is required."
    NAME_FORBIDDEN_WORD_MSG: str = "Category name '{value}' is not allowed."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.value or not self.value.strip():
            raise CategoryDomainError(self.CATEGORY_NAME_REQUIRED_MSG)

        if self.value.strip().lower() in self.FORBIDDEN_WORDS:
            message = self.NAME_FORBIDDEN_WORD_MSG.format(value=self.value)
            raise CategoryDomainError(message)
