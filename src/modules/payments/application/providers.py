from functools import lru_cache

from src.modules.catalog.infrastructure.repositories.product_repository import (
    ProductRepository,
)
from src.modules.orders.infrastructure.repositories.order_repository import (
    OrderRepository,
)
from src.modules.payments.application.use_cases.capture_payment import (
    CapturePaymentUseCase,
)
from src.modules.payments.application.use_cases.initiate_payment import (
    InitiatePaymentUseCase,
)
from src.modules.payments.infrastructure.repositories.transaction_repository import (
    TransactionRepository,
)


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepository()


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository()


@lru_cache
def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()


def get_initiate_payment_use_case() -> InitiatePaymentUseCase:
    return InitiatePaymentUseCase(
        order_repo=get_order_repository(),
        transaction_repo=get_transaction_repository(),
    )


def get_capture_payment_use_case() -> CapturePaymentUseCase:
    return CapturePaymentUseCase(
        transaction_repo=get_transaction_repository(),
        order_repo=get_order_repository(),
        product_repo=get_product_repository(),
    )
