from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для чтения."""
    full_name = serializers.CharField(read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'patronymic', 
                  'full_name', 'is_active', 'roles', 'created_at']

    def get_roles(self, obj):
        return [r.name for r in obj.get_roles()]


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email уже зарегистрирован'})
        return data


class UserUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления профиля."""
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    patronymic = serializers.CharField(max_length=100, required=False, allow_blank=True)
    password = serializers.CharField(min_length=6, required=False, write_only=True)
    password_confirm = serializers.CharField(min_length=6, required=False, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password and password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        return data
