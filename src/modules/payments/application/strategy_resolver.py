from src.modules.payments.domain.strategies.payment_strategy import PaymentStrategy
from src.modules.payments.infrastructure.strategies.paypal_strategy import (
    PaypalStrategy,
)

STRATEGY_MAP: dict[str, PaymentStrategy] = {
    "paypal": PaypalStrategy(),
}
