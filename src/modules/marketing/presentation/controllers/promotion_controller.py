from typing import cast

from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.common.presentation.pagination import paginate_queryset
from src.modules.marketing.domain.exceptions import MarketingDomainError, PromotionDomainError
from src.modules.marketing.presentation.providers import (
    get_create_promotion_use_case,
    get_get_active_promotions_use_case,
)
from src.modules.marketing.presentation.schemas.promotion_schema import PROMOTION_LIST_CREATE_SCHEMA
from src.modules.marketing.presentation.serializers.promotion_serializer import (
    PromotionInputSerializer,
    PromotionOutputSerializer,
)
from src.modules.marketing.presentation.throttles import CreatePromotionRateThrottle, ListPromotionsRateThrottle


@extend_schema_view(**PROMOTION_LIST_CREATE_SCHEMA)
class PromotionListCreateController(BaseController):
    throttle_map: dict = {"GET": ListPromotionsRateThrottle, "POST": CreatePromotionRateThrottle}

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        use_case = get_get_active_promotions_use_case()
        promotions = use_case.execute()
        response = paginate_queryset(request, promotions, PromotionOutputSerializer)
        response.status_code = status.HTTP_200_OK
        return response

    def post(self, request: Request) -> Response:
        serializer = PromotionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast("dict", serializer.validated_data)
        use_case = get_create_promotion_use_case()

        try:
            promotion = use_case.execute(data=validated_data)
            return Response(PromotionOutputSerializer(promotion).data, status=status.HTTP_201_CREATED)
        except (PromotionDomainError, MarketingDomainError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
