from django.urls import path
from .views import (
    ProductsView, ProductDetailView,
    OrdersView, OrderDetailView,
    ReportsView
)

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('reports/', ReportsView.as_view(), name='reports'),
]
