from apps.payments.domain.strategies.payment_strategy import PaymentStrategy
from apps.payments.infrastructure.strategies.paypal_strategy import PaypalStrategy

STRATEGY_MAP: dict[str, PaymentStrategy] = {
    "paypal": PaypalStrategy(),
}
