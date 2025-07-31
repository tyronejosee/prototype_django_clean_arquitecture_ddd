from decimal import Decimal
from uuid import UUID

import requests
from decouple import config
from django.conf import settings

from src.modules.payments.domain.exceptions import PaymentDomainError


class PaypalGateway:
    # Messages
    ACCESS_TOKEN_NOT_FOUND_MSG: str = "Access token not found."
    ACCESS_TOKEN_INVALID_MSG: str = "Access token is invalid."

    def __init__(self) -> None:
        self.is_debug = settings.DEBUG
        self.base_url = "https://api-m.sandbox.paypal.com" if self.is_debug else "https://api-m.paypal.com"
        self.client_id = config(
            "PAYPAL_CLIENT_ID",
            default="secret-client-id",
        )
        self.client_secret = config(
            "PAYPAL_CLIENT_SECRET",
            default="secret-client-secret",
        )
        self.return_url = config(
            "PAYPAL_RETURN_URL",
            default="http://localhost:8000/payments/success",
        )
        self.cancel_url = config(
            "PAYPAL_CANCEL_URL",
            default="http://localhost:8000/payments/cancel",
        )

        self.token = self._get_access_token()

    def _get_access_token(self) -> str:
        try:
            res = requests.post(
                f"{self.base_url}/v1/oauth2/token",
                auth=(self.client_id, self.client_secret),  # type: ignore[attr-defined]
                data={"grant_type": "client_credentials"},
                timeout=10,
            )
            data = res.json()
        except requests.RequestException as error:
            raise PaymentDomainError(self.ACCESS_TOKEN_NOT_FOUND_MSG) from error

        if "access_token" not in data:
            raise PaymentDomainError(self.ACCESS_TOKEN_INVALID_MSG)

        return data["access_token"]

    def create_order(self, order_id: UUID, amount: Decimal) -> dict:
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": str(order_id),
                    "amount": {"currency_code": "USD", "value": f"{amount:.2f}"},
                },
            ],
            "application_context": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.base_url}/v2/checkout/orders",
            json=payload,
            headers=headers,
            timeout=10,
        )
        return response.json()

    def capture_order(self, paypal_order_id: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.base_url}/v2/checkout/orders/{paypal_order_id}/capture",
            headers=headers,
            timeout=10,
        )
        return response.json()
