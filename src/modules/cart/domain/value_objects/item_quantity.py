from dataclasses import dataclass

from modules.cart.domain.exceptions import CartDomainError


@dataclass(frozen=True)
class ItemQuantity:
    value: int

    # Constants
    MIN: int = 1
    MAX: int = 10

    # Messages
    QUANTITY_OUT_OF_RANGE_MSG: str = "Quantity must be between {min} and {max}."

    def __post_init__(self) -> None:
        self._validate()

    def __int__(self) -> int:
        return self.value

    def _validate(self) -> None:
        if not (self.value >= self.MIN and self.value <= self.MAX):
            raise CartDomainError(
                self.QUANTITY_OUT_OF_RANGE_MSG.format(min=self.MIN, max=self.MAX),
            )
