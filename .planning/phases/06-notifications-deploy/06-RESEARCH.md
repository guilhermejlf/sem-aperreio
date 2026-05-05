# Phase 6 Research: Notificações e Deploy

**Date:** 2026-05-05
**Phase:** 06-notifications-deploy

---

## 1. Celery + Redis para Django

### Stack
- **Celery**: Task queue padrão para Django. Suporta tarefas periódicas via `celery beat`.
- **Redis**: Broker e backend de resultados. Lightweight, free tier disponível na maioria das plataformas.

### Setup Django
```python
# settings.py
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BEAT_SCHEDULE = {
    'weekly-reminder': {
        'task': 'api.tasks.send_weekly_reminder',
        'schedule': crontab(day_of_week=1, hour=9),  # Segunda 9h
    },
    'monthly-average-alert': {
        'task': 'api.tasks.check_monthly_average',
        'schedule': crontab(day_of_week='*/7', hour=10),  # Semanal
    },
}
```

### Files needed
- `backend/celery.py` — Celery app config
- `backend/__init__.py` — Import celery app on Django startup
- `api/tasks.py` — Task definitions
- `Procfile` or Railway start command: `worker: celery -A backend worker -l info` + `beat: celery -A backend beat -l info`

### Railway specifics
- Redis: add-on gratuito no Railway (128MB, suficiente para Celery beat + tasks)
- Workers: Railway suporta múltiplos process types no Procfile ou via `railway.json`
- Environment variables: `REDIS_URL` provisionado automaticamente pelo add-on

---

## 2. Email Service

### Options
- **SendGrid**: Free tier 100 emails/dia. SMTP relay simples.
- **Mailgun**: Free tier 5.000 emails/mês por 3 meses, depois pago.
- **Gmail SMTP**: Limitado a 100 emails/dia, requer app password. OK para MVP.

### Decision
**SendGrid** — Free tier suficiente para MVP (100 emails/dia ~ 700 emails/semana, cobre muito mais que os usuários atuais). Integração simples via SMTP no Django.

### Django config
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = 'Sem Aperreio <noreply@semaperreio.app>'
```

---

## 3. PostgreSQL Migration

### Django approach
Django ORM abstrai a maioria das diferenças SQLite → PostgreSQL. Potenciais problemas:
- **JSONField**: SQLite não tem native JSON; PostgreSQL sim. Se usarmos `JSONField`, precisa do PostgreSQL.
- **DateTimeField com timezone**: PostgreSQL exige `USE_TZ = True` (já padrão no Django).
- **AutoField/Serial**: Funciona igual.

### Settings pattern
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}
```

### Dependency
- `dj-database-url` + `psycopg2-binary`

### Railway
- PostgreSQL add-on gratuito: 500MB storage, suficiente para MVP.
- `DATABASE_URL` provisionado automaticamente.

---

## 4. CI/CD — GitHub Actions

### Workflow
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python manage.py check
      - run: npm ci && npm run build
        working-directory: frontend
      - uses: railway/cli-action@v1
        with: { railway_token: ${{ secrets.RAILWAY_TOKEN }} }
      - run: railway up --service backend
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: vercel/action-deploy@v1
        with: { vercel_token: ${{ secrets.VERCEL_TOKEN }} }
```

### Railway CLI
- Deploy via CLI: `railway up`
- Config file: `railway.json` para definir build/start commands
- Não precisa de Dockerfile para Django (Railway detecta Python automaticamente)

### Vercel
- Connect to GitHub repo, auto-deploy on push to main
- Build command: `cd frontend && npm run build`
- Output directory: `frontend/dist`
- Environment variable: `VITE_API_BASE_URL` apontando para o backend Railway

---

## 5. Railway + Vercel Integration

### CORS
Backend Railway precisa aceitar requisições do domínio Vercel. Adicionar `CORS_ALLOWED_ORIGINS` no settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://sem-aperreio.vercel.app',  # production
]
```

### Environment Variables
| Var | Source | Used By |
|-----|--------|---------|
| `DATABASE_URL` | Railway PostgreSQL add-on | Django settings |
| `REDIS_URL` | Railway Redis add-on | Celery broker |
| `SECRET_KEY` | Manual (GitHub Secret → Railway) | Django |
| `SENDGRID_API_KEY` | Manual (GitHub Secret → Railway) | Email backend |
| `ALLOWED_HOSTS` | Railway domain | Django |
| `DEBUG` | `False` in prod | Django |
| `VITE_API_BASE_URL` | Manual (Vercel dashboard) | Frontend build |

---

## 6. Project Structure Changes

New files:
```
backend/
  celery.py              # NEW
  __init__.py            # MODIFIED (import celery)
api/
  tasks.py               # NEW (Celery tasks)
  templates/
    emails/
      weekly_reminder.html  # NEW
      average_alert.html    # NEW
.github/
  workflows/
    deploy.yml             # NEW
railway.json               # NEW
Procfile                   # NEW
requirements.txt           # MODIFIED (+celery, redis, psycopg2-binary, dj-database-url)
frontend/.env.production     # NEW (VITE_API_BASE_URL)
```

---

## Key Risks

1. **Redis no Railway free tier**: 128MB pode ser suficiente para Celery beat, mas se crescer muito, pode precisar de upgrade.
2. **SendGrid free tier limit**: 100 emails/dia. Com 10 usuários ativos = 10 emails/semana (lembrete) + alguns alertas = bem abaixo do limite.
3. **PostgreSQL migration**: Sem dados críticos no SQLite de dev, migração é trivial (novo banco em prod).
4. **Celery beat + Railway**: Railway pode dormir workers no free tier. Considerar usar um scheduler externo (cron-job.org) chamando um endpoint HTTP se necessário.

---

## References

- Django Celery: https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
- Railway Django: https://docs.railway.app/quick-start
- Vercel Vue: https://vercel.com/docs/frameworks/vue
- SendGrid Django: https://docs.sendgrid.com/for-developers/sending-email/django
- dj-database-url: https://github.com/jazzband/dj-database-url

