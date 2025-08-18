from typing import ClassVar, cast
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.modules.catalog.domain.exceptions import BrandDomainError
from src.modules.catalog.presentation.providers import (
    get_create_brand_use_case,
    get_delete_brand_use_case,
    get_list_brands_use_case,
    get_list_products_by_brand_use_case,
    get_update_brand_use_case,
)
from src.modules.catalog.presentation.serializers.brand_serializer import BrandInputSerializer, BrandOutputSerializer
from src.modules.catalog.presentation.serializers.product_serializer import ProductSerializer
from src.modules.common.presentation.pagination import paginate_queryset


class BrandListCreateController(APIView):
    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request: Request) -> Response:
        use_case = get_list_brands_use_case()
        brands = use_case.execute()
        return paginate_queryset(request, brands, BrandOutputSerializer)

    def post(self, request: Request) -> Response:
        serializer = BrandInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        use_case = get_create_brand_use_case()

        try:
            brand = use_case.execute(validated_data)
            return Response(BrandOutputSerializer(brand).data, status=status.HTTP_201_CREATED)
        except BrandDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BrandDetailController(APIView):
    permission_classes: ClassVar[list] = [IsAdminUser]

    def put(self, request: Request, brand_id: UUID) -> Response:
        serializer = BrandInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)
        use_case = get_update_brand_use_case()

        try:
            brand = use_case.execute(brand_id, validated_data)
            return Response(BrandOutputSerializer(brand).data, status=status.HTTP_200_OK)
        except BrandDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, brand_id: UUID) -> Response:
        use_case = get_delete_brand_use_case()
        use_case.execute(brand_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandProductListController(APIView):
    permission_classes: ClassVar[list] = [AllowAny]

    def get(self, request: Request, brand_id: UUID) -> Response:
        use_case = get_list_products_by_brand_use_case()
        products = use_case.execute(brand_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
