from abc import ABC, abstractmethod
from uuid import UUID

from apps.cart.domain.entities.cart import Cart


class CartRepositoryInterface(ABC):
    @abstractmethod
    def get_by_user(self, user_id: UUID) -> Cart: ...

    @abstractmethod
    def create(self, cart: Cart) -> Cart: ...

    @abstractmethod
    def update(self, cart: Cart) -> Cart: ...

    @abstractmethod
    def patch_item(self, user_id: UUID, item_id: UUID, quantity: int) -> Cart: ...

    @abstractmethod
    def delete_item(self, user_id: UUID, item_id: UUID) -> Cart: ...

    @abstractmethod
    def preview(self, cart: Cart) -> dict: ...
