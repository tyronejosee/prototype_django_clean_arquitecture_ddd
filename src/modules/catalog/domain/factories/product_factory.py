from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.value_objects.currency import Currency
from src.modules.catalog.domain.value_objects.sku import SKU
from src.modules.catalog.domain.value_objects.slug import Slug
from src.modules.catalog.domain.value_objects.weight_unit import WeightUnit


class ProductFactory:
    @staticmethod
    def from_dict(data) -> Product:
        return Product(
            id=data.get("id", uuid4()),
            name=data["name"],
            slug=Slug.from_name(data["name"]),
            description=data["description"],
            sku=SKU(data["sku"]),
            category_id=data["category_id"],
            brand_id=data["brand_id"],
            price=Decimal(data["price"]),
            discount_price=(Decimal(data["discount_price"]) if data.get("discount_price") else None),
            currency=Currency(data.get("currency", "USD")),
            stock=data.get("stock", 0),
            min_stock=data.get("min_stock", 5),
            warehouse_location=data.get("warehouse_location", ""),
            image_url=data.get("image_url", ""),
            is_active=data.get("is_active", True),
            is_featured=data.get("is_featured", False),
            weight=Decimal(data["weight"]) if data.get("weight") else None,
            unit=WeightUnit(data.get("unit", "kg")),
            nutritional_info=data.get("nutritional_info", {}),
            ingredients=data.get("ingredients", {}),
            allergens=data.get("allergens", {}),
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Product:
        return Product(
            id=data.id,
            name=data.name,
            slug=data.slug,
            description=data.description,
            sku=data.sku,
            category_id=data.category_id,
            brand_id=data.brand_id,
            price=data.price,
            discount_price=data.discount_price,
            currency=data.currency,
            stock=data.stock,
            min_stock=data.min_stock,
            warehouse_location=data.warehouse_location,
            image_url=data.image.url if data.image else "",
            is_active=data.is_active,
            is_featured=data.is_featured,
            weight=data.weight,
            unit=data.unit,
            nutritional_info=data.nutritional_info,
            ingredients=data.ingredients,
            allergens=data.allergens,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
