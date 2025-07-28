from uuid import uuid4

from apps.marketing.domain.entities.promotion import Promotion


class PromotionFactory:
    @staticmethod
    def from_dict(data) -> Promotion:
        return Promotion(
            id=data.get("id", uuid4()),
            name=data.get("name", ""),
            description=data.get("description", ""),
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
            is_active=data.is_active,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
        )
