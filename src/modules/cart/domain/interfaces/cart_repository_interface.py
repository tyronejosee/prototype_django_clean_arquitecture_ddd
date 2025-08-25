from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.entities.cart_item import CartItem


class CartRepositoryInterface(ABC):
    @abstractmethod
    def get_by_user(self, user_id: UUID) -> Cart: ...

    @abstractmethod
    def create(self, user_id: UUID) -> Cart: ...

    @abstractmethod
    def add_items(self, user_id: UUID, items: list[CartItem]) -> Cart: ...

    @abstractmethod
    def patch_item(self, user_id: UUID, item_id: UUID, quantity: int) -> Cart: ...

    @abstractmethod
    def delete_item(self, user_id: UUID, item_id: UUID) -> Cart: ...

    @abstractmethod
    def clear(self, user_id: UUID) -> None: ...
