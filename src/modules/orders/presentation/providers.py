from functools import lru_cache

from src.modules.marketing.domain.chains.discount_handler_chain import DiscountHandlerChain
from src.modules.orders.application.use_cases.cancel_order import CancelOrderUseCase
from src.modules.orders.application.use_cases.create_order import CreateOrderUseCase
from src.modules.orders.application.use_cases.get_order import GetOrderUseCase
from src.modules.orders.application.use_cases.list_orders import ListOrdersUseCase
from src.modules.orders.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from src.modules.orders.infrastructure.acls.cart_acl import CartACL
from src.modules.orders.infrastructure.acls.marketing_acl import MarketingACL
from src.modules.orders.infrastructure.repositories.order_repository import OrderRepository


@lru_cache
def get_order_repository() -> OrderRepository:
    return OrderRepository()


@lru_cache
def get_cart_service() -> CartACL:
    return CartACL()


@lru_cache
def get_marketing_service() -> MarketingACL:
    return MarketingACL(chain=DiscountHandlerChain())


def get_create_order_use_case() -> CreateOrderUseCase:
    return CreateOrderUseCase(
        order_repo=get_order_repository(),
        cart_service=get_cart_service(),
        marketing_service=get_marketing_service(),
    )


def get_get_order_use_case() -> GetOrderUseCase:
    return GetOrderUseCase(repo=get_order_repository())


def get_list_orders_use_case() -> ListOrdersUseCase:
    return ListOrdersUseCase(repo=get_order_repository())


def get_cancel_order_use_case() -> CancelOrderUseCase:
    return CancelOrderUseCase(repo=get_order_repository())


def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(repo=get_order_repository())
