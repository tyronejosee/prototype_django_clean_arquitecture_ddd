from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.catalog.domain.entities.brand import Brand


class BrandRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, brand_id: UUID) -> Brand | None: ...

    @abstractmethod
    def list_all(self) -> list[Brand]: ...

    @abstractmethod
    def create(self, brand: Brand) -> Brand: ...

    @abstractmethod
    def update(self, brand_id: UUID, brand: Brand) -> Brand: ...

    @abstractmethod
    def delete(self, brand_id: UUID) -> None: ...

    @abstractmethod
    def exists_by_name(self, name: str) -> bool: ...
