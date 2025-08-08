from uuid import UUID

from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.exceptions import WishlistItemAlreadyExistsError
from src.modules.users.domain.factories.wishlist_factory import WishlistFactory
from src.modules.users.domain.interfaces.wishlist_repository_interface import WishlistRepositoryInterface


class AddToWishlistUseCase:
    # Messages
    PRODUCT_ALREADY_IN_WISHLIST: str = "Product already in wishlist."

    def __init__(self, repo: WishlistRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, product_id: UUID) -> Wishlist:
        if self.repo.exists(user_id, product_id):
            raise WishlistItemAlreadyExistsError(self.PRODUCT_ALREADY_IN_WISHLIST)
        wishlist_item = WishlistFactory.from_dict({"user_id": user_id, "product_id": product_id})
        return self.repo.add_item(wishlist_item)
