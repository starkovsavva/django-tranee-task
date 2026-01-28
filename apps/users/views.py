from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .services import UserService
from apps.auth_app.decorators import login_required


class RegisterView(APIView):
    """Регистрация нового пользователя."""

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = UserService.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            patronymic=data.get('patronymic')
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    """Профиль текущего пользователя."""

    @login_required
    def get(self, request):
        """Получить свой профиль."""
        return Response(UserSerializer(request.user).data)

    @login_required
    def patch(self, request):
        """Обновить свой профиль."""
        serializer = UserUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.update_user(request.user, **serializer.validated_data)
        return Response(UserSerializer(user).data)

    @login_required
    def delete(self, request):
        """Мягкое удаление аккаунта."""
        # Инвалидируем все сессии
        from apps.auth_app.models import Session
        Session.objects.filter(user=request.user).update(is_active=False)
        
        # Мягкое удаление
        UserService.soft_delete(request.user)
        return Response({'message': 'Аккаунт деактивирован'}, status=status.HTTP_200_OK)
