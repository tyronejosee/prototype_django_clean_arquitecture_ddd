"""Views for the catalog presentation"""

from uuid import UUID

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

from apps.catalog.domain.exceptions import (
    CategoryDomainException,
    ProductDomainException,
)
from apps.catalog.application.use_cases.product_use_cases import (
    ListAllProductsUseCase,
    CreateProductUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    ListFeaturedProductsUseCase,
    ListProductsByCategoryUseCase,
)
from apps.catalog.application.use_cases.category_use_cases import (
    ListCategoriesUseCase,
    CreateCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase,
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
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = ListAllProductsUseCase(ProductRepository())
        products = use_case.execute(dict(request.query_params))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = CreateProductUseCase(ProductRepository())
            product = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                ProductSerializer(product).data, status=status.HTTP_201_CREATED
            )
        except ProductDomainException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request, product_id: UUID) -> Response:
        use_case = GetProductUseCase(ProductRepository())
        product = use_case.execute(product_id)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request: Request, product_id: UUID) -> Response:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            use_case = UpdateProductUseCase(ProductRepository())
            product = use_case.execute(
                product_id,
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        except ProductDomainException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, product_id: UUID) -> Response:
        use_case = DeleteProductUseCase(ProductRepository())
        use_case.execute(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeaturedProductsView(APIView):
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = ListFeaturedProductsUseCase(ProductRepository())
        products = use_case.execute()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListCreateView(APIView):
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request) -> Response:
        use_case = ListCategoriesUseCase(CategoryRepository())
        categories = use_case.execute()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = CreateCategoryUseCase(CategoryRepository())
        try:
            category = use_case.execute(
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                CategorySerializer(category).data, status=status.HTTP_201_CREATED
            )
        except CategoryDomainException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def put(self, request: Request, category_id: UUID) -> Response:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = UpdateCategoryUseCase(CategoryRepository())
        try:
            category = use_case.execute(
                category_id,
                serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(
                CategorySerializer(category).data, status=status.HTTP_200_OK
            )
        except CategoryDomainException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, category_id: UUID) -> Response:
        use_case = DeleteCategoryUseCase(CategoryRepository())
        use_case.execute(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryProductListView(APIView):
    permission_classes: list = [AllowAny]  # ! TODO: Add roles

    def get(self, request: Request, category_id: UUID) -> Response:
        use_case = ListProductsByCategoryUseCase(ProductRepository())
        products = use_case.execute(category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
