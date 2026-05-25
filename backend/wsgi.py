"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Inicializa Sentry ANTES de carregar a aplicação
print('[WSGI] Iniciando Sentry...', flush=True)
from backend.sentry_config import init_sentry
init_sentry()
print('[WSGI] Sentry iniciado', flush=True)

application = get_wsgi_application()
