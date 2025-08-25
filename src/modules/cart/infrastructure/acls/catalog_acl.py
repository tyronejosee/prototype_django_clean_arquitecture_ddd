from typing import override
from uuid import UUID

from src.modules.cart.domain.contracts.product_catalog_interface import ProductCatalogInterface
from src.modules.catalog.infrastructure.models.product_model import ProductModel


class CatalogACL(ProductCatalogInterface):
    @override
    def exists(self, product_id: UUID) -> bool:
        return ProductModel.objects.filter(id=product_id, is_active=True).exists()
