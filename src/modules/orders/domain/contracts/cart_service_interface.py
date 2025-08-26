from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.orders.domain.contracts.cart_dtos import CartDTO


class CartServiceInterface(ABC):
    @abstractmethod
    def get_cart(self, user_id: UUID) -> CartDTO | None: ...

    @abstractmethod
    def clear_cart(self, user_id: UUID) -> None: ...
