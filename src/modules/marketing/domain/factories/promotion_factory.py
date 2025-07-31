from uuid import uuid4

from src.modules.marketing.domain.entities.promotion import Promotion
from src.modules.marketing.domain.value_objects.discount_percent import DiscountPercent


class PromotionFactory:
    @staticmethod
    def from_dict(data) -> Promotion:
        return Promotion(
            id=data.get("id", uuid4()),
            name=data.get("name", ""),
            description=data.get("description", ""),
            discount_percent=DiscountPercent(data["discount_percent"]),
            is_active=data.get("is_active", True),
            starts_at=data.get("starts_at", None),
            ends_at=data.get("ends_at", None),
        )

    @staticmethod
    def from_model(data) -> Promotion:
        return Promotion(
            id=data.id,
            name=data.name,
            description=data.description,
            discount_percent=data.discount_percent,
            is_active=data.is_active,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
        )
