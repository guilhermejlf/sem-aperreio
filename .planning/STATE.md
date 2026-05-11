# Project State

## Current Milestone

**Milestone:** Next — TBD
**Phase:** None
**Status:** Planning next milestone
**Last activity:** 2026-05-11 — v3.0 milestone completed and archived

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-11)
See: `.planning/MILESTONES.md` (v1.0 + v3.0 retrospective)

**Core value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

## Previous Milestones

- ✅ v1.0 MVP — SHIPPED (2026-04-30) — Auth JWT, Family Groups, Dashboard, ML + Export
- ✅ v3.0 AI — SHIPPED (2026-05-07) — Budget, Notifications, Deploy, AI Assistant

## What's Next

Run `/gsd-new-milestone` to define next milestone.

Backlog items:
- TEST-01: Testes automatizados
- CACHE-01: Cache Redis
- MOB-01: PWA offline
- BANK-01: Open Banking avaliação
- CRON-01: Celery Beat interno

## Recent Commits

- `cc3c963` chore: remove REQUIREMENTS.md for v1.0 milestone — 2026-04-30
- `ed7c783` chore: archive v1.0 milestone files — 2026-04-30
- `8a0ac9f` feat: implementa fases 1-3 do v1(auth, family, dashboard) — 2026-04-30
- `fcf429b` Initial commit - projeto limpo — 2026-04-24

## Active TODOs

- [x] Criar REQUIREMENTS.md para v2.0
- [x] Criar ROADMAP.md para v2.0 (Phases 5–6)
- [x] Phase 5 discuss-phase: decisões capturadas em `05-CONTEXT.md`
- [x] Phase 5 plan-phase: `05-01-PLAN.md` (backend) e `05-02-PLAN.md` (frontend) criados
- [x] Phase 5 ui-spec: `05-UI-SPEC.md` criado
- [x] Phase 5 execute-phase: implementar Budget models, endpoints, e UI ✅
- [x] Phase 5 review: bugs fixed (formatarValor, category filtering, delete UI)
- [x] Phase 6 discuss-phase: decisões capturadas em `06-CONTEXT.md`
- [x] Phase 6 plan-phase: `06-01-PLAN.md` (backend notificações) e `06-02-PLAN.md` (infraestrutura/deploy) criados
- [x] Phase 6 execute-phase: implementar notificações + PostgreSQL + CI/CD + deploy ✅
- [x] Phase 7 discuss-phase: decisões capturadas em `07-CONTEXT.md`
- [x] Phase 7 plan-phase: `07-01-PLAN.md` criado
- [x] Phase 7 execute-phase: implementar IA parser + drawer chat + FAB ✅
- [x] Phase 7 review: testes manuais end-to-end ✅
- [x] Phase 7.1 discuss-phase: contextual multi-etapas (sem discuss formal, feature rapida)
- [x] Phase 7.1 execute-phase: implementar contexto + perguntas complementares ✅
- [x] Phase 7.2 execute-phase: implementar continuidade conversacional + saudacoes + fim de conversa ✅

## Accumulated Context

- Options API no Vue — Composition API migration candidate for next milestone
- PostgreSQL em produção (Railway) — SQLite mantido para dev
- ML model on-demand training — consider Celery/persisted model for large datasets
- No automated tests — only manual testing performed
- Pagination partial (simple limit, no full metadata)
- Git tag v1.0 pushado para origin
- Git tag v3.0 criado (push pending)
- Cron jobs externos (cron-job.org) — Celery Beat interno candidato para upgrade
- Assistente IA funcional com fallback regex
- Deploy automatizado (GitHub Actions → Railway + Vercel)
