from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.presentation.controllers.base_controller import BaseController
from apps.marketing.application.providers import (
    get_create_promotion_use_case,
    get_get_active_promotions_use_case,
)
from apps.marketing.domain.exceptions import PromotionDomainError
from apps.marketing.presentation.serializers.promotion_serializer import (
    PromotionSerializer,
)


class PromotionListController(BaseController):
    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser]
        return [IsAuthenticated]

    def get(self, request: Request) -> Response:
        use_case = get_get_active_promotions_use_case()
        promotions = use_case.execute()
        return Response(PromotionSerializer(promotions, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_promotion_use_case()
        try:
            promotion = use_case.execute(
                data=serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(PromotionSerializer(promotion).data, status=201)
        except PromotionDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
