from django.http import JsonResponse

def sentry_test_error(request):
    """Endpoint temporario para validar Sentry ingest."""
    raise Exception('Teste Sentry backend - erro deliberado para validacao')

def sentry_test_message(request):
    """Endpoint temporario para validar Sentry capture_message."""
    import sentry_sdk
    sentry_sdk.capture_message('Teste Sentry backend - mensagem de teste', level='warning')
    return JsonResponse({'status': 'mensagem enviada'})
