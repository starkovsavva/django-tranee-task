from django.urls import path
from .views import (
    RoleListView, ResourceListView, PermissionListView,
    PermissionDetailView, UserRoleListView, UserRoleDeleteView,
    MyPermissionsView
)

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='roles'),
    path('resources/', ResourceListView.as_view(), name='resources'),
    path('rules/', PermissionListView.as_view(), name='permissions'),
    path('rules/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),
    path('user-roles/', UserRoleListView.as_view(), name='user-roles'),
    path('user-roles/<int:pk>/', UserRoleDeleteView.as_view(), name='user-role-delete'),
    path('my/', MyPermissionsView.as_view(), name='my-permissions'),
]
