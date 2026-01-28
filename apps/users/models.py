import uuid
from django.db import models


class User(models.Model):
    """
    Модель пользователя. Не используем встроенную модель Django.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Для мягкого удаления
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    def get_roles(self):
        """Получить роли пользователя."""
        return [ur.role for ur in self.user_roles.select_related('role')]

    def has_role(self, role_name: str) -> bool:
        """Проверить наличие роли."""
        return any(r.name == role_name for r in self.get_roles())

    def is_admin(self) -> bool:
        """Проверить, является ли администратором."""
        return self.has_role('admin')
