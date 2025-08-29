from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.cart.domain.contracts.product_dtos import ProductDTO


class CatalogServiceInterface(ABC):
    @abstractmethod
    def get_product(self, product_id: UUID) -> ProductDTO | None: ...
