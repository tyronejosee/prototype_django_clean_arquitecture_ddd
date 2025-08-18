from typing import ClassVar, cast
from uuid import UUID

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.catalog.domain.exceptions import ProductDomainError
from src.modules.catalog.presentation.providers import (
    get_create_product_use_case,
    get_delete_product_use_case,
    get_get_product_use_case,
    get_list_featured_products_use_case,
    get_list_products_use_case,
    get_update_product_use_case,
)
from src.modules.catalog.presentation.schemas.product_schemas import (
    featured_products_schema,
    product_detail_schema,
    product_list_create_schema,
)
from src.modules.catalog.presentation.serializers.product_serializer import (
    ProductInputSerializer,
    ProductOutputSerializer,
)
from src.modules.catalog.presentation.throttles import (
    CreateProductRateThrottle,
    DeleteProductRateThrottle,
    GetProductRateThrottle,
    ListProductsRateThrottle,
    UpdateProductRateThrottle,
)
from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.common.presentation.pagination import paginate_queryset


@extend_schema_view(**product_list_create_schema)
class ProductListCreateController(BaseController):
    throttle_map: dict = {"GET": ListProductsRateThrottle, "POST": CreateProductRateThrottle}

    def get_permissions(self) -> list:
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request: Request) -> Response:
        use_case = get_list_products_use_case()
        products = use_case.execute(dict(request.query_params))
        return paginate_queryset(request, products, ProductOutputSerializer)

    def post(self, request: Request) -> Response:
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        use_case = get_create_product_use_case()

        try:
            product = use_case.execute(validated_data)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_201_CREATED)
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**product_detail_schema)
class ProductDetailController(BaseController):
    throttle_map: dict = {
        "GET": GetProductRateThrottle,
        "PUT": UpdateProductRateThrottle,
        "DELETE": DeleteProductRateThrottle,
    }

    def get_permissions(self) -> list:
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request: Request, product_id: UUID) -> Response:
        use_case = get_get_product_use_case()
        product = use_case.execute(product_id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductOutputSerializer(product)
        return Response(serializer.data)

    def put(self, request: Request, product_id: UUID) -> Response:
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        use_case = get_update_product_use_case()

        try:
            product = use_case.execute(product_id, validated_data)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_200_OK)
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, product_id: UUID) -> Response:
        use_case = get_delete_product_use_case()
        use_case.execute(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**featured_products_schema)
class FeaturedProductsController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]
    throttle_map: dict = {"GET": ListProductsRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_list_featured_products_use_case()
        products = use_case.execute()
        return paginate_queryset(request, products, ProductOutputSerializer)
