from uuid import UUID

from src.modules.users.domain.interfaces.wishlist_repository_interface import WishlistRepositoryInterface


class RemoveFromWishlistUseCase:
    def __init__(self, repo: WishlistRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID, product_id: UUID) -> None:
        self.repo.delete_item(user_id, product_id)
