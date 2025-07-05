from dataclasses import dataclass
from typing import ClassVar

from apps.catalog.domain.exceptions import ProductDomainError


@dataclass(frozen=True)
class WeightUnit:
    value: str = "kg"

    # Constants
    VALID_UNITS: ClassVar[set] = {"kg", "g", "lb"}

    # Messages
    INVALID_UNIT_MSG: str = "Invalid unit."

    def __post_init__(self) -> None:
        self._validate()

    def __str__(self) -> str:
        return self.value

    def _validate(self) -> None:
        if self.value not in self.VALID_UNITS:
            raise ProductDomainError(self.INVALID_UNIT_MSG)
