from rest_framework import serializers


class CouponInputSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    discount_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField()
    max_uses = serializers.IntegerField(allow_null=True)
    expires_at = serializers.DateTimeField()


class CouponOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(read_only=True, max_length=50)
    discount_percent = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    is_active = serializers.BooleanField(read_only=True)
    max_uses = serializers.IntegerField(read_only=True)
    used_count = serializers.IntegerField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
