from uuid import UUID

from src.modules.payments.application.strategy_resolver import STRATEGY_MAP
from src.modules.payments.domain.contracts.orders_service_interface import OrdersServiceInterface
from src.modules.payments.domain.exceptions import PaymentDomainError
from src.modules.payments.domain.factories.transaction_factory import TransactionFactory
from src.modules.payments.domain.interfaces.transaction_repository_interface import TransactionRepositoryInterface


class InitiatePaymentUseCase:
    # Messages
    ORDER_NOT_FOUND_MSG = "Order {order_id} not found."
    ONLY_PENDING_ORDER_MSG = "Only pending orders can be paid."
    PAYMENT_METHOD_NOT_SUPPORTED_MSG = "Payment method {payment_method} is not supported."

    def __init__(
        self,
        transaction_repo: TransactionRepositoryInterface,
        orders_service: OrdersServiceInterface,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.orders_service = orders_service

    def execute(self, order_id: UUID, payment_method: str, email: str) -> dict:
        order = self.orders_service.get_order_by_id(order_id)
        if not order:
            raise PaymentDomainError(self.ORDER_NOT_FOUND_MSG.format(order_id=order_id))

        if order.status != "pending":
            raise PaymentDomainError(self.ONLY_PENDING_ORDER_MSG)

        if payment_method not in STRATEGY_MAP:
            raise PaymentDomainError(self.PAYMENT_METHOD_NOT_SUPPORTED_MSG.format(payment_method=payment_method))

        strategy = STRATEGY_MAP[payment_method]
        result = strategy.initiate(order_id=order_id, amount=order.final_price)
        transaction = TransactionFactory.from_dict(
            {
                "external_id": result["external_id"],
                "order_id": order_id,
                "amount": order.final_price,
                "status": result["status"],
                "payment_method": payment_method,
                "payer_email": email,
            },
        )
        self.transaction_repo.create(transaction)
        return result
