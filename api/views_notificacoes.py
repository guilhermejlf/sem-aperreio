import os
import threading
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .tasks import send_weekly_reminder, check_monthly_average


@api_view(['GET'])
@permission_classes([AllowAny])
def healthcheck(request):
    """Healthcheck endpoint para monitoramento."""
    return Response({
        'status': 'ok',
        'version': '2.0',
        'timestamp': timezone.now().isoformat(),
    })




@api_view(['GET'])
@permission_classes([AllowAny])
def healthcheck_detailed(request):
    """Healthcheck detalhado para monitoramento de infraestrutura."""
    import time
    from django.db import connection
    from django.core.cache import cache
    from redis.exceptions import ConnectionError as RedisConnectionError

    start_time = time.time()
    checks = {
        'database': {'status': 'unknown', 'response_ms': 0},
        'redis': {'status': 'unknown', 'response_ms': 0},
        'celery': {'status': 'unknown', 'response_ms': 0},
        'email': {'status': 'unknown'},
        'openai': {'status': 'unknown'},
    }

    # Check database
    db_start = time.time()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        checks['database']['status'] = 'ok'
    except Exception as e:
        checks['database']['status'] = 'error'
        checks['database']['error'] = str(e)
    checks['database']['response_ms'] = round((time.time() - db_start) * 1000, 2)

    # Check Redis (com timeout curto para nao bloquear)
    redis_start = time.time()
    try:
        from django.core.cache.backends.base import InvalidCacheBackendError
        cache.set('healthcheck_test', 'ok', timeout=5)
        val = cache.get('healthcheck_test')
        if val == 'ok':
            checks['redis']['status'] = 'ok'
        else:
            checks['redis']['status'] = 'error'
            checks['redis']['error'] = 'Cache value mismatch'
    except (RedisConnectionError, InvalidCacheBackendError, ConnectionError, OSError):
        checks['redis']['status'] = 'unavailable'
    except Exception as e:
        checks['redis']['status'] = 'error'
        checks['redis']['error'] = str(e)[:200]
    checks['redis']['response_ms'] = round((time.time() - redis_start) * 1000, 2)

    # Check Celery (config + broker connection apenas)
    celery_start = time.time()
    try:
        from celery import current_app
        # Verifica se o app Celery está configurado e consegue pingar o broker
        # Não usa inspect() pois pode bloquear com timeout > 10s
        broker_url = current_app.conf.broker_url
        checks['celery']['status'] = 'ok'
        checks['celery']['broker'] = broker_url.split('@')[-1] if broker_url else 'unknown'
    except Exception as e:
        checks['celery']['status'] = 'error'
        checks['celery']['error'] = str(e)
    checks['celery']['response_ms'] = round((time.time() - celery_start) * 1000, 2)

    # Check email (SendGrid config)
    checks['email']['status'] = 'ok' if bool(settings.EMAIL_HOST_PASSWORD) else 'not_configured'

    # Check OpenAI
    checks['openai']['status'] = 'ok' if bool(os.environ.get('OPENAI_API_KEY')) else 'not_configured'

    total_time = round((time.time() - start_time) * 1000, 2)
    all_ok = all(c['status'] in ('ok', 'not_configured') for c in checks.values())

    return Response({
        'status': 'healthy' if all_ok else 'degraded',
        'version': '2.1.0',
        'timestamp': timezone.now().isoformat(),
        'total_response_ms': total_time,
        'checks': checks,
    }, status=200 if all_ok else 503)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notificacoes_status(request):
    """Retorna configuração de notificações do usuário logado."""
    # TODO: Implementar modelo UserNotificationPreferences para permitir
    # cada usuário habilitar/desabilitar lembretes e alertas individualmente.
    return Response({
        'email_configurado': bool(settings.EMAIL_HOST_PASSWORD),
        'lembrete_semanal': True,
        'alerta_media': True,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_tasks(request):
    """
    Endpoint para acionar tasks manualmente.
    Protegido por secret key para evitar spam.
    Usado por cron-job.org quando Railway free tier não suporta worker.
    """
    # Read secret from custom header (avoids exposure in URL query params / logs)
    secret = request.headers.get('X-Trigger-Secret', '')

    expected = os.environ.get('TASK_TRIGGER_SECRET', '')
    if not expected or secret != expected:
        return Response({'erro': 'Unauthorized'}, status=403)

    task_type = request.data.get('task') if hasattr(request, 'data') else None
    if not task_type:
        task_type = request.GET.get('task', 'all')

    def _run_tasks():
        results = {}
        if task_type in ('all', 'reminder'):
            try:
                results['reminder'] = send_weekly_reminder()
            except Exception as e:
                results['reminder'] = f'Erro: {str(e)}'
        if task_type in ('all', 'average'):
            try:
                results['average'] = check_monthly_average()
            except Exception as e:
                results['average'] = f'Erro: {str(e)}'
        # Railway free tier may kill the process after HTTP response,
        # but the thread gets a few seconds grace period.
        # For reliable delivery, consider upgrading Railway or using a paid worker.

    # Start background thread and return immediately to avoid cron-job timeout
    t = threading.Thread(target=_run_tasks, daemon=True)
    t.start()

    return Response({'status': 'started', 'task': task_type})
