"""Views for the catalog presentation"""

from uuid import UUID

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from apps.catalog.application.use_cases.product_use_cases import (
    ListAllProductsUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    ListFeaturedProductsUseCase,
    ListProductsByCategoryUseCase,
)
from apps.catalog.application.use_cases.category_use_cases import (
    ListCategoriesUseCase,
    CreateCategoryUseCase,
)
from apps.catalog.infrastructure.repositories import (
    CategoryRepository,
    ProductRepository,
)
from apps.catalog.presentation.serializers import (
    CategorySerializer,
    ProductSerializer,
)


class ProductListCreateView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        use_case = ListAllProductsUseCase(ProductRepository())
        products = use_case.execute(dict(request.query_params))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateProductUseCase(ProductRepository())
            product = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request, product_id: UUID) -> Response:
        use_case = GetProductUseCase(ProductRepository())
        product = use_case.execute(product_id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        use_case = ListFeaturedProductsUseCase(ProductRepository())
        products = use_case.execute()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListCreateView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request) -> Response:
        use_case = ListCategoriesUseCase(CategoryRepository())
        categories = use_case.execute()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateCategoryUseCase(CategoryRepository())
            category = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryProductListView(APIView):
    permission_classes: list = [AllowAny]

    def get(self, request: Request, category_id: UUID) -> Response:
        use_case = ListProductsByCategoryUseCase(ProductRepository())
        products = use_case.execute(category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
