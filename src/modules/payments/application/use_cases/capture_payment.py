from modules.catalog.domain.interfaces.product_repository_interface import (
    ProductRepositoryInterface,
)
from modules.orders.domain.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from modules.payments.domain.exceptions import PaymentDomainError
from modules.payments.domain.interfaces.transaction_repository_interface import (
    TransactionRepositoryInterface,
)
from modules.payments.infrastructure.strategies.paypal_strategy import PaypalStrategy


class CapturePaymentUseCase:
    # Messages
    TRANSACTION_NOT_FOUND_MSG = "Transaction {external_id} not found."
    PRODUCT_NOT_FOUND_MSG = "Product {product_id} not found."
    PRODUCT_STOCK_NOT_ENOUGH_MSG = "Not enough stock for product {product_id}."

    def __init__(
        self,
        transaction_repo: TransactionRepositoryInterface,
        order_repo: OrderRepositoryInterface,
        product_repo: ProductRepositoryInterface,
    ) -> None:
        self.strategy = PaypalStrategy()
        self.transaction_repo = transaction_repo
        self.order_repo = order_repo
        self.product_repo = product_repo

    def execute(self, payment_data: dict) -> dict:
        try:
            external_id: str = payment_data["external_id"]
            trx = self.transaction_repo.get_by_external_id(external_id)

            if not trx:
                raise PaymentDomainError(
                    self.TRANSACTION_NOT_FOUND_MSG.format(external_id=external_id),
                )

            result = self.strategy.complete(payment_data)
            self.transaction_repo.update_status(
                transaction_id=trx.order_id,
                status="paid",
            )

            if self.order_repo and self.product_repo and result["status"].lower() == "completed":
                order = self.order_repo.get_by_id(trx.order_id)
                for item in order.items:
                    product = self.product_repo.get_by_id(item.product_id)
                    if not product:
                        raise PaymentDomainError(
                            self.PRODUCT_NOT_FOUND_MSG.format(
                                product_id=item.product_id,
                            ),
                        )
                    if product.stock < item.quantity:
                        raise PaymentDomainError(
                            self.PRODUCT_STOCK_NOT_ENOUGH_MSG.format(
                                product_id=item.product_id,
                            ),
                        )
                    product.stock -= item.quantity
                    self.product_repo.update(product.id, product)
                self.order_repo.update_status(order_id=trx.order_id, status="paid")

            return result
        except Exception as error:
            raise PaymentDomainError(str(error)) from error
