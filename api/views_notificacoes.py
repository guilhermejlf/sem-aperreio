import os
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
    secret = request.data.get('secret') if hasattr(request, 'data') else None
    if not secret:
        secret = request.GET.get('secret', '')

    expected = os.environ.get('TASK_TRIGGER_SECRET', '')
    if not expected or secret != expected:
        return Response({'erro': 'Unauthorized'}, status=403)

    task_type = request.data.get('task') if hasattr(request, 'data') else None
    if not task_type:
        task_type = request.GET.get('task', 'all')

    results = {}

    if task_type in ('all', 'reminder'):
        results['reminder'] = send_weekly_reminder()
    if task_type in ('all', 'average'):
        results['average'] = check_monthly_average()

    return Response({'status': 'ok', 'results': results})
