from typing import ClassVar
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.application.providers import (
    get_create_product_use_case,
    get_delete_product_use_case,
    get_get_product_use_case,
    get_list_featured_products_use_case,
    get_list_products_use_case,
    get_update_product_use_case,
)
from apps.catalog.domain.exceptions import ProductDomainError
from apps.catalog.presentation.serializers.product_serializer import ProductSerializer


class ProductListCreateController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = get_list_products_use_case()
        products = use_case.execute(dict(request.query_params))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_create_product_use_case()
            product = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED,
            )
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request, product_id: UUID) -> Response:
        use_case = get_get_product_use_case()
        product = use_case.execute(product_id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request: Request, product_id: UUID) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = get_update_product_use_case()
            product = use_case.execute(
                product_id,
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        except ProductDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, product_id: UUID) -> Response:
        use_case = get_delete_product_use_case()
        use_case.execute(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeaturedProductsController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = get_list_featured_products_use_case()
        products = use_case.execute()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
