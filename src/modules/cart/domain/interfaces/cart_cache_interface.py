from abc import ABC, abstractmethod

from src.modules.cart.domain.entities.cart import Cart


class CartCacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Cart: ...

    @abstractmethod
    def set(self, key: str, value: Cart, timeout: int | None = None) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...
