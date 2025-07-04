"""Entities for the catalog domain"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from apps.catalog.domain.exceptions import (
    CategoryDomainError,
    ProductDomainError,
)


class Category:
    _forbidden_words = {"forbidden", "badword", "invalid", "test"}

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str = "",
        is_active: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

        self._validate()

    def _validate(self) -> None:
        if not self.name:
            raise CategoryDomainError("Name is required.")

        for forbidden_word in self._forbidden_words:
            if forbidden_word in self.name.strip().lower():
                message = f"Name contains a forbidden word: '{forbidden_word}'."
                raise CategoryDomainError(message)


class Product:
    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        sku: str,
        category_id: UUID,
        price: Decimal,
        discount_price: Decimal | None = None,
        stock: int = 0,
        min_stock: int = 5,
        image_url: str | None = None,
        is_active: bool = True,
        is_featured: bool = False,
        weight: Decimal | None = None,
        unit: str = "kg",
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.sku = sku
        self.category_id = category_id
        self.price = price
        self.discount_price = discount_price
        self.stock = stock
        self.min_stock = min_stock
        self.image_url = image_url
        self.is_active = is_active
        self.is_featured = is_featured
        self.weight = weight
        self.unit = unit
        self.created_at = created_at
        self.updated_at = updated_at

        self._validate()

    def _validate(self) -> None:
        if not self.name:
            raise ProductDomainError("Name is required.")

        if self.price < 0:
            raise ProductDomainError("Price cannot be negative.")

        if self.discount_price is not None and self.discount_price < 0:
            raise ProductDomainError("Discount price cannot be negative.")

        if self.discount_price is not None and self.discount_price > self.price:
            raise ProductDomainError("Discount price cannot exceed price.")

        if self.stock < 0:
            raise ProductDomainError("Stock cannot be negative.")

        if self.stock > 100:
            raise ProductDomainError("Stock cannot exceed 100 units.")

        if self.min_stock < 0:
            raise ProductDomainError("Min stock cannot be negative.")
