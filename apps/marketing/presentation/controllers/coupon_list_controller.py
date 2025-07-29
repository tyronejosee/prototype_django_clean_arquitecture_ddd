from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common.presentation.controllers.base_controller import BaseController
from apps.marketing.application.providers import (
    get_create_coupon_use_case,
    get_get_active_coupons_use_case,
)
from apps.marketing.domain.exceptions import CouponDomainError
from apps.marketing.presentation.serializers.coupon_serializer import CouponSerializer


class CouponListController(BaseController):
    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminUser]
        return [IsAuthenticated]

    def get(self, request: Request) -> Response:
        use_case = get_get_active_coupons_use_case()
        coupons = use_case.execute(user_id=request.user.id)
        return Response(CouponSerializer(coupons, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = CouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = get_create_coupon_use_case()
        try:
            coupon = use_case.execute(
                data=serializer.validated_data,  # type: ignore[arg-type]
            )
            return Response(CouponSerializer(coupon).data, status=201)
        except CouponDomainError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
