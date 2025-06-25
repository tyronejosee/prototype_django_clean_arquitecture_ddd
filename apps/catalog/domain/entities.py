"""Entities for the catalog domain"""

from uuid import UUID
from typing import Optional
from decimal import Decimal
from datetime import datetime


class Category:
    def __init__(
        self,
        id: UUID,
        name: str,
        description: str = "",
        parent_id: Optional[UUID] = None,
        image_url: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.image_url = image_url
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at


class Product:
    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        sku: str,
        category_id: UUID,
        price: Decimal,
        discount_price: Optional[Decimal] = None,
        stock: int = 0,
        min_stock: int = 5,
        image_url: Optional[str] = None,
        is_active: bool = True,
        is_featured: bool = False,
        weight: Optional[Decimal] = None,
        unit: str = "kg",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
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
