from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID


class PaymentStrategy(ABC):
    @abstractmethod
    def initiate(self, order_id: UUID, amount: Decimal) -> dict: ...

    @abstractmethod
    def complete(self, external_id: str) -> dict: ...
