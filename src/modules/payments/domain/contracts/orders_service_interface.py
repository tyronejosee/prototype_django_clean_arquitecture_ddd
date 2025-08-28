from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.payments.domain.contracts.orders_dtos import OrderDTO


class OrdersServiceInterface(ABC):
    @abstractmethod
    def get_order_by_id(self, order_id: UUID) -> OrderDTO | None: ...

    @abstractmethod
    def update_status(self, order_id: UUID, status: str) -> bool: ...
