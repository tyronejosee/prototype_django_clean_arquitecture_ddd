import logging
from decimal import Decimal
from uuid import UUID

import httpx
from django.conf import settings

from src.modules.payments.domain.exceptions import GatewayRequestError, GatewayTimeoutError, GatewayTokenError

logger = logging.getLogger(__name__)


class PaypalGateway:
    # Messages
    ACCESS_TOKEN_NOT_FOUND_MSG: str = "Access token not found."
    ACCESS_TOKEN_INVALID_MSG: str = "Access token is invalid."
    CREATE_ORDER_TIMEOUT_MSG: str = "Timeout while creating PayPal order"
    CREATE_ORDER_REQUEST_MSG: str = "Error creating PayPal order"
    CAPTURE_ORDER_TIMEOUT_MSG: str = "Timeout while capturing PayPal order '{order_id}'"
    CAPTURE_ORDER_REQUEST_MSG: str = "Error capturing PayPal order"
    INVALID_JSON_RESPONSE_MSG: str = "Invalid JSON response from PayPal during '{action}'"

    def __init__(self) -> None:
        self.is_debug = settings.DEBUG
        self.base_url = settings.PAYPAL_BASE_URL
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.return_url = settings.PAYPAL_RETURN_URL
        self.cancel_url = settings.PAYPAL_CANCEL_URL

        self._token: str | None = None
        self.client = httpx.Client(timeout=10)

    @property
    def token(self) -> str:
        if not self._token:
            self._token = self._get_access_token()
        return self._token

    def create_order(self, order_id: UUID, amount: Decimal) -> dict:
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": str(order_id),
                    "amount": {"currency_code": "USD", "value": f"{amount:.2f}"},
                }
            ],
            "application_context": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url,
            },
        }

        try:
            response = self.client.post(
                f"{self.base_url}/v2/checkout/orders",
                json=payload,
                headers=self._get_headers(),
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            logger.exception(self.CREATE_ORDER_TIMEOUT_MSG)
            raise GatewayTimeoutError(self.CREATE_ORDER_TIMEOUT_MSG) from error
        except httpx.RequestError as error:
            logger.exception(self.CREATE_ORDER_REQUEST_MSG)
            raise GatewayRequestError(self.CREATE_ORDER_REQUEST_MSG) from error

        return self._handle_response(response, "create_order")

    def capture_order(self, paypal_order_id: str) -> dict:
        try:
            response = self.client.post(
                f"{self.base_url}/v2/checkout/orders/{paypal_order_id}/capture",
                headers=self._get_headers(),
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            logger.exception(self.CAPTURE_ORDER_TIMEOUT_MSG.format(order_id=paypal_order_id))
            raise GatewayTimeoutError(self.CAPTURE_ORDER_TIMEOUT_MSG.format(order_id=paypal_order_id)) from error
        except httpx.RequestError as error:
            logger.exception(self.CAPTURE_ORDER_REQUEST_MSG)
            raise GatewayRequestError(self.CAPTURE_ORDER_REQUEST_MSG.format(error=error)) from error

        return self._handle_response(response, "capture_order")

    def _get_access_token(self) -> str:
        try:
            res = self.client.post(
                f"{self.base_url}/v1/oauth2/token",
                auth=(self.client_id, self.client_secret),
                data={"grant_type": "client_credentials"},
            )
            res.raise_for_status()
            data = res.json()
        except httpx.TimeoutException as error:
            logger.exception(self.ACCESS_TOKEN_NOT_FOUND_MSG)
            raise GatewayTimeoutError(self.ACCESS_TOKEN_NOT_FOUND_MSG) from error
        except httpx.RequestError as error:
            logger.exception(self.ACCESS_TOKEN_INVALID_MSG)
            raise GatewayRequestError(self.ACCESS_TOKEN_NOT_FOUND_MSG) from error

        if "access_token" not in data:
            logger.error("%s: %s", self.ACCESS_TOKEN_INVALID_MSG, data)
            raise GatewayTokenError(self.ACCESS_TOKEN_INVALID_MSG)

        return data["access_token"]

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def _handle_response(self, response: httpx.Response, action: str) -> dict:
        try:
            data = response.json()
        except ValueError as error:
            logger.exception(self.INVALID_JSON_RESPONSE_MSG.format(action=action))
            raise GatewayTokenError(self.INVALID_JSON_RESPONSE_MSG.format(action=action)) from error

        logger.info(
            "PayPal %s response: status=%s, debug_id=%s",
            action,
            response.status_code,
            response.headers.get("Paypal-Debug-Id"),
        )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": data,
        }
