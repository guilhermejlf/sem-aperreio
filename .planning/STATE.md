# Project State

## Current Milestone

**Milestone:** v2.0 Infra & Quality — IN PROGRESS
**Phase:** 16 — Infra Polish
**Plan:** `.planning/ROADMAP-v2.0.md`
**Status:** Phase 16 completed (2026-05-19)
**Last activity:** 2026-05-19 — Celery Beat scheduler, periodic tasks, rate limiting middleware

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
- ✅ Phase 12: Backend Tests — DONE
- ✅ Phase 13: Frontend Tests — DONE
- ✅ Phase 14: Redis Cache — DONE (2026-05-18)
- ✅ Phase 15: PWA Offline — DONE (2026-05-18)
- ✅ Phase 16: Infra Polish — DONE (2026-05-19)

**Planning artifacts:**
- `.planning/REQUIREMENTS-v2.0.md` — 16 requirements defined
- `.planning/ROADMAP-v2.0.md` — 5 phases with dependencies

**Deferred:**
- v3.1 Auth Polish — After v2.0
- v3.3 Onboarding Experience — Backlog

## Recent Commits

- `phase-15` Phase 15: PWA Offline — service worker, install prompt, IndexedDB cache — 2026-05-18
- `76720a6` Phase 14: Redis Cache — caching and invalidation for ML predictions and metas — 2026-05-18
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
- [x] Phase 12: Backend Tests — 55 tests passing ✅
- [x] Phase 13: Frontend Tests — Vitest configured ✅
- [x] Phase 14: Redis Cache — decorators, invalidation, graceful fallback ✅
- [x] Phase 15: PWA Offline — service worker, install prompt, IndexedDB cache ✅
- [x] Phase 16: Infra Polish — Celery Beat, rate limiting, periodic tasks ✅

## Accumulated Context

- Options API no Vue — Composition API migration candidate for next milestone
- PostgreSQL em produção (Railway) — SQLite mantido para dev
- ML model on-demand training — consider Celery/persisted model for large datasets
- 55 automated backend tests (pytest) covering auth, family, gastos, receitas, metas, dashboard, and cache
- Pagination partial (simple limit, no full metadata)
- Git tag v1.0 pushado para origin
- Git tag v3.0 criado (push pending)
- Celery Beat interno ativo (django-celery-beat) — cron-job.org mantido como fallback
- Assistente IA funcional com fallback regex
- Deploy automatizado (GitHub Actions → Railway + Vercel)
- Dashboard com visual hierarchy madura (3 níveis), motion system oficial, mobile-first consolidado
- `clamp()` para fontes dinâmicas no mobile
- Canvas gradients para charts orgânicos
