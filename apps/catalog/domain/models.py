"""Models for the catalog domain."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID
from uuid import uuid4
from datetime import datetime


@dataclass
class Category:
    id: UUID
    name: str
    description: str = ""
    parent_id: Optional[UUID] = None
    image_url: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(
            id=data.get("id", uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Product:
    id: UUID
    name: str
    description: str
    sku: str
    category_id: UUID
    price: Decimal
    discount_price: Optional[Decimal] = None
    stock: int = 0
    min_stock: int = 5
    image_url: Optional[str] = None
    is_active: bool = True
    is_featured: bool = False
    weight: Optional[Decimal] = None
    unit: str = "kg"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def current_price(self) -> Decimal:
        return self.discount_price if self.discount_price else self.price

    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0

    @property
    def is_low_stock(self) -> bool:
        return self.stock <= self.min_stock

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            id=data.get("id", uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            sku=data["sku"],
            category_id=data["category_id"],
            price=Decimal(data["price"]),
            discount_price=(
                Decimal(data["discount_price"])
                if data.get(
                    "discount_price",
                )
                else None
            ),
            stock=data.get("stock", 0),
            min_stock=data.get("min_stock", 5),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
            is_featured=data.get("is_featured", False),
            weight=Decimal(data["weight"]) if data.get("weight") else None,
            unit=data.get("unit", "kg"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
