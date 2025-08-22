from uuid import uuid4

from django.utils.text import slugify
import factory

from src.modules.catalog.infrastructure.models.brand_model import BrandModel
from src.modules.catalog.infrastructure.models.category_model import CategoryModel
from src.modules.catalog.infrastructure.models.product_model import ProductModel


class BrandModelFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = BrandModel

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    is_active = True


class CategoryModelFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = CategoryModel

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("sentence")
    is_active = True


class ProductModelFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore[override]
        model = ProductModel

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("sentence")
    sku = factory.Faker("ean13")
    category = factory.SubFactory(CategoryModelFactory)
    brand = factory.SubFactory(BrandModelFactory)
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    discount_price = None
    currency = "USD"
    stock = factory.Faker("random_int", min=1, max=100)
    min_stock = 1
    warehouse_location = factory.Faker("city")
    image = factory.django.ImageField(color="blue")
    is_active = True
    is_featured = False
    weight = factory.Faker("pydecimal", left_digits=2, right_digits=3, positive=True)
    unit = "kg"
    nutritional_info = {}
    ingredients = []
    allergens = []
