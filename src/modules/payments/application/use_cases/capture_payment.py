from src.modules.payments.application.strategy_resolver import STRATEGY_MAP
from src.modules.payments.domain.contracts.catalog_service_interface import CatalogServiceInterface
from src.modules.payments.domain.contracts.orders_service_interface import OrdersServiceInterface
from src.modules.payments.domain.exceptions import PaymentDomainError
from src.modules.payments.domain.interfaces.transaction_repository_interface import TransactionRepositoryInterface


class CapturePaymentUseCase:
    # Messages
    PAYMENT_METHOD_NOT_SUPPORTED_MSG = "Payment method {payment_method} is not supported."
    TRANSACTION_NOT_FOUND_MSG = "Transaction {external_id} not found."
    PRODUCT_NOT_FOUND_MSG = "Product {product_id} not found."
    PRODUCT_STOCK_NOT_ENOUGH_MSG = "Not enough stock for product {product_id}."
    ORDER_NOT_FOUND_MSG = "Order {order_id} not found."

    def __init__(
        self,
        transaction_repo: TransactionRepositoryInterface,
        orders_service: OrdersServiceInterface,
        catalog_service: CatalogServiceInterface,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.orders_service = orders_service
        self.catalog_service = catalog_service

    def execute(self, external_id: str, payment_method: str = "paypal") -> dict:
        try:
            trx = self.transaction_repo.get_by_external_id(external_id)

            if not trx:
                raise PaymentDomainError(self.TRANSACTION_NOT_FOUND_MSG.format(external_id=external_id))

            if payment_method not in STRATEGY_MAP:
                raise PaymentDomainError(self.PAYMENT_METHOD_NOT_SUPPORTED_MSG.format(payment_method=payment_method))

            strategy = STRATEGY_MAP[payment_method]
            result = strategy.complete(external_id)
            self.transaction_repo.update_status(transaction_id=trx.order_id, status="paid")

            if self.orders_service and self.catalog_service and result["status"].lower() == "completed":
                order = self.orders_service.get_order_by_id(trx.order_id)
                if not order:
                    raise PaymentDomainError(self.ORDER_NOT_FOUND_MSG.format(order_id=trx.order_id))

                for item in order.items:
                    product = self.catalog_service.get_product_by_id(item.product_id)

                    if not product:
                        raise PaymentDomainError(self.PRODUCT_NOT_FOUND_MSG.format(product_id=item.product_id))

                    if product.stock < item.quantity:
                        raise PaymentDomainError(self.PRODUCT_STOCK_NOT_ENOUGH_MSG.format(product_id=item.product_id))

                    new_stock = product.stock - item.quantity
                    self.catalog_service.update_product_stock_by_id(product_id=product.id, stock=new_stock)

                self.orders_service.update_status(order_id=trx.order_id, status="paid")

            return result
        except Exception as error:
            raise PaymentDomainError(str(error)) from error
