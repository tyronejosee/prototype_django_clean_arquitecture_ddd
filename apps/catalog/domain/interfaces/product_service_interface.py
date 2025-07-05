from abc import ABC, abstractmethod
from decimal import Decimal

from apps.catalog.domain.entities.product import Product


class ProductServiceInterface(ABC):
    @abstractmethod
    def is_active(self, product: Product) -> bool: ...

    @abstractmethod
    def check_stock(self, product: Product, quantity: int) -> bool: ...

    @abstractmethod
    def can_be_featured(self, product: Product) -> bool: ...

    @abstractmethod
    def restock(self, product: Product, quantity: int) -> None: ...

    @abstractmethod
    def apply_discount(
        self,
        product: Product,
        discount_percentage: float,
    ) -> Decimal: ...
