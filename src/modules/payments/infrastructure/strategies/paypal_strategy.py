import logging
from decimal import Decimal
from typing import override
from uuid import UUID

from src.modules.payments.domain.strategies.payment_strategy import PaymentStrategy
from src.modules.payments.infrastructure.gateways.paypal_gateway import PaypalGateway

logger = logging.getLogger(__name__)


class PaypalStrategy(PaymentStrategy):
    STATUS_MAP = {
        "CREATED": "created",
        "APPROVED": "approved",
        "COMPLETED": "completed",
        "VOIDED": "voided",
    }

    def __init__(self) -> None:
        self.gateway = PaypalGateway()

    @override
    def initiate(self, order_id: UUID, amount: Decimal) -> dict:
        paypal_response = self.gateway.create_order(order_id, amount)

        external_id = paypal_response["body"].get("id")
        status = self.STATUS_MAP.get(paypal_response["body"].get("status"), "unknown")
        approve_link = next(
            (link["href"] for link in paypal_response["body"]["links"] if link["rel"] == "approve"),
            None,
        )

        return {
            "external_id": external_id,
            "status": status,
            "redirect_url": approve_link,
            "details": {"order_id": str(order_id), "amount": str(amount)},
        }

    @override
    def complete(self, external_id: str) -> dict:
        capture_result = self.gateway.capture_order(external_id)
        capture_body = capture_result["body"]

        return {
            "external_id": capture_body["id"],
            "status": self.STATUS_MAP.get(capture_body.get("status"), "unknown"),
            "details": capture_body,
        }
