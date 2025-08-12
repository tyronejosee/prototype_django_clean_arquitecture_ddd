from uuid import UUID

from src.modules.users.domain.entities.wishlist import Wishlist
from src.modules.users.domain.interfaces.wishlist_repository_interface import WishlistRepositoryInterface


class ListWishlistUseCase:
    def __init__(self, repo: WishlistRepositoryInterface) -> None:
        self.repo = repo

    def execute(self, user_id: UUID) -> list[Wishlist]:
        return self.repo.get_by_user(user_id)
