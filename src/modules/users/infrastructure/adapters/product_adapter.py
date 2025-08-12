from uuid import UUID

from src.modules.catalog.infrastructure.models.product_model import ProductModel
from src.modules.users.domain.ports.product_port import ProductPort


class ProductAdapter(ProductPort):
    def exists(self, product_id: UUID) -> bool:
        return ProductModel.objects.filter(pk=product_id, is_active=True).exists()
