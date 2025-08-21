from typing import override

from django.core.cache import cache

from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.interfaces.product_cache_interface import ProductCacheInterface


class ProductCacheService(ProductCacheInterface):
    def __init__(self, default_ttl: int = 300) -> None:
        self.default_ttl = default_ttl

    @override
    def get(self, key: str) -> list[Product]:
        return cache.get(key)

    @override
    def set(self, key: str, value, timeout: int | None = None) -> None:
        actual_timeout = timeout or self.default_ttl
        cache.set(key, value, timeout=actual_timeout)

    @override
    def delete(self, key: str) -> None:
        cache.delete(key)
