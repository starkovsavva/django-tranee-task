from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Role, UserRole, Resource, Permission
from .serializers import (
    RoleSerializer, ResourceSerializer, PermissionSerializer,
    PermissionUpdateSerializer, UserRoleSerializer, AssignRoleSerializer
)
from .services import PermissionService
from apps.auth_app.decorators import login_required, admin_required
from apps.users.models import User


class RoleListView(APIView):
    """Список ролей (только для админа)."""

    @admin_required
    def get(self, request):
        roles = Role.objects.all()
        return Response(RoleSerializer(roles, many=True).data)


class ResourceListView(APIView):
    """Список ресурсов (только для админа)."""

    @admin_required
    def get(self, request):
        resources = Resource.objects.all()
        return Response(ResourceSerializer(resources, many=True).data)


class PermissionListView(APIView):
    """Список всех прав доступа (только для админа)."""

    @admin_required
    def get(self, request):
        permissions = Permission.objects.select_related('role', 'resource').all()
        return Response(PermissionSerializer(permissions, many=True).data)


class PermissionDetailView(APIView):
    """Управление конкретным правом доступа (только для админа)."""

    @admin_required
    def get(self, request, pk):
        permission = Permission.objects.filter(pk=pk).first()
        if not permission:
            return Response({'error': 'Право не найдено'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PermissionSerializer(permission).data)

    @admin_required
    def patch(self, request, pk):
        permission = Permission.objects.filter(pk=pk).first()
        if not permission:
            return Response({'error': 'Право не найдено'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PermissionUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for field, value in serializer.validated_data.items():
            setattr(permission, field, value)
        permission.save()

        return Response(PermissionSerializer(permission).data)


class UserRoleListView(APIView):
    """Список назначений ролей пользователям (только для админа)."""

    @admin_required
    def get(self, request):
        user_roles = UserRole.objects.select_related('user', 'role').all()
        return Response(UserRoleSerializer(user_roles, many=True).data)

    @admin_required
    def post(self, request):
        """Назначить роль пользователю."""
        serializer = AssignRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=serializer.validated_data['user_id']).first()
        role = Role.objects.filter(id=serializer.validated_data['role_id']).first()

        if not user:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        if not role:
            return Response({'error': 'Роль не найдена'}, status=status.HTTP_404_NOT_FOUND)

        user_role, created = UserRole.objects.get_or_create(user=user, role=role)
        return Response(
            UserRoleSerializer(user_role).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class UserRoleDeleteView(APIView):
    """Удаление роли у пользователя (только для админа)."""

    @admin_required
    def delete(self, request, pk):
        user_role = UserRole.objects.filter(pk=pk).first()
        if not user_role:
            return Response({'error': 'Назначение не найдено'}, status=status.HTTP_404_NOT_FOUND)
        user_role.delete()
        return Response({'message': 'Роль удалена у пользователя'})


class MyPermissionsView(APIView):
    """Получить свои права доступа."""

    @login_required
    def get(self, request):
        permissions = PermissionService.get_user_permissions(request.user)
        return Response({
            'user': request.user.email,
            'roles': [r.name for r in request.user.get_roles()],
            'permissions': permissions
        })
