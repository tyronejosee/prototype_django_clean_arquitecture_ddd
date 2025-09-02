from typing import ClassVar, cast
from uuid import UUID

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.catalog.domain.exceptions import ProductDomainError, ProductNotFoundError
from src.modules.catalog.presentation.providers import (
    get_create_product_use_case,
    get_delete_product_use_case,
    get_get_product_use_case,
    get_list_featured_products_use_case,
    get_list_products_use_case,
    get_update_product_use_case,
)
from src.modules.catalog.presentation.schemas.product_schema import (
    FEATURED_PRODUCTS_SCHEMA,
    PRODUCT_DETAIL_SCHEMA,
    PRODUCT_LIST_CREATE_SCHEMA,
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


@extend_schema_view(**PRODUCT_LIST_CREATE_SCHEMA)
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
        validated_data = cast("dict", serializer.validated_data)
        image_file = validated_data.pop("image")
        use_case = get_create_product_use_case()

        try:
            product = use_case.execute(validated_data, image_file)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_201_CREATED)
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**PRODUCT_DETAIL_SCHEMA)
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

        try:
            product = use_case.execute(product_id)
            return Response(ProductOutputSerializer(product).data)
        except ProductNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, product_id: UUID) -> Response:
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        image_file = validated_data.pop("image", None)
        use_case = get_update_product_use_case()

        try:
            product = use_case.execute(product_id, validated_data, image_file)
            return Response(ProductOutputSerializer(product).data, status=status.HTTP_200_OK)
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProductNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, product_id: UUID) -> Response:
        use_case = get_delete_product_use_case()
        use_case.execute(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**FEATURED_PRODUCTS_SCHEMA)
class FeaturedProductsController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]
    throttle_map: dict = {"GET": ListProductsRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_list_featured_products_use_case()
        products = use_case.execute()
        return paginate_queryset(request, products, ProductOutputSerializer)
