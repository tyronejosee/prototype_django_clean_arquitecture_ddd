from typing import ClassVar, cast
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.users.application.providers import (
    get_add_to_wishlist_use_case,
    get_list_wishlist_use_case,
    get_remove_from_wishlist_use_case,
)
from src.modules.users.domain.exceptions import (
    WishlistDomainError,
    WishlistItemAlreadyExistsError,
    WishlistItemNotFoundError,
)
from src.modules.users.presentation.serializers.wishlist_serializer import (
    WishlistCreateSerializer,
    WishlistListSerializer,
)
from src.modules.users.presentation.throttles import (
    AddWishlistItemRateThrottle,
    DeleteWishlistItemRateThrottle,
    ListWishlistRateThrottle,
)


class WishlistController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"GET": ListWishlistRateThrottle, "POST": AddWishlistItemRateThrottle}

    def get(self, request: Request) -> Response:
        use_case = get_list_wishlist_use_case()
        wishlist = use_case.execute(request.user.id)
        serializer = WishlistListSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = WishlistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict, serializer.validated_data)
        use_case = get_add_to_wishlist_use_case()

        try:
            item = use_case.execute(request.user.id, data["product_id"])
            return Response(WishlistListSerializer(item).data, status=status.HTTP_201_CREATED)
        except (WishlistDomainError, WishlistItemAlreadyExistsError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WishlistDetailController(BaseController):
    permission_classes: ClassVar[list] = [IsAuthenticated]
    throttle_map: dict = {"DELETE": DeleteWishlistItemRateThrottle}

    def delete(self, request: Request, product_id: UUID) -> Response:
        use_case = get_remove_from_wishlist_use_case()

        try:
            use_case.execute(request.user.id, product_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WishlistItemNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
