from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def login_required(view_method):
    """Декоратор для проверки аутентификации."""
    @wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_method(self, request, *args, **kwargs)
    return wrapper


def admin_required(view_method):
    """Декоратор для проверки прав администратора."""
    @wraps(view_method)
    def wrapper(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or request.user is None:
            return Response(
                {'error': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not request.user.is_admin():
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_method(self, request, *args, **kwargs)
    return wrapper
