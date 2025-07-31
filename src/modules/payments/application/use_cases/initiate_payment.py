from uuid import UUID

from src.modules.orders.domain.exceptions import OrderNotFoundError
from src.modules.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from src.modules.payments.application.strategy_resolver import STRATEGY_MAP
from src.modules.payments.domain.exceptions import PaymentDomainError
from src.modules.payments.domain.factories.transaction_factory import TransactionFactory
from src.modules.payments.domain.interfaces.transaction_repository_interface import (
    TransactionRepositoryInterface,
)


class InitiatePaymentUseCase:
    # Messages
    ORDER_NOT_FOUND_MSG = "Order {order_id} not found."
    ORDER_PENDING_MSG = "Only pending orders can be paid."
    PAYMENT_METHOD_NOT_SUPPORTED_MSG = "Payment method {payment_method} is not supported."

    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        transaction_repo: TransactionRepositoryInterface,
    ) -> None:
        self.order_repo = order_repo
        self.transaction_repo = transaction_repo

    def execute(self, order_id: UUID, payment_method: str, email: str) -> dict:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(self.ORDER_NOT_FOUND_MSG.format(order_id=order_id))

        if order.status != "pending":
            raise PaymentDomainError(self.ORDER_PENDING_MSG)

        if payment_method not in STRATEGY_MAP:
            raise PaymentDomainError(
                self.PAYMENT_METHOD_NOT_SUPPORTED_MSG.format(
                    payment_method=payment_method,
                ),
            )

        strategy = STRATEGY_MAP[payment_method]
        result = strategy.initiate(order_id=order_id, amount=order.total())
        transaction = TransactionFactory.from_dict(
            {
                "external_id": result["external_id"],
                "order_id": order_id,
                "amount": order.total(),
                "status": result["status"],
                "payment_method": payment_method,
                "payer_email": email,
            },
        )
        self.transaction_repo.create(transaction)
        return result
