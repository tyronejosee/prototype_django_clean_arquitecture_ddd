"""Services for the catalog domain"""

from decimal import Decimal

from apps.catalog.domain.entities import Product
from apps.catalog.domain.exceptions import ProductDomainError


def is_product_active(product: Product) -> bool:
    return product.is_active and product.stock > 0


def check_product_in_stock(product: Product, quantity: int) -> bool:
    return product.stock >= quantity


def can_be_featured(product: Product) -> bool:
    return product.is_active and product.stock > 10 and product.price > 100


def restock_product(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise ProductDomainError("Quantity must be positive")
    product.stock += quantity


def apply_discount(product: Product, discount_percentage: float) -> Decimal:
    if discount_percentage < 0 or discount_percentage > 100:
        raise ProductDomainError("Discount percentage must be between 0 and 100")
    discount = Decimal(discount_percentage) / Decimal("100")
    return product.price * (Decimal("1") - discount)
