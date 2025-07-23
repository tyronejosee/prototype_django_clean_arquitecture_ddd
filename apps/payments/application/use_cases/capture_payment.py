from apps.payments.domain.exceptions import PaymentDomainError
from apps.payments.infrastructure.strategies.paypal_strategy import PaypalStrategy


class CapturePaymentUseCase:
    def __init__(self) -> None:
        self.strategy = PaypalStrategy()

    def execute(self, payment_data: dict) -> dict:
        try:
            # ! TODO: Add persistence logic for completed transactions
            return self.strategy.complete(payment_data)
        except Exception as error:
            raise PaymentDomainError(str(error)) from error
