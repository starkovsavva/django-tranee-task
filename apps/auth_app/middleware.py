from .services import AuthService


class JWTAuthMiddleware:
    """
    Middleware для JWT аутентификации.
    Извлекает токен из заголовка Authorization и устанавливает request.user.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            request.user = AuthService.get_user_by_token(token)

        return self.get_response(request)
