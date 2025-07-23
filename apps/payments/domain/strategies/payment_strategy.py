from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class PaymentStrategy(ABC):
    @abstractmethod
    def initiate(self, order_id: UUID, amount: Decimal, payment_data: dict) -> dict: ...

    @abstractmethod
    def complete(self, data: dict) -> dict: ...
