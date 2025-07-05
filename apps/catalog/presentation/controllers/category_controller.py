from typing import ClassVar
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.application.providers import (
    get_create_category_use_case,
    get_delete_category_use_case,
    get_list_categories_use_case,
    get_list_products_by_category_use_case,
    get_update_category_use_case,
)
from apps.catalog.domain.exceptions import CategoryDomainError
from apps.catalog.presentation.serializers.category_serializer import CategorySerializer
from apps.catalog.presentation.serializers.product_serializer import ProductSerializer


class CategoryListCreateController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = get_list_categories_use_case()
        categories = use_case.execute()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_create_category_use_case()
            category = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED,
            )
        except CategoryDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def put(self, request: Request, category_id: UUID) -> Response:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = get_update_category_use_case()
        try:
            category = use_case.execute(
                category_id,
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_200_OK,
            )
        except CategoryDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, category_id: UUID) -> Response:
        use_case = get_delete_category_use_case()
        use_case.execute(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryProductListController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request, category_id: UUID) -> Response:
        use_case = get_list_products_by_category_use_case()
        products = use_case.execute(category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
