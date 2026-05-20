"""Utilitários de cache com Redis/LocMem para o Sem Aperreio."""
import hashlib
import logging
from functools import wraps

from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_PREFIX = 'sa'
CACHE_TIMEOUT = 300  # 5 minutos


def _user_key(user):
    return str(user.id)


def cache_key(base, user, *args):
    """Gera chave de cache determinística."""
    parts = [CACHE_PREFIX, base, _user_key(user)] + [str(a) for a in args]
    return ':'.join(parts)


def cached_view(base_key, timeout=CACHE_TIMEOUT):
    """Decorator para cachear resposta de view DRF.

    Armazena os dados serializáveis (response.data) em vez do objeto
    Response, evitando problemas de pickle com DRF/LocMemCache.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Só cacheia GET
            if request.method != 'GET':
                return func(request, *args, **kwargs)

            # Monta chave com query params ordenados (hash para evitar
            # caracteres problemáticos com memcached/redis)
            query_str = '&'.join(f'{k}={v}' for k, v in sorted(request.query_params.items()))
            query_hash = hashlib.md5(query_str.encode()).hexdigest()[:8]
            key = cache_key(base_key, request.user, *args, query_hash)

            cached = cache.get(key)
            if cached is not None:
                logger.debug(f'Cache HIT: {key}')
                from rest_framework.response import Response
                return Response(cached['data'], status=cached['status'])

            response = func(request, *args, **kwargs)
            if hasattr(response, 'status_code') and response.status_code == 200:
                cache.set(key, {'data': response.data, 'status': response.status_code}, timeout=timeout)
                logger.debug(f'Cache SET: {key}')
            return response
        return wrapper
    return decorator


def invalidate_user_cache(user, *patterns):
    """Invalida chaves de cache do usuário que casem com os padrões."""
    # Se for LocMemCache, não temos como listar chaves; fazemos delete exato
    # Se for Redis, podemos usar pattern matching
    try:
        # Tentativa de usar pattern delete (Redis)
        from django_redis import get_redis_connection
        redis = get_redis_connection('default')
        for pattern in patterns:
            key = f'{CACHE_PREFIX}:{pattern}:{_user_key(user)}*'
            keys = redis.keys(key)
            if keys:
                redis.delete(*keys)
                logger.debug(f'Cache INVALIDATE (Redis): {key} — {len(keys)} chaves')
    except Exception:
        # Fallback LocMem: limpa todo o cache (aceitável em dev)
        logger.debug(f'Cache INVALIDATE (LocMem): patterns={patterns}, user={user.id}')
        cache.clear()


def invalidate_dashboard(user):
    """Invalida cache do dashboard do usuário."""
    invalidate_user_cache(user, 'dashboard')


def invalidate_gastos(user):
    """Invalida cache de gastos/extrato/dashboard do usuário."""
    invalidate_user_cache(user, 'gastos', 'extrato', 'dashboard')


def invalidate_receitas(user):
    """Invalida cache de receitas/extrato/dashboard do usuário."""
    invalidate_user_cache(user, 'receitas', 'extrato', 'dashboard')


def invalidate_metas(user):
    """Invalida cache de metas/dashboard do usuário."""
    invalidate_user_cache(user, 'metas', 'dashboard')
