from datetime import UTC, datetime
from uuid import uuid4

from modules.payments.domain.entities.transaction import Transaction


class TransactionFactory:
    @staticmethod
    def from_dict(data) -> Transaction:
        return Transaction(
            id=data.get("id", uuid4()),
            external_id=data["external_id"],
            order_id=data["order_id"],
            amount=data["amount"],
            status=data["status"],
            payment_method=data["payment_method"],
            payer_email=data.get("payer_email", None),
            created_at=data.get("created_at", datetime.now(UTC)),
        )

    @staticmethod
    def from_model(data) -> Transaction:
        return Transaction(
            id=data.id,
            external_id=data.external_id,
            order_id=data.order_id,
            amount=data.amount,
            status=data.status,
            payment_method=data.payment_method,
            payer_email=data.payer_email,
            created_at=data.created_at,
        )
