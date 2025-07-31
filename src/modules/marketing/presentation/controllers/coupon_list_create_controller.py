from typing import cast

from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.controllers.base_controller import BaseController
from src.modules.common.presentation.pagination import paginate_queryset
from src.modules.marketing.application.providers import (
    get_create_coupon_use_case,
    get_get_active_coupons_use_case,
)
from src.modules.marketing.domain.exceptions import (
    CouponDomainError,
    MarketingDomainError,
)
from src.modules.marketing.presentation.serializers.coupon_serializer import (
    CouponSerializer,
)
from src.modules.marketing.presentation.throttles import (
    CreateCouponRateThrottle,
    ListCouponsRateThrottle,
)


class CouponListCreateController(BaseController):
    throttle_map: dict = {
        "GET": ListCouponsRateThrottle,
        "POST": CreateCouponRateThrottle,
    }

    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        use_case = get_get_active_coupons_use_case()
        coupons = use_case.execute(user_id=request.user.id)
        response = paginate_queryset(request, coupons, CouponSerializer)
        response.status_code = status.HTTP_200_OK
        return response

    def post(self, request: Request) -> Response:
        serializer = CouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_coupon_use_case()
        try:
            data = cast(dict, serializer.validated_data)
            coupon = use_case.execute(data=data)
            return Response(CouponSerializer(coupon).data, status=201)
        except (CouponDomainError, MarketingDomainError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
