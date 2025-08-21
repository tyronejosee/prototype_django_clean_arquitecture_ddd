from dataclasses import dataclass

from src.modules.catalog.domain.exceptions import ProductDomainError


@dataclass(frozen=True)
class ProductName:
    value: str

    # Messages
    PRODUCT_NAME_REQUIRED_MSG: str = "Product name is required."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        # Normalize the value
        object.__setattr__(self, "value", self.value.strip() if self.value else "")
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise ProductDomainError(self.PRODUCT_NAME_REQUIRED_MSG)
