# Project State

## Current Milestone

**Milestone:** v3.2 Dashboard Premium — SHIPPED
**Phase:** 11 — Micro Refinements Premium
**Plan:** —
**Status:** Shipped (2026-05-15)
**Last activity:** 2026-05-15 — dashboard micro refinements + mobile fixes

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-05-15)
See: `.planning/MILESTONES.md` (v1.0 + v3.0 + v3.2 retrospective)

**Core value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

## Previous Milestones

- ✅ v1.0 MVP — SHIPPED (2026-04-30) — Auth JWT, Family Groups, Dashboard, ML + Export
- ✅ v3.0 AI — SHIPPED (2026-05-07) — Budget, Notifications, Deploy, AI Assistant
- ✅ v3.2 Dashboard Premium — SHIPPED (2026-05-15) — Visual Hierarchy, Motion System, Mobile Polish

## What's Next

**Current milestone:** v2.0 Infra & Quality — STARTED

**Phases:**
- Phase 12: Backend Tests — Pending
- Phase 13: Frontend Tests — Pending
- Phase 14: Redis Cache — Pending
- Phase 15: PWA Offline — Pending
- Phase 16: Infra Polish — Pending

**Planning artifacts:**
- `.planning/REQUIREMENTS-v2.0.md` — 16 requirements defined
- `.planning/ROADMAP-v2.0.md` — 5 phases with dependencies

**Deferred:**
- v3.1 Auth Polish — After v2.0
- v3.3 Onboarding Experience — Backlog

## Recent Commits

- `dfe5695` fix(dashboard): ajustes mobile — layout saldo e centralização previsão — 2026-05-15
- `1aee9bf` refine(dashboard): micro refinamentos premium — alinhamento, saturação, profundidade — 2026-05-15
- `0b8a777` refine(dashboard): proporção, protagonismo e ritmo visual fino — 2026-05-15
- `d0d5428` refine(dashboard): hierarquia visual e densidade perceptiva — 2026-05-15
- `6df3a2d` refine(intelligence): refinamento visual dos insights contextuais — 2026-05-15

## Active TODOs

- [x] Phase 9: Dashboard Visual Hierarchy Refinement — implementado ✅
- [x] Phase 10: Dashboard Proportion & Rhythm — implementado ✅
- [x] Phase 11: Dashboard Micro Refinements — implementado ✅
- [x] Mobile fixes: saldo clamp(), previsão centralizado, layout bloco-situacao ✅

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
- Dashboard com visual hierarchy madura (3 níveis), motion system oficial, mobile-first consolidado
- `clamp()` para fontes dinâmicas no mobile
- Canvas gradients para charts orgânicos
