from rest_framework import serializers


class CouponSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField()
    max_uses = serializers.IntegerField(allow_null=True)
    used_count = serializers.IntegerField()
    expires_at = serializers.DateTimeField()
