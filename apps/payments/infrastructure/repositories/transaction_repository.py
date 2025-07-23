from typing import override

from apps.payments.domain.entities.transaction import Transaction
from apps.payments.domain.interfaces.transaction_repository_interface import (
    TransactionRepositoryInterface,
)
from apps.payments.infrastructure.models.transaction_model import TransactionModel


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
