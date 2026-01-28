from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer
from .services import AuthService
from .decorators import login_required
from apps.users.serializers import UserSerializer


class LoginView(APIView):
    """Вход в систему."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user, token = AuthService.login(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'error': 'Неверный email или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'token': token,
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    """Выход из системы."""

    @login_required
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        AuthService.logout(token)
        return Response({'message': 'Выход выполнен'})
