import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import logging


def init_sentry():
    """Inicializa Sentry com integrações Django e Celery."""
    dsn = os.environ.get('SENTRY_DSN')
    if not dsn:
        logging.info('[Sentry] DSN não configurado — skipping initialization')
        return

    environment = os.environ.get('ENVIRONMENT', 'development')
    release = os.environ.get('RELEASE', 'unknown')

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
    logging.info(f'[Sentry] Initialized — env={environment}, release={release}')


def filter_sensitive_events(event, hint):
    """Remove dados sensíveis antes de enviar para Sentry."""
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
