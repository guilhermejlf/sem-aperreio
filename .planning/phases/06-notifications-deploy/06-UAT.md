# Phase 6 — UAT: Notificações e Deploy

**Phase:** 06-notifications-deploy
**Status:** completed
**Date:** 2026-05-05

## Tests

| ID | Test | Status | Notes |
|----|------|--------|-------|
| NOTF-01 | Task send_weekly_reminder calcula resumo semana anterior | pass | |
| NOTF-02 | Email enviado apenas para usuários com gastos na semana | pass | |
| NOTF-03 | Template HTML renderiza total, categoria top e alerta de meta | pass | |
| NOTF-04 | Task check_monthly_average cálculo correto (6 meses excluindo atual) | pass | |
| NOTF-05 | Alerta só dispara quando gasto > média * 1.2 | pass | |
| NOTF-06 | Máximo 1 alerta por usuário por mês | pass | |
| NOTF-07 | Endpoint /api/tasks/trigger/ protegido por secret | pass | |
| NOTF-08 | Cron jobs configurados no cron-job.org (segunda 9h e 10h) | pass | |
| INFR-01 | Healthcheck /api/health/ responde {"status":"ok"} | pass | |
| INFR-02 | PostgreSQL funcional em produção | pass | |
| INFR-03 | Push no main dispara deploy automático (GitHub Actions) | pass | |
| INFR-04 | Frontend acessível via HTTPS (Vercel) | pass | |
| INFR-05 | CORS funciona em produção | pass | fallback para FRONTEND_URL |

## Verdict

**Result:** PASS (13/13)

All acceptance criteria met. No blockers.

## Production URLs
- Backend: `https://campo-valor-production.up.railway.app`
- Frontend: `https://sem-aperreio.vercel.app`
