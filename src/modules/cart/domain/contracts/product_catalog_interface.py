from abc import ABC, abstractmethod
from uuid import UUID


class ProductCatalogInterface(ABC):
    @abstractmethod
    def exists(self, product_id: UUID) -> bool: ...
