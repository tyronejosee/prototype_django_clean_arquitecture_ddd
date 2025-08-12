from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs) -> dict:
        if attrs["new_password"] != attrs["confirm_password"]:
            message = "New passwords do not match."
            raise serializers.ValidationError(message)
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)
