from django.db import models
from apps.users.models import User


class Role(models.Model):
    """
    Роли пользователей: admin, manager, user.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
    Связь пользователей и ролей.
    Пользователь может иметь несколько ролей.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class Resource(models.Model):
    """
    Ресурсы (бизнес-объекты) системы.
    Примеры: products, orders, reports.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'resources'

    def __str__(self):
        return self.code


class Permission(models.Model):
    """
    Правила доступа: какая роль какие действия может выполнять с ресурсом.
    
    Действия:
    - read: чтение своих объектов
    - read_all: чтение всех объектов
    - create: создание
    - update: обновление своих объектов
    - update_all: обновление всех объектов
    - delete: удаление своих объектов
    - delete_all: удаление всех объектов
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')
    
    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        db_table = 'permissions'
        unique_together = ('role', 'resource')

    def __str__(self):
        return f"{self.role.name} -> {self.resource.code}"

    def has_permission(self, action: str, is_owner: bool = False) -> bool:
        """
        Проверяет право на действие.
        action: read, create, update, delete
        is_owner: владелец ли пользователь объекта
        """
        all_perm = getattr(self, f'can_{action}_all', False)
        own_perm = getattr(self, f'can_{action}', False)
        
        if all_perm:
            return True
        if action == 'create':
            return own_perm
        if own_perm and is_owner:
            return True
        return False
