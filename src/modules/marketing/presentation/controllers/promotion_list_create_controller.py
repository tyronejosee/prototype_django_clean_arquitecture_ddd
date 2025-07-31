from typing import cast

from modules.common.presentation.controllers.base_controller import BaseController
from modules.common.presentation.pagination import paginate_queryset
from modules.marketing.application.providers import (
    get_create_promotion_use_case,
    get_get_active_promotions_use_case,
)
from modules.marketing.domain.exceptions import (
    MarketingDomainError,
    PromotionDomainError,
)
from modules.marketing.presentation.serializers.promotion_serializer import (
    PromotionSerializer,
)
from modules.marketing.presentation.throttles import (
    CreatePromotionRateThrottle,
    ListPromotionsRateThrottle,
)
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class PromotionListCreateController(BaseController):
    throttle_map: dict = {
        "GET": ListPromotionsRateThrottle,
        "POST": CreatePromotionRateThrottle,
    }

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        use_case = get_get_active_promotions_use_case()
        promotions = use_case.execute()
        response = paginate_queryset(request, promotions, PromotionSerializer)
        response.status_code = status.HTTP_200_OK
        return response

    def post(self, request: Request) -> Response:
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_promotion_use_case()
        try:
            data = cast(dict, serializer.validated_data)
            promotion = use_case.execute(data=data)
            return Response(
                PromotionSerializer(promotion).data,
                status=status.HTTP_201_CREATED,
            )
        except (PromotionDomainError, MarketingDomainError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
