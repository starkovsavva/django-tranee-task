from .models import Role, Permission, Resource
from apps.users.models import User


class PermissionService:
    """Сервис проверки прав доступа."""

    @staticmethod
    def check_permission(user: User, resource_code: str, action: str, is_owner: bool = False) -> bool:
        """
        Проверяет, имеет ли пользователь право на действие с ресурсом.
        
        user: пользователь
        resource_code: код ресурса (products, orders, etc.)
        action: read, create, update, delete
        is_owner: является ли пользователь владельцем объекта
        """
        roles = user.get_roles()
        
        for role in roles:
            permission = Permission.objects.filter(
                role=role,
                resource__code=resource_code
            ).first()
            
            if permission and permission.has_permission(action, is_owner):
                return True
        
        return False

    @staticmethod
    def get_user_permissions(user: User) -> dict:
        """Получить все права пользователя."""
        result = {}
        roles = user.get_roles()
        
        for role in roles:
            for perm in Permission.objects.filter(role=role).select_related('resource'):
                resource_code = perm.resource.code
                if resource_code not in result:
                    result[resource_code] = {
                        'read': False, 'read_all': False,
                        'create': False,
                        'update': False, 'update_all': False,
                        'delete': False, 'delete_all': False,
                    }
                
                # Объединяем права от разных ролей
                for action in ['read', 'read_all', 'create', 'update', 'update_all', 'delete', 'delete_all']:
                    if getattr(perm, f'can_{action}', False):
                        result[resource_code][action] = True
        
        return result
