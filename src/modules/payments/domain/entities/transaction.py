from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Transaction:
    id: UUID
    external_id: str
    order_id: UUID
    amount: Decimal
    status: str
    payment_method: str
    payer_email: str | None = None
    created_at: datetime | None = None
