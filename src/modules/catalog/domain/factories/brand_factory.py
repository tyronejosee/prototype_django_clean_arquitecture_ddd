from datetime import UTC, datetime
from uuid import uuid4

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.value_objects.brand_name import BrandName


class BrandFactory:
    @staticmethod
    def from_dict(data) -> Brand:
        return Brand(
            id=data.get("id", uuid4()),
            name=BrandName(data["name"]),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.now(UTC)),
            updated_at=data.get("updated_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Brand:
        return Brand(
            id=data.id,
            name=data.name,
            is_active=data.is_active,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
