from decimal import Decimal
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from src.modules.catalog.domain.entities.brand import Brand
from src.modules.catalog.domain.entities.category import Category
from src.modules.catalog.domain.entities.product import Product
from src.modules.catalog.domain.exceptions import BrandNotFoundError, CategoryNotFoundError, ProductNotFoundError
from src.modules.catalog.domain.value_objects.brand_name import BrandName
from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.currency import Currency
from src.modules.catalog.domain.value_objects.sku import SKU
from src.modules.catalog.domain.value_objects.slug import Slug
from src.modules.catalog.domain.value_objects.weight_unit import WeightUnit
from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from src.modules.catalog.infrastructure.models.product_model import ProductModel
from src.modules.catalog.infrastructure.repositories.brand_repository import BrandRepository
from src.modules.catalog.infrastructure.repositories.category_repository import CategoryRepository
from src.modules.catalog.infrastructure.repositories.product_repository import ProductRepository
from tests.unit.catalog.domain.test_entities import build_valid_brand, build_valid_category, build_valid_product


@pytest.mark.django_db()
class TestBrandRepository:
    def test_brand_repository_create_and_retrieve(self) -> None:
        # Given: a valid Brand entity to persist
        repo = BrandRepository()
        brand = build_valid_brand()

        # When: creating the brand via repository
        saved = repo.create(brand)

        # Then: the saved brand should match the input
        assert isinstance(saved, Brand)
        assert saved.id == brand.id
        assert saved.name == brand.name
        assert saved.slug == brand.slug

    def test_brand_repository_get_by_id_success(self) -> None:
        # Given: a brand saved in the DB
        model = BrandModel.objects.create(name="Adidas", slug="adidas", is_active=True)
        repo = BrandRepository()

        # When: fetching by id
        brand = repo.get_by_id(model.id)

        # Then: the brand is returned correctly
        assert isinstance(brand, Brand)
        assert brand.id == model.id
        assert brand.name == model.name

    def test_brand_repository_get_by_id_not_found(self) -> None:
        # Given: no brand exists with given ID
        repo = BrandRepository()
        fake_id = uuid4()

        # When & Then: fetching should raise BrandNotFoundError
        with pytest.raises(BrandNotFoundError):
            repo.get_by_id(fake_id)

    def test_brand_repository_list_all_filters_active_only(self) -> None:
        # Given: some active and inactive brands
        BrandModel.objects.create(name="ActiveBrand", slug="active", is_active=True)
        BrandModel.objects.create(name="InactiveBrand", slug="inactive", is_active=False)
        repo = BrandRepository()

        # When: listing all
        results = repo.list_all()

        # Then: only active brands are returned
        names = [b.name for b in results]
        assert "ActiveBrand" in names
        assert "InactiveBrand" not in names

    def test_brand_repository_update_success(self) -> None:
        # Given: a saved brand
        model = BrandModel.objects.create(name="OldName", slug="oldslug", is_active=True)
        repo = BrandRepository()
        updated_brand = build_valid_brand(name=BrandName("NewName"), slug=Slug("newslug"), is_active=False)

        # When: updating via repository
        result = repo.update(model.id, updated_brand)

        # Then: the changes are persisted
        assert result.name == "NewName"
        assert result.slug == "newslug"
        assert result.is_active is False

    def test_brand_repository_update_not_found(self) -> None:
        # Given: a non-existent brand id
        repo = BrandRepository()
        fake_id = uuid4()
        # brand = Brand(id=fake_id, name="Name", slug="slug", is_active=True)
        brand = build_valid_brand(id=fake_id, name="Name", slug="slug", is_active=True)

        # When & Then: updating should raise BrandNotFoundError
        with pytest.raises(BrandNotFoundError):
            repo.update(fake_id, brand)

    def test_brand_repository_delete_success(self) -> None:
        # Given: a saved brand
        model = BrandModel.objects.create(name="ToDelete", slug="delete", is_active=True)
        repo = BrandRepository()

        # When: deleting via repository
        repo.delete(model.id)
        model.refresh_from_db()

        # Then: brand should be marked inactive
        assert model.is_active is False

    def test_brand_repository_delete_not_found(self) -> None:
        # Given: a non-existent brand id
        repo = BrandRepository()
        fake_id = uuid4()

        # When & Then: deleting should raise BrandNotFoundError
        with pytest.raises(BrandNotFoundError):
            repo.delete(fake_id)

    def test_brand_repository_exists_methods(self) -> None:
        # Given: a saved brand
        model = BrandModel.objects.create(name="Existing", slug="exist", is_active=True)
        repo = BrandRepository()

        # When & Then: exists should return True for existing active brand
        assert repo.exists(model.id) is True
        assert repo.exists_by_name("Existing") is True

        # Inactive brand should not exist
        model.is_active = False
        model.save()
        assert repo.exists(model.id) is False
        assert repo.exists_by_name("Existing") is False


