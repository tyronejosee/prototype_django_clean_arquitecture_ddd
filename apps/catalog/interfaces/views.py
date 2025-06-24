"""Views for the catalog interfaces"""

from uuid import UUID

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.catalog.domain.models import Category, Product
from apps.catalog.application.services import CategoryService, ProductService
from apps.catalog.interfaces.serializers import (
    CategorySerializer,
    ProductSerializer,
)


class ProductListView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        service = ProductService()
        products = service.list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        service = ProductService()
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        product_entity = Product.from_dict(serializer.validated_data)  # type: ignore[arg-type]
        product = service.create_product(product_entity)
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED,
        )


class ProductDetailView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request, pk: UUID) -> Response:
        service = ProductService()
        product = service.get_product(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        service = ProductService()
        products = service.list_featured_products(limit=10)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CategoryListView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        service = CategoryService()
        categories = service.list_all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        service = CategoryService()
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        category_entity = Category.from_dict(serializer.validated_data)  # type: ignore[arg-type]
        category = service.create_category(category_entity)
        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryProductListView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request, category_id: UUID) -> Response:
        service = ProductService()
        products = service.list_products_by_category(category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
