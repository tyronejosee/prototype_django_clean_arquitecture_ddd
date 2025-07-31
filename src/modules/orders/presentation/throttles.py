from rest_framework.throttling import UserRateThrottle


class CreateOrderRateThrottle(UserRateThrottle):
    scope: str = "create_order"


class ListOrdersRateThrottle(UserRateThrottle):
    scope: str = "list_orders"


class RetrieveOrderRateThrottle(UserRateThrottle):
    scope: str = "retrieve_order"


class CancelOrderRateThrottle(UserRateThrottle):
    scope: str = "cancel_order"
