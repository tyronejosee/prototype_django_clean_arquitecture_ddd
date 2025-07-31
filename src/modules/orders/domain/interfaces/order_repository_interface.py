from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.orders.domain.entities.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def create(self, order: Order) -> Order: ...

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order: ...

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[Order]: ...

    @abstractmethod
    def update(self, order: Order) -> Order: ...

    @abstractmethod
    def cancel(self, order_id: UUID) -> Order: ...

    @abstractmethod
    def update_status(self, order_id: UUID, status: str) -> None: ...
