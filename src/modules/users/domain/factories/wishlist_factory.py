from uuid import uuid4

from src.modules.users.domain.entities.wishlist import Wishlist


class WishlistFactory:
    @staticmethod
    def from_dict(data: dict) -> Wishlist:
        return Wishlist(
            id=data.get("id", uuid4()),
            user_id=data["user_id"],
            product_id=data["product_id"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_model(model) -> Wishlist:
        return Wishlist(
            id=model.id,
            user_id=model.user_id_id,
            product_id=model.product_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
