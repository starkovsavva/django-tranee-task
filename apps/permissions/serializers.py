from rest_framework import serializers
from .models import Role, UserRole, Resource, Permission


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'code', 'name', 'description']


class PermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    resource_code = serializers.CharField(source='resource.code', read_only=True)

    class Meta:
        model = Permission
        fields = ['id', 'role', 'role_name', 'resource', 'resource_code',
                  'can_read', 'can_read_all', 'can_create',
                  'can_update', 'can_update_all', 'can_delete', 'can_delete_all']


class PermissionUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления прав."""
    can_read = serializers.BooleanField(required=False)
    can_read_all = serializers.BooleanField(required=False)
    can_create = serializers.BooleanField(required=False)
    can_update = serializers.BooleanField(required=False)
    can_update_all = serializers.BooleanField(required=False)
    can_delete = serializers.BooleanField(required=False)
    can_delete_all = serializers.BooleanField(required=False)


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'user_email', 'role', 'role_name', 'assigned_at']


class AssignRoleSerializer(serializers.Serializer):
    """Сериализатор для назначения роли."""
    user_id = serializers.UUIDField()
    role_id = serializers.IntegerField()
