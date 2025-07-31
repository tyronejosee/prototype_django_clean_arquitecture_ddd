from typing import override
from uuid import UUID

from modules.payments.domain.entities.transaction import Transaction
from modules.payments.domain.factories.transaction_factory import TransactionFactory
from modules.payments.domain.interfaces.transaction_repository_interface import (
    TransactionRepositoryInterface,
)
from modules.payments.infrastructure.models.transaction_model import TransactionModel


class TransactionRepository(TransactionRepositoryInterface):
    @override
    def create(self, transaction: Transaction) -> None:
        TransactionModel.objects.create(
            external_id=transaction.external_id,
            order_id=transaction.order_id,
            amount=transaction.amount,
            status=transaction.status,
            payer_email=transaction.payer_email,
            payment_method=transaction.payment_method,
        )

    @override
    def get_by_external_id(self, external_id: str) -> Transaction | None:
        try:
            model = TransactionModel.objects.get(external_id=external_id)
        except TransactionModel.DoesNotExist:
            return None
        return TransactionFactory.from_model(model)

    @override
    def update_status(self, transaction_id: UUID, status: str) -> None:
        TransactionModel.objects.filter(id=transaction_id).update(status=status)
