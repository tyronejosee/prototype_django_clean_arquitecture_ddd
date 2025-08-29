from functools import lru_cache

from src.modules.payments.application.use_cases.capture_payment import CapturePaymentUseCase
from src.modules.payments.application.use_cases.initiate_payment import InitiatePaymentUseCase
from src.modules.payments.infrastructure.acls.catalog_acl import CatalogACL
from src.modules.payments.infrastructure.acls.orders_acl import OrdersACL
from src.modules.payments.infrastructure.repositories.transaction_repository import TransactionRepository


@lru_cache
def get_orders_service() -> OrdersACL:
    return OrdersACL()


@lru_cache
def get_catalog_service() -> CatalogACL:
    return CatalogACL()


@lru_cache
def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()


def get_initiate_payment_use_case() -> InitiatePaymentUseCase:
    return InitiatePaymentUseCase(
        transaction_repo=get_transaction_repository(),
        orders_service=get_orders_service(),
    )


def get_capture_payment_use_case() -> CapturePaymentUseCase:
    return CapturePaymentUseCase(
        transaction_repo=get_transaction_repository(),
        orders_service=get_orders_service(),
        catalog_service=get_catalog_service(),
    )
