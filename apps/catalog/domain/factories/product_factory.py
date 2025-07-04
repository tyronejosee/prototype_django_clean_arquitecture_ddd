"""Product factory for the catalog domain"""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from apps.catalog.domain.entities import Product


class ProductFactory:
    @staticmethod
    def from_dict(data) -> Product:
        return Product(
            id=data.get("id", uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            sku=data["sku"],
            category_id=data["category_id"],
            price=Decimal(data["price"]),
            discount_price=(
                Decimal(data["discount_price"]) if data.get("discount_price") else None
            ),
            stock=data.get("stock", 0),
            min_stock=data.get("min_stock", 5),
            image_url=data.get("image_url"),
            is_active=data.get("is_active", True),
            is_featured=data.get("is_featured", False),
            weight=Decimal(data["weight"]) if data.get("weight") else None,
            unit=data.get("unit", "kg"),
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Product:
        return Product(
            id=data.id,
            name=data.name,
            description=data.description,
            sku=data.sku,
            category_id=data.category_id,
            price=data.price,
            discount_price=data.discount_price,
            stock=data.stock,
            min_stock=data.min_stock,
            image_url=data.image.url if data.image else None,
            is_active=data.is_active,
            is_featured=data.is_featured,
            weight=data.weight,
            unit=data.unit,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
