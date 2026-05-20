import time
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings


class RateLimitMiddleware:
    """
    Rate limiting global:
    - 100 req/min por IP (não autenticado)
    - 1000 req/min por usuário autenticado
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignorar healthcheck e static/media
        path = request.path_info
        if path.startswith('/health') or path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)

        # Identificar chave de rate limit
        if hasattr(request, 'user') and request.user and request.user.is_authenticated:
            key = f'ratelimit:user:{request.user.id}'
            limit = 1000
            window = 60
        else:
            ip = self._get_client_ip(request)
            key = f'ratelimit:ip:{ip}'
            limit = 100
            window = 60

        # Verificar e incrementar contador
        now = int(time.time())
        window_key = f'{key}:{now // window}'
        current = cache.get(window_key, 0)

        if current >= limit:
            return JsonResponse(
                {'detail': 'Rate limit exceeded. Try again later.'},
                status=429,
                headers={
                    'X-RateLimit-Limit': str(limit),
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Window': str(window),
                    'Retry-After': str(window - (now % window)),
                }
            )

        cache.set(window_key, current + 1, timeout=window)
        remaining = max(0, limit - current - 1)

        response = self.get_response(request)
        response['X-RateLimit-Limit'] = str(limit)
        response['X-RateLimit-Remaining'] = str(remaining)
        response['X-RateLimit-Window'] = str(window)
        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
