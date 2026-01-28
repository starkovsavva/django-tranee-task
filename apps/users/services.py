import bcrypt
from .models import User


class UserService:
    """Сервис для работы с пользователями."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля с bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Проверка пароля."""
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    @classmethod
    def create_user(cls, email: str, password: str, first_name: str, 
                    last_name: str, patronymic: str = None) -> User:
        """Создание нового пользователя."""
        user = User.objects.create(
            email=email,
            password_hash=cls.hash_password(password),
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic or ''
        )
        # Назначаем роль user по умолчанию
        from apps.permissions.models import Role, UserRole
        default_role = Role.objects.filter(name='user').first()
        if default_role:
            UserRole.objects.create(user=user, role=default_role)
        return user

    @classmethod
    def update_user(cls, user: User, **kwargs) -> User:
        """Обновление данных пользователя."""
        if 'password' in kwargs:
            user.password_hash = cls.hash_password(kwargs.pop('password'))
            kwargs.pop('password_confirm', None)
        
        for field, value in kwargs.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)
        
        user.save()
        return user

    @staticmethod
    def soft_delete(user: User) -> User:
        """Мягкое удаление пользователя."""
        user.is_active = False
        user.save()
        return user

    @staticmethod
    def get_by_email(email: str) -> User | None:
        """Получить пользователя по email."""
        return User.objects.filter(email=email, is_active=True).first()
