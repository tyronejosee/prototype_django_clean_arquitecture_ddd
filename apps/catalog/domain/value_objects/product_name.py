from dataclasses import dataclass

from apps.catalog.domain.exceptions import ProductDomainError


@dataclass(frozen=True)
class ProductName:
    value: str

    # Messages
    PRODUCT_NAME_REQUIRED_MSG: str = "Product name is required."

    def __post_init__(self) -> None:
        self._validate()

    def __str__(self) -> str:
        return self.value

    def _validate(self) -> None:
        if not self.value or not self.value.strip():
            raise ProductDomainError(self.PRODUCT_NAME_REQUIRED_MSG)
