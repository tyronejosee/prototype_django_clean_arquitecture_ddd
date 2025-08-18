from rest_framework import serializers


class BrandInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()


class BrandOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
