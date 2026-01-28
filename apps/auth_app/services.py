import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

from apps.users.models import User
from apps.users.services import UserService
from .models import Session


class AuthService:
    """Сервис аутентификации."""

    @staticmethod
    def generate_token(user: User) -> str:
        """Генерация JWT токена."""
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        """Декодирование JWT токена."""
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @classmethod
    def login(cls, email: str, password: str) -> tuple[User, str] | tuple[None, None]:
        """
        Аутентификация пользователя.
        Возвращает (user, token) или (None, None).
        """
        user = UserService.get_by_email(email)
        if not user or not UserService.verify_password(password, user.password_hash):
            return None, None

        token = cls.generate_token(user)
        
        # Создаем сессию
        Session.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        )
        
        return user, token

    @classmethod
    def logout(cls, token: str) -> bool:
        """Выход из системы - инвалидация сессии."""
        session = Session.objects.filter(token=token, is_active=True).first()
        if session:
            session.invalidate()
            return True
        return False

    @classmethod
    def get_user_by_token(cls, token: str) -> User | None:
        """Получить пользователя по токену."""
        payload = cls.decode_token(token)
        if not payload:
            return None

        # Проверяем сессию в БД
        session = Session.objects.filter(token=token, is_active=True).first()
        if not session or not session.is_valid:
            return None

        return User.objects.filter(id=payload['user_id'], is_active=True).first()
