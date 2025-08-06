from typing import override

from django.core.cache import cache

from src.modules.cart.domain.entities.cart import Cart
from src.modules.cart.domain.interfaces.cart_cache_interface import CartCacheInterface


class CartCacheService(CartCacheInterface):
    def __init__(self, default_ttl: int = 300) -> None:
        self.default_ttl = default_ttl

    @override
    def get(self, key: str) -> Cart:
        return cache.get(key)

    @override
    def set(self, key: str, value, timeout: int | None = None) -> None:
        actual_timeout = timeout or self.default_ttl
        cache.set(key, value, timeout=actual_timeout)

    @override
    def delete(self, key: str) -> None:
        cache.delete(key)
