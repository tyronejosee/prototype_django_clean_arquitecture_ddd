from decimal import Decimal
from typing import override
from uuid import UUID

from apps.payments.domain.strategies.payment_strategy import PaymentStrategy
from apps.payments.infrastructure.gateways.paypal_gateway import PaypalGateway


class PaypalStrategy(PaymentStrategy):
    def __init__(self) -> None:
        self.gateway = PaypalGateway()

    @override
    def initiate(
        self,
        order_id: UUID,
        amount: Decimal,
        payment_data: dict,
    ) -> dict:
        paypal_response = self.gateway.create_order(order_id, amount)

        approve_link = next(
            link["href"]
            for link in paypal_response["links"]
            if link["rel"] == "approve"
        )

        return {
            "payment_id": paypal_response["id"],
            "status": "initiated",
            "redirect_url": approve_link,
        }

    @override
    def complete(self, data: dict) -> dict:
        paypal_order_id = data["paypal_order_id"]
        capture_result = self.gateway.capture_order(paypal_order_id)

        return {
            "payment_id": capture_result["id"],
            "status": capture_result["status"],
        }
