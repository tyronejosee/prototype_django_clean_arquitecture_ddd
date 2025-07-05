from decimal import Decimal

from apps.catalog.domain.entities.product import Product
from apps.catalog.domain.exceptions import ProductDomainError
from apps.catalog.domain.interfaces.product_service_interface import (
    ProductServiceInterface,
)


class ProductService(ProductServiceInterface):
    # Constants
    MIN_DISCOUNT: int = 0
    MIN_STOCK: int = 0
    MIN_RESTOCK_QUANTITY: int = 1
    MAX_DISCOUNT: int = 100
    FEATURED_MIN_STOCK: int = 10
    FEATURED_MIN_PRICE: Decimal = Decimal("100")

    # Messages
    INVALID_RESTOCK_MSG: str = "Quantity must be positive."
    INVALID_DISCOUNT_MSG: str = (
        "Discount percentage must be between {min_}% and {max_}%."
    )

    def is_active(self, product: Product) -> bool:
        return product.is_active and product.stock > self.MIN_STOCK

    def check_stock(self, product: Product, quantity: int) -> bool:
        return product.stock >= quantity

    def can_be_featured(self, product: Product) -> bool:
        return (
            product.is_active
            and product.stock > self.FEATURED_MIN_STOCK
            and product.price > self.FEATURED_MIN_PRICE
        )

    def restock(self, product: Product, quantity: int) -> None:
        if quantity < self.MIN_RESTOCK_QUANTITY:
            raise ProductDomainError(self.INVALID_RESTOCK_MSG)
        product.stock += quantity

    def apply_discount(self, product: Product, discount_percentage: float) -> Decimal:
        if not (self.MIN_DISCOUNT <= discount_percentage <= self.MAX_DISCOUNT):
            message = self.INVALID_DISCOUNT_MSG.format(
                min_=self.MIN_DISCOUNT,
                max_=self.MAX_DISCOUNT,
            )
            raise ProductDomainError(message)
        discount = Decimal(discount_percentage) / Decimal("100")
        return product.price * (Decimal("1") - discount)
