from abc import ABC, abstractmethod

from apps.payments.domain.entities.transaction import Transaction


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> None: ...
