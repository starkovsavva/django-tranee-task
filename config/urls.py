from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('apps.auth_app.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/permissions/', include('apps.permissions.urls')),
    path('api/business/', include('apps.business.urls')),
]
