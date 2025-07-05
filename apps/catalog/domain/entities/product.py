from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from apps.catalog.domain.exceptions import ProductDomainError
from apps.catalog.domain.value_objects.sku import SKU
from apps.catalog.domain.value_objects.weight_unit import WeightUnit


@dataclass(kw_only=True, slots=True)
class Product:
    id: UUID
    name: str
    description: str
    sku: SKU
    category_id: UUID
    price: Decimal
    discount_price: Decimal | None = None
    stock: int = 0
    min_stock: int = 5
    image_url: str | None = None
    is_active: bool = True
    is_featured: bool = False
    weight: Decimal | None = None
    unit: WeightUnit
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # Constants
    MIN_PRICE: Decimal = Decimal("0")
    MIN_DISCOUNT: Decimal = Decimal("0")
    MAX_STOCK: int = 100
    MIN_STOCK: int = 0

    # Messages
    NAME_REQUIRED_MSG: str = "Name is required."
    PRICE_NEGATIVE_MSG: str = "Price cannot be negative."
    DISCOUNT_NEGATIVE_MSG: str = "Discount price cannot be negative."
    DISCOUNT_EXCEEDS_PRICE_MSG: str = "Discount price cannot exceed price."
    STOCK_NEGATIVE_MSG: str = "Stock cannot be negative."
    STOCK_EXCEEDS_MAX_MSG: str = "Stock cannot exceed 100 units."
    MIN_STOCK_NEGATIVE_MSG: str = "Min stock cannot be negative."

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.name:
            raise ProductDomainError(self.NAME_REQUIRED_MSG)

        if self.price < self.MIN_PRICE:
            raise ProductDomainError(self.PRICE_NEGATIVE_MSG)

        if self.discount_price is not None:
            if self.discount_price < self.MIN_DISCOUNT:
                raise ProductDomainError(self.DISCOUNT_NEGATIVE_MSG)
            if self.discount_price > self.price:
                raise ProductDomainError(self.DISCOUNT_EXCEEDS_PRICE_MSG)

        if self.stock < self.MIN_STOCK:
            raise ProductDomainError(self.STOCK_NEGATIVE_MSG)

        if self.stock > self.MAX_STOCK:
            raise ProductDomainError(self.STOCK_EXCEEDS_MAX_MSG)

        if self.min_stock < self.MIN_STOCK:
            raise ProductDomainError(self.MIN_STOCK_NEGATIVE_MSG)
