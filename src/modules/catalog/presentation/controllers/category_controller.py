from typing import ClassVar, cast
from uuid import UUID

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.catalog.domain.exceptions import CategoryDomainError, CategoryNotFoundError
from src.modules.catalog.presentation.providers import (
    get_create_category_use_case,
    get_delete_category_use_case,
    get_list_categories_use_case,
    get_list_products_by_category_use_case,
    get_update_category_use_case,
)
from src.modules.catalog.presentation.schemas.category_schema import (
    CATEGORY_DETAIL_SCHEMA,
    CATEGORY_LIST_CREATE_SCHEMA,
    CATEGORY_PRODUCT_LIST_SCHEMA,
)
from src.modules.catalog.presentation.serializers.category_serializer import (
    CategoryInputSerializer,
    CategoryOutputSerializer,
)
from src.modules.catalog.presentation.serializers.product_serializer import ProductOutputSerializer
from src.modules.catalog.presentation.throttles import (
    CreateCategoryRateThrottle,
    DeleteCategoryRateThrottle,
    ListCategoriesRateThrottle,
    ListProductsRateThrottle,
    UpdateCategoryRateThrottle,
)
from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.common.presentation.pagination import paginate_queryset


@extend_schema_view(**CATEGORY_LIST_CREATE_SCHEMA)
class CategoryListCreateController(BaseController):
    throttle_map: dict = {"GET": ListCategoriesRateThrottle, "POST": CreateCategoryRateThrottle}

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request: Request) -> Response:
        use_case = get_list_categories_use_case()
        categories = use_case.execute()
        return paginate_queryset(request, categories, CategoryOutputSerializer)

    def post(self, request: Request) -> Response:
        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        use_case = get_create_category_use_case()

        try:
            category = use_case.execute(validated_data)
            return Response(CategoryOutputSerializer(category).data, status=status.HTTP_201_CREATED)
        except CategoryDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**CATEGORY_DETAIL_SCHEMA)
class CategoryDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAdminUser]
    throttle_map: dict = {"PUT": UpdateCategoryRateThrottle, "DELETE": DeleteCategoryRateThrottle}

    def put(self, request: Request, category_id: UUID) -> Response:
        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        use_case = get_update_category_use_case()

        try:
            category = use_case.execute(category_id, validated_data)
            return Response(CategoryOutputSerializer(category).data, status=status.HTTP_200_OK)
        except CategoryDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, category_id: UUID) -> Response:
        use_case = get_delete_category_use_case()
        use_case.execute(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(**CATEGORY_PRODUCT_LIST_SCHEMA)
class CategoryProductListController(BaseController):
    permission_classes: ClassVar[list] = [AllowAny]
    throttle_map: dict = {"GET": ListProductsRateThrottle}

    def get(self, request: Request, category_id: UUID) -> Response:
        use_case = get_list_products_by_category_use_case()

        try:
            products = use_case.execute(category_id)
            return paginate_queryset(request, products, ProductOutputSerializer)
        except CategoryNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
