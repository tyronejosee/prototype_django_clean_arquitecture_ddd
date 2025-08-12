from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.users.domain.entities.wishlist import Wishlist


class WishlistRepositoryInterface(ABC):
    @abstractmethod
    def get_by_user(self, user_id: UUID) -> list[Wishlist]: ...

    @abstractmethod
    def add_item(self, wishlist: Wishlist) -> Wishlist: ...

    @abstractmethod
    def delete_item(self, user_id: UUID, product_id: UUID) -> None: ...

    @abstractmethod
    def exists(self, user_id: UUID, product_id: UUID) -> bool: ...
