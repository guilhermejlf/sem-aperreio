import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

# Release tracking consistente
_DEFAULT_VERSION = '2.1.0'


def _get_release():
    """Retorna release tag no formato sem-aperreio@vX.Y.Z."""
    release = os.environ.get('RELEASE')
    if release:
        if not release.startswith('sem-aperreio@'):
            return f'sem-aperreio@{release}'
        return release
    return f'sem-aperreio@v{_DEFAULT_VERSION}'


def init_sentry():
    """Inicializa Sentry com integracoes Django e Celery."""
    dsn = os.environ.get('SENTRY_DSN')
    if not dsn:
        print('[Sentry] DSN nao configurado — skipping initialization')
        return

    environment = os.environ.get('ENVIRONMENT', 'development')
    release = _get_release()

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=True,
            ),
            CeleryIntegration(
                propagate_traces=True,
            ),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        profiles_sample_rate=float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', '0.05')),
        send_default_pii=True,
        attach_stacktrace=True,
        max_breadcrumbs=50,
        before_send=filter_sensitive_events,
    )
    print(f'[Sentry] Initialized — env={environment}, release={release}')


def filter_sensitive_events(event, hint):
    """Remove dados sensiveis e filtra ruido antes de enviar para Sentry."""
    # Filtrar erros conhecidos de ruido
    if _is_noise_event(event):
        return None

    if 'exception' in event:
        # Mascara tokens JWT e senhas em stacktraces
        for value in event.get('exception', {}).get('values', []):
            stacktrace = value.get('stacktrace', {})
            for frame in stacktrace.get('frames', []):
                vars_dict = frame.get('vars', {})
                for key in list(vars_dict.keys()):
                    if any(s in key.lower() for s in ['password', 'token', 'secret', 'key', 'auth']):
                        vars_dict[key] = '[FILTERED]'
    return event


def _is_noise_event(event):
    """Retorna True se o evento for ruido conhecido que deve ser ignorado."""
    try:
        values = event.get('exception', {}).get('values', [])
        for value in values:
            exc_type = value.get('type', '')
            exc_value = value.get('value', '')

            # Ignorar erros comuns de browser/extensions
            noise_patterns = [
                'ResizeObserver loop limit exceeded',
                'ResizeObserver loop completed with undelivered notifications',
                'Non-Error promise rejection captured',
                'Cannot redefine property: googletag',
                'window.__REACT_DEVTOOLS_GLOBAL_HOOK__',
                'Extension context invalidated',
                'The fetching process for the media resource',
                'NetworkError when attempting to fetch resource',
                'AbortError',
                'CancelError',
                'The operation was aborted',
                'The user aborted a request',
            ]
            for pattern in noise_patterns:
                if pattern in exc_value:
                    return True

            # Ignorar erros de extensões conhecidas
            if exc_type in (
                'SecurityError',  # CORS/policy de extensões
            ):
                # Verificar se vem de uma extensão
                frames = value.get('stacktrace', {}).get('frames', [])
                for frame in frames:
                    filename = frame.get('filename', '')
                    if 'chrome-extension://' in filename or 'moz-extension://' in filename:
                        return True

            # Ignorar erros de serviços de tracking/analytics
            frames = value.get('stacktrace', {}).get('frames', [])
            for frame in frames:
                filename = frame.get('filename', '')
                if any(domain in filename for domain in [
                    'google-analytics',
                    'googletagmanager',
                    'facebook.com/tr',
                    'connect.facebook.net',
                ]):
                    return True

    except Exception:
        pass
    return False
