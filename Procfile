web: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A backend worker -l info -c 2
beat: celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
