import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Inicializa Sentry antes de criar o app Celery
from backend.sentry_config import init_sentry
init_sentry()

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
