from rest_framework import serializers


class InitiatePaymentInputSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    payment_method = serializers.CharField(required=True)


class DetailsOuputSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)


class InitiatePaymentOutputSerializer(serializers.Serializer):
    external_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    redirect_url = serializers.URLField(read_only=True)
    details = DetailsOuputSerializer(read_only=True)


class CapturePaymentOutputSerializer(serializers.Serializer):
    external_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    details = serializers.DictField(child=serializers.CharField(read_only=True))
