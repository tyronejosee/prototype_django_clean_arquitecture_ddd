from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.payments.domain.contracts.product_dtos import ProductDTO


class CatalogServiceInterface(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: UUID) -> ProductDTO | None: ...

    @abstractmethod
    def update_product_stock_by_id(self, product_id: UUID, stock: int) -> bool: ...
