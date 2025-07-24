from abc import ABC, abstractmethod
from uuid import UUID

from apps.payments.domain.entities.transaction import Transaction


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> None: ...

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Transaction | None: ...

    @abstractmethod
    def update_status(self, transaction_id: UUID, status: str) -> None: ...
