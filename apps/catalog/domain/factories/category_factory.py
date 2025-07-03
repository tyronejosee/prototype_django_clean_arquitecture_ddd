"""Category factory for the catalog domain"""

from datetime import datetime
from uuid import uuid4

from apps.catalog.domain.entities import Category


class CategoryFactory:
    @staticmethod
    def from_dict(data) -> Category:
        return Category(
            id=data.get("id", uuid4()),
            name=data["name"],
            description=data.get("description", ""),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.now()),
            updated_at=data.get("updated_at", datetime.now()),
        )

    @staticmethod
    def from_model(data) -> Category:
        return Category(
            id=data.id,
            name=data.name,
            description=data.description,
            is_active=data.is_active,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
