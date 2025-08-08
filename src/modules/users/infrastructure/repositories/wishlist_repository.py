from typing import override
from uuid import UUID

from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.exceptions import WishlistItemNotFoundError
from src.modules.users.domain.factories.wishlist_factory import WishlistFactory
from src.modules.users.domain.interfaces.wishlist_repository_interface import WishlistRepositoryInterface
from src.modules.users.infrastructure.models.wishlist_model import WishlistModel


class WishlistRepository(WishlistRepositoryInterface):
    # Messages
    PRODUCT_NOT_FOUND: str = "Product not found."

    @override
    def get_by_user(self, user_id: UUID) -> list[Wishlist]:
        return [
            WishlistFactory.from_model(obj)
            for obj in WishlistModel.objects.filter(user_id_id=user_id).only("id", "product_id", "created_at")
        ]

    @override
    def add_item(self, wishlist: Wishlist) -> Wishlist:
        wishlist_model = WishlistModel.objects.create(user_id_id=wishlist.user_id, product_id=wishlist.product_id)
        return WishlistFactory.from_model(wishlist_model)

    @override
    def delete_item(self, user_id: UUID, product_id: UUID) -> None:
        wishlist_item = WishlistModel.objects.filter(user_id_id=user_id, product_id=product_id)
        if not wishlist_item:
            raise WishlistItemNotFoundError(self.PRODUCT_NOT_FOUND)
        wishlist_item.delete()

    @override
    def exists(self, user_id: UUID, product_id: UUID) -> bool:
        return WishlistModel.objects.filter(user_id_id=user_id, product_id=product_id).exists()
