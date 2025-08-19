from dataclasses import dataclass
from typing import ClassVar

from src.modules.catalog.domain.exceptions import ProductDomainError


@dataclass(frozen=True, slots=True)
class Currency:
    value: str

    # Constants
    VALID_CURRENCIES: ClassVar[set] = {"USD", "CLP"}

    # Messages
    INVALID_CURRENCY_MSG: str = "Invalid currency {value}."

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.value not in self.VALID_CURRENCIES:
            raise ProductDomainError(self.INVALID_CURRENCY_MSG.format(value=self.value))
