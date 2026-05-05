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
