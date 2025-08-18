from abc import ABC, abstractmethod

from src.modules.catalog.domain.entities.brand import Brand


class BrandCacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> list[Brand]: ...

    @abstractmethod
    def set(self, key: str, value: list[Brand], timeout: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...