@pytest.mark.django_db()
class TestCategoryRepository:
    def test_category_repository_create_and_retrieve(self) -> None:
        # Given: a valid Category entity
        repo = CategoryRepository()
        category = build_valid_category()

        # When: creating the category via repository
        saved = repo.create(category)

        # Then: the saved category should match input
        assert isinstance(saved, Category)
        assert saved.id == category.id
        assert saved.name == category.name
        assert saved.slug == category.slug
        assert saved.description == category.description

    def test_category_repository_get_by_id_success(self) -> None:
        # Given: a category saved in DB
        model = CategoryModel.objects.create(name="Books", slug="books", description="All books", is_active=True)
        repo = CategoryRepository()

        # When: fetching by ID
        category = repo.get_by_id(model.id)

        # Then: the category is returned correctly
        assert isinstance(category, Category)
        assert category.id == model.id
        assert category.name == model.name

    def test_category_repository_get_by_id_not_found(self) -> None:
        # Given: no category exists with given ID
        repo = CategoryRepository()
        fake_id = uuid4()

        # When & Then: fetching should raise CategoryNotFoundError
        with pytest.raises(CategoryNotFoundError):
            repo.get_by_id(fake_id)

    def test_category_repository_list_all_filters_active_only(self) -> None:
        # Given: some active and inactive categories
        CategoryModel.objects.create(name="ActiveCat", slug="activecat", description="Active", is_active=True)
        CategoryModel.objects.create(name="InactiveCat", slug="inactivecat", description="Inactive", is_active=False)
        repo = CategoryRepository()

        # When: listing all
        results = repo.list_all()

        # Then: only active categories returned
        names = [c.name for c in results]
        assert "ActiveCat" in names
        assert "InactiveCat" not in names

    def test_category_repository_update_success(self) -> None:
        # Given: a saved category
        model = CategoryModel.objects.create(name="OldName", slug="oldslug", description="Old desc", is_active=True)
        repo = CategoryRepository()
        updated_category = build_valid_category(
            name=CategoryName("NewName"), slug=Slug("newslug"), description="New desc", is_active=False
        )

        # When: updating via repository
        result = repo.update(model.id, updated_category)

        # Then: changes are persisted
        assert result.name == "NewName"
        assert result.slug == "newslug"
        assert result.description == "New desc"
        assert result.is_active is False

    def test_category_repository_update_not_found(self) -> None:
        # Given: a non-existent category ID
        repo = CategoryRepository()
        fake_id = uuid4()
        category = build_valid_category(id=fake_id, name="Name", slug="slug", description="desc", is_active=True)

        # When & Then: updating should raise CategoryNotFoundError
        with pytest.raises(CategoryNotFoundError):
            repo.update(fake_id, category)

    def test_category_repository_delete_success(self) -> None:
        # Given: a saved category
        model = CategoryModel.objects.create(name="ToDelete", slug="delete", description="Delete me", is_active=True)
        repo = CategoryRepository()

        # When: deleting via repository
        repo.delete(model.id)
        model.refresh_from_db()

        # Then: category is marked inactive
        assert model.is_active is False

    def test_category_repository_delete_not_found(self) -> None:
        # Given: a non-existent category ID
        repo = CategoryRepository()
        fake_id = uuid4()

        # When & Then: deleting should raise CategoryNotFoundError
        with pytest.raises(CategoryNotFoundError):
            repo.delete(fake_id)

    def test_category_repository_exists_methods(self) -> None:
        # Given: a saved category
        model = CategoryModel.objects.create(name="ExistingCat", slug="existcat", description="desc", is_active=True)
        repo = CategoryRepository()

        # When & Then: exists should return True for active category
        assert repo.exists(model.id) is True
        assert repo.exists_by_name("ExistingCat") is True

        # Inactive category should return False
        model.is_active = False
        model.save()
        assert repo.exists(model.id) is False
        assert repo.exists_by_name("ExistingCat") is False


