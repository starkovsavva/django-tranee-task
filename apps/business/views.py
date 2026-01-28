from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.auth_app.decorators import login_required
from apps.permissions.services import PermissionService
from .mock_data import PRODUCTS, ORDERS, REPORTS


class BaseBusinessView(APIView):
    """Базовый класс для бизнес-ресурсов с проверкой прав."""
    resource_code = None
    mock_data = None

    def check_access(self, request, action: str, obj_id: int = None):
        """
        Проверка доступа.
        Возвращает (True, None) если доступ есть,
        или (False, Response) с ошибкой.
        """
        if not hasattr(request, 'user') or request.user is None:
            return False, Response(
                {'error': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Проверяем владельца для конкретного объекта
        is_owner = False
        if obj_id and self.mock_data:
            obj = next((x for x in self.mock_data if x['id'] == obj_id), None)
            if obj:
                is_owner = str(obj.get('owner_id')) == str(request.user.id)

        if not PermissionService.check_permission(
            request.user, self.resource_code, action, is_owner
        ):
            return False, Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )

        return True, None


class ProductsView(BaseBusinessView):
    """Mock API для товаров."""
    resource_code = 'products'
    mock_data = PRODUCTS

    def get(self, request):
        """Получить список товаров."""
        has_access, error = self.check_access(request, 'read')
        if not has_access:
            return error
        return Response({'products': PRODUCTS})

    def post(self, request):
        """Создать товар."""
        has_access, error = self.check_access(request, 'create')
        if not has_access:
            return error
        return Response({'message': 'Товар создан (mock)', 'data': request.data})


class ProductDetailView(BaseBusinessView):
    """Mock API для конкретного товара."""
    resource_code = 'products'
    mock_data = PRODUCTS

    def get(self, request, pk):
        """Получить товар."""
        has_access, error = self.check_access(request, 'read', pk)
        if not has_access:
            return error
        product = next((p for p in PRODUCTS if p['id'] == pk), None)
        if not product:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(product)

    def patch(self, request, pk):
        """Обновить товар."""
        has_access, error = self.check_access(request, 'update', pk)
        if not has_access:
            return error
        return Response({'message': 'Товар обновлен (mock)', 'id': pk})

    def delete(self, request, pk):
        """Удалить товар."""
        has_access, error = self.check_access(request, 'delete', pk)
        if not has_access:
            return error
        return Response({'message': 'Товар удален (mock)', 'id': pk})


class OrdersView(BaseBusinessView):
    """Mock API для заказов."""
    resource_code = 'orders'
    mock_data = ORDERS

    def get(self, request):
        """Получить список заказов."""
        has_access, error = self.check_access(request, 'read')
        if not has_access:
            return error
        return Response({'orders': ORDERS})

    def post(self, request):
        """Создать заказ."""
        has_access, error = self.check_access(request, 'create')
        if not has_access:
            return error
        return Response({'message': 'Заказ создан (mock)', 'data': request.data})


class OrderDetailView(BaseBusinessView):
    """Mock API для конкретного заказа."""
    resource_code = 'orders'
    mock_data = ORDERS

    def get(self, request, pk):
        """Получить заказ."""
        has_access, error = self.check_access(request, 'read', pk)
        if not has_access:
            return error
        order = next((o for o in ORDERS if o['id'] == pk), None)
        if not order:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(order)

    def patch(self, request, pk):
        """Обновить заказ."""
        has_access, error = self.check_access(request, 'update', pk)
        if not has_access:
            return error
        return Response({'message': 'Заказ обновлен (mock)', 'id': pk})

    def delete(self, request, pk):
        """Удалить заказ."""
        has_access, error = self.check_access(request, 'delete', pk)
        if not has_access:
            return error
        return Response({'message': 'Заказ удален (mock)', 'id': pk})


class ReportsView(BaseBusinessView):
    """Mock API для отчетов."""
    resource_code = 'reports'
    mock_data = REPORTS

    def get(self, request):
        """Получить список отчетов."""
        has_access, error = self.check_access(request, 'read')
        if not has_access:
            return error
        return Response({'reports': REPORTS})
