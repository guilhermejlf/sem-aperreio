# Phase 6 - Backend Summary: Notificacoes e Jobs

**Phase:** 06-notifications-deploy
**Plan:** 06-01 (backend)
**Status:** Completed
**Date:** 2026-05-05

## What Was Built

### api/tasks.py
- `send_weekly_reminder()` — resumo semanal por email com total gasto, categoria top, meta proxima do limite
- `check_monthly_average()` — alerta quando gasto do mes atual ultrapassa media dos ultimos 6 meses + 20%
- Templates HTML: `weekly_reminder.html`, `average_alert.html`, `base_email.html` (dark theme)
- Duplicata evitada: maximo 1 alerta por usuario/mes

### api/views_notificacoes.py
- `POST /api/tasks/trigger/` — endpoint protegido por secret (TASK_TRIGGER_SECRET) para cron-job.org
- Suporta task=reminder|average|all
- Retorna 403 se secret incorreto

### Configuracao de Email
- SendGrid SMTP via variaveis de ambiente
- Fallback para console backend em dev quando senha ausente
- Railway: EMAIL_HOST_PASSWORD configurado

### Cron Jobs
- cron-job.org: 2 jobs semanais (segunda 9h e 10h) apontando para production URL
- Nota: Celery worker/beat nao rodou no Railway free tier; fallback para endpoint + cron funcionou

### Files Created/Modified
- `api/tasks.py`
- `api/templates/emails/base_email.html`
- `api/templates/emails/weekly_reminder.html`
- `api/templates/emails/average_alert.html`
- `api/views_notificacoes.py`
- `backend/settings/base.py` (email config, CORS fallback)

## Verification
- [x] Tasks executam via endpoint de trigger
- [x] Email enviado em producao (SendGrid)
- [x] Calculo de media historica correto
- [x] Duplicata de alerta evitada
- [x] Secret protege contra chamadas nao autorizadas