@pytest.mark.django_db()
class TestProductRepository:
    def test_product_repository_create_and_retrieve(self) -> None:
        # Given: a valid Product entity with minimal required fields
        repo = ProductRepository()
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        product = build_valid_product(brand_id=brand.id, category_id=category.id)
        image_file = SimpleUploadedFile("image.jpg", b"fake image content", content_type="image/jpeg")

        # When: creating the product
        saved = repo.create(product, image_file)  # type: ignore[arg-type]

        # Then: product is persisted correctly
        assert isinstance(saved, Product)
        assert saved.id == product.id
        assert saved.name == product.name
        assert saved.sku == product.sku

    def test_product_repository_get_by_id_success(self) -> None:
        # Given: a saved product
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        model = ProductModel.objects.create(
            name="Phone",
            slug="phone",
            description="Smartphone",
            sku="SKU999",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("500.00"),
            discount_price=Decimal("450.00"),
            currency="USD",
            stock=5,
            min_stock=1,
            warehouse_location="B2",
            image=b"",
            is_active=True,
            is_featured=False,
            weight=0.3,
            unit="kg",
        )
        repo = ProductRepository()

        # When: fetching by ID
        product = repo.get_by_id(model.id)

        # Then: product matches
        assert isinstance(product, Product)
        assert product.id == model.id
        assert product.name == model.name

    def test_product_repository_get_by_id_not_found(self) -> None:
        # Given: non-existent product ID
        repo = ProductRepository()
        fake_id = uuid4()

        # When & Then: should raise ProductNotFoundError
        with pytest.raises(ProductNotFoundError):
            repo.get_by_id(fake_id)

    def test_product_repository_update_success(self) -> None:
        # Given: a saved product
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        model = ProductModel.objects.create(
            name="OldProduct",
            slug="oldproduct",
            description="Old",
            sku="SKUOLD",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("100.00"),
            discount_price=Decimal("90.00"),
            currency="USD",
            stock=2,
            min_stock=1,
            warehouse_location="C3",
            image=SimpleUploadedFile("old-image.jpg", b"fake image content", content_type="image/jpeg"),
            is_active=True,
            is_featured=False,
            weight=1.0,
            unit="kg",
        )
        repo = ProductRepository()
        updated_product = build_valid_product(
            name="NewProduct",
            slug=Slug("new-product"),
            description="Updated",
            sku=SKU("SKUNEW"),
            category_id=model.category_id,  # type: ignore[union-attr]
            brand_id=model.brand_id,  # type: ignore[union-attr]
            price=Decimal("120.00"),
            discount_price=Decimal("110.00"),
            currency=Currency("USD"),
            stock=5,
            min_stock=1,
            warehouse_location="D4",
            is_active=True,
            is_featured=True,
            weight=1.2,
            unit=WeightUnit("kg"),
            nutritional_info=None,
            ingredients=None,
            allergens=None,
        )
        new_image = SimpleUploadedFile("new-image.jpg", b"fake image content", content_type="image/jpeg")

        # When: updating the product
        result = repo.update(model.id, updated_product, image=new_image)  # type: ignore[arg-type]

        # Then: fields are updated
        assert result.name == "NewProduct"
        assert result.sku == "SKUNEW"
        assert result.is_featured is True

    def test_product_repository_delete_success(self) -> None:
        # Given: a saved product
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        model = ProductModel.objects.create(
            name="ToDelete",
            slug="todelete",
            description="Delete me",
            sku="SKUDEL",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("50.00"),
            discount_price=Decimal("45.00"),
            currency="USD",
            stock=1,
            min_stock=1,
            warehouse_location="E5",
            image=b"",
            is_active=True,
            is_featured=False,
            weight=0.5,
            unit="kg",
        )
        repo = ProductRepository()

        # When: deleting the product
        repo.delete(model.id)
        model.refresh_from_db()

        # Then: product is inactive
        assert model.is_active is False

    def test_product_repository_exists_methods(self) -> None:
        # Given: a saved product
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        model = ProductModel.objects.create(
            name="ExistingProd",
            slug="existprod",
            description="desc",
            sku="SKUEXIST",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("200.00"),
            discount_price=Decimal("190.00"),
            currency="USD",
            stock=3,
            min_stock=1,
            warehouse_location="F6",
            image=b"",
            is_active=True,
            is_featured=True,
            weight=1.0,
            unit="kg",
        )
        repo = ProductRepository()

        # When & Then: checking existence by SKU should return correct boolean
        assert repo.exists(model.id) is True
        assert repo.exists_by_sku("SKUEXIST") is True
        model.is_active = False
        model.save()
        assert repo.exists(model.id) is False
        assert repo.exists_by_sku("SKUEXIST") is False

    def test_product_repository_list_featured_and_by_filters(self) -> None:
        # Given: multiple products with various attributes
        brand = BrandModel.objects.create(name="TestBrand", slug="testbrand", is_active=True)
        category = CategoryModel.objects.create(name="TestCategory", slug="testcategory", is_active=True)
        ProductModel.objects.create(
            name="FeatProd",
            slug="fp",
            description="desc",
            sku="SKU1",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("100"),
            discount_price=Decimal("90"),
            currency="USD",
            stock=5,
            min_stock=1,
            warehouse_location="",
            image=b"",
            is_active=True,
            is_featured=True,
            weight=1,
            unit="kg",
        )
        ProductModel.objects.create(
            name="NonFeatProd",
            slug="nfp",
            description="desc",
            sku="SKU2",
            category_id=category.id,
            brand_id=brand.id,
            price=Decimal("200"),
            discount_price=Decimal("140"),
            currency="USD",
            stock=5,
            min_stock=1,
            warehouse_location="",
            image=b"",
            is_active=True,
            is_featured=False,
            weight=1,
            unit="kg",
        )
        repo = ProductRepository()

        # When: listing featured products
        featured = repo.list_featured()
        # Then: only featured returned
        assert len(featured) == 1
        assert featured[0].name == "FeatProd"

        # When: listing by category
        by_category = repo.list_by_category(category.id)
        assert len(by_category) == 2

        # When: listing by brand
        by_brand = repo.list_by_brand(brand.id)
        assert len(by_brand) == 2

        # When: filtering with query params
        filtered = repo.list_all({"q": "FeatProd", "category": category.id, "min_price": 50, "max_price": 150})
        assert len(filtered) == 1
        assert filtered[0].name == "FeatProd"
