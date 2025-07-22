from functools import lru_cache

from apps.cart.infrastructure.repositories.cart_repository import CartRepository
from apps.catalog.infrastructure.repositories.product_repository import (
    ProductRepository,
)
from apps.orders.infrastructure.repositories.order_repository import OrderRepository

from .use_cases.cancel_order import CancelOrderUseCase
from .use_cases.create_order import CreateOrderUseCase
from .use_cases.get_order import GetOrderUseCase
from .use_cases.list_orders import ListOrdersUseCase
from .use_cases.update_order_status import UpdateOrderStatusUseCase


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepository()


@lru_cache
def get_cart_repository() -> CartRepository:
    return CartRepository()


@lru_cache
def get_product_repository() -> ProductRepository:
    return ProductRepository()


def get_create_order_use_case() -> CreateOrderUseCase:
    return CreateOrderUseCase(
        order_repo=get_order_repository(),
        cart_repo=get_cart_repository(),
        product_repo=get_product_repository(),
    )


def get_get_order_use_case() -> GetOrderUseCase:
    return GetOrderUseCase(repo=get_order_repository())


def get_list_orders_use_case() -> ListOrdersUseCase:
    return ListOrdersUseCase(repo=get_order_repository())


def get_cancel_order_use_case() -> CancelOrderUseCase:
    return CancelOrderUseCase(repo=get_order_repository())


def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(repo=get_order_repository())
