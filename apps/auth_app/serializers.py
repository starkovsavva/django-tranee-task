from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа."""
    email = serializers.EmailField()
    password = serializers.CharField()
