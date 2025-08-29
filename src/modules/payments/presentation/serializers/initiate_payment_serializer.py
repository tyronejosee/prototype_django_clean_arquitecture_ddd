from rest_framework import serializers


class InitiatePaymentInputSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    payment_method = serializers.CharField(required=True)
