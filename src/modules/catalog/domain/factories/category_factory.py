from datetime import UTC, datetime
from uuid import uuid4

from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.slug import Slug


class CategoryFactory:
    @staticmethod
    def from_dict(data) -> Category:
        return Category(
            id=data.get("id", uuid4()),
            name=CategoryName(data["name"]),
            slug=Slug.from_name(data["name"]),
            description=data.get("description", ""),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Category:
        return Category(
            id=data.id,
            name=data.name,
            slug=data.slug,
            description=data.description,
            is_active=data.is_active,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
