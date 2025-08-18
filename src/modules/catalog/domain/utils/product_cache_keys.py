from uuid import UUID


class ProductCacheKeys:
    @staticmethod
    def product_list_key() -> str:
        return "products:is_active"

    @staticmethod
    def product_list_featured_key() -> str:
        return "products:is_featured"

    @staticmethod
    def product_list_by_category_key(category_id: UUID) -> str:
        return "products:category_id:" + str(category_id)

    @staticmethod
    def product_list_by_brand_key(brand_id: UUID) -> str:
        return "products:brand_id:" + str(brand_id)
