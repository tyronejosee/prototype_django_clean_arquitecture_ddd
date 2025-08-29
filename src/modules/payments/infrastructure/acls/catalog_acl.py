from typing import override
from uuid import UUID

from src.modules.catalog.infrastructure.models.product_model import ProductModel
from src.modules.payments.domain.contracts.catalog_service_interface import CatalogServiceInterface
from src.modules.payments.domain.contracts.product_dtos import ProductDTO


class CatalogACL(CatalogServiceInterface):
    @override
    def get_product_by_id(self, product_id: UUID) -> ProductDTO | None:
        product = ProductModel.objects.filter(id=product_id, is_active=True).values("id", "price", "stock").first()
        if not product:
            return None
        return ProductDTO(id=product["id"], price=product["price"], stock=product["stock"])

    @override
    def update_product_stock_by_id(self, product_id: UUID, stock: int) -> bool:
        try:
            product = ProductModel.objects.get(id=product_id)
            product.stock = stock
            product.save()
            return True
        except ProductModel.DoesNotExist:
            return False
