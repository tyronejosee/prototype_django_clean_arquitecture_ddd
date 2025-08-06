from uuid import UUID


class CartCacheKeys:
    @staticmethod
    def cart_user_key(user_id: UUID) -> str:
        return "cart:user:" + str(user_id)
