from typing import override
from uuid import UUID

from src.modules.cart.domain.contracts.catalog_service_interface import CatalogServiceInterface
from src.modules.cart.domain.contracts.product_dtos import ProductDTO
from src.modules.catalog.infrastructure.models.product_model import ProductModel


class CatalogACL(CatalogServiceInterface):
    @override
    def get_product(self, product_id: UUID) -> ProductDTO | None:
        product = ProductModel.objects.filter(id=product_id, is_active=True).values("id", "price").first()
        if not product:
            return None
        return ProductDTO(id=product["id"], price=product["price"])
