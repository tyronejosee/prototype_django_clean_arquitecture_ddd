from uuid import UUID

from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.exceptions import WishlistDomainError, WishlistItemAlreadyExistsError
from src.modules.users.domain.factories.wishlist_factory import WishlistFactory
from src.modules.users.domain.interfaces.wishlist_repository_interface import WishlistRepositoryInterface
from src.modules.users.domain.ports.product_port import ProductPort


class AddToWishlistUseCase:
    # Messages
    PRODUCT_ALREADY_IN_WISHLIST: str = "Product already in wishlist."
    PRODUCT_NOT_FOUND: str = "Product not found."

    def __init__(self, repo: WishlistRepositoryInterface, product_adapter: ProductPort) -> None:
        self.repo = repo
        self.product_adapter = product_adapter

    def execute(self, user_id: UUID, product_id: UUID) -> Wishlist:
        if self.repo.exists(user_id, product_id):
            raise WishlistItemAlreadyExistsError(self.PRODUCT_ALREADY_IN_WISHLIST)

        if not self.product_adapter.exists(product_id):
            raise WishlistDomainError(self.PRODUCT_NOT_FOUND)

        wishlist_item = WishlistFactory.from_dict({"user_id": user_id, "product_id": product_id})
        return self.repo.add_item(wishlist_item)
