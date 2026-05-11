# Phase 6 - Infra Summary: PostgreSQL, CI/CD e Deploy

**Phase:** 06-notifications-deploy
**Plan:** 06-02 (infraestrutura)
**Status:** Completed
**Date:** 2026-05-05

## What Was Built

### PostgreSQL Migration
- `DATABASE_URL` via `os.environ.get()` (python-decouple ignorava .env em producao)
- Railway PostgreSQL add-on provisionado; migrations aplicadas com sucesso
- SQLite mantido como fallback local

### Railway (Backend)
- Deploy: `campo-valor-production.up.railway.app`
- `railway.json` + `Procfile` configurados
- Healthcheck: `/api/health/` retorna `{"status":"ok"}`
- Variaveis: DATABASE_URL, SECRET_KEY, EMAIL_HOST_PASSWORD, TASK_TRIGGER_SECRET, FRONTEND_URL, DEBUG=False

### Vercel (Frontend)
- Deploy: `https://sem-aperreio.vercel.app`
- `vercel.json` com SPA routing (filesystem handle antes do catch-all)
- `VITE_API_BASE_URL` aponta para backend production

### CI/CD GitHub Actions
- `.github/workflows/deploy.yml`: check + deploy backend (Railway) + deploy frontend (Vercel)
- Trigger: push na branch `main`
- Secrets: RAILWAY_TOKEN, VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID

### CORS Fix
- CORS_ALLOWED_ORIGINS fallback para FRONTEND_URL quando lista vazia
- Resolvido bloqueio de cross-origin em producao

### Files Created/Modified
- `backend/settings/base.py` (DATABASE_URL, CORS, email)
- `railway.json`
- `Procfile`
- `.github/workflows/deploy.yml`
- `frontend/vercel.json`
- `frontend/src/config/api.js` (default API URL para producao)

## Verification
- [x] Healthcheck responde 200
- [x] PostgreSQL funcional em producao
- [x] Push no `main` dispara deploy automatico
- [x] Frontend acessivel via HTTPS
- [x] Frontend consegue chamar API do backend (CORS OK)
- [x] Dados persistem em PostgreSQL

## Production URLs
- Backend: `https://campo-valor-production.up.railway.app`
- Frontend: `https://sem-aperreio.vercel.app`
