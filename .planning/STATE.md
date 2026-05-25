# Project State

## Current Milestone

**Milestone:** v2.0 Infra & Quality — SHIPPED (2026-05-19)
**Phase:** 17.1 — Observability Hardening & Production Activation
**Plan:** `.planning/ROADMAP-v2.0.md`
**Status:** Phase 17 + 17.1 COMPLETE (observability ativa em producao)
**Phase 17.2:** Production Activation Closure — IN PROGRESS
**Last activity:** 2026-05-25 — CORS fix, auth redirect, healthcheck version, docs sync

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
- ✅ Phase 15: PWA Offline — DONE (2026-05-20)
  - Manifest + IndexedDB + OfflineFallback + InstallPrompt + vite-plugin-pwa SW
- ✅ Phase 16: Infra Polish — DONE (2026-05-19)
- ✅ Phase 17: Observability & Monitoring — DONE (2026-05-22)
- ✅ Phase 17.1: Hardening & Production Activation — DONE (2026-05-22)
  - Sentry frontend/backend, structured logging, detailed healthchecks, error UX

**Planning artifacts:**
- `.planning/REQUIREMENTS-v2.0.md` — 16 requirements defined
- `.planning/ROADMAP-v2.0.md` — 5 phases with dependencies

**Deferred:**
- v3.1 Auth Polish — After v2.0
- v3.3 Onboarding Experience — Backlog

## Recent Commits

- `aba481f` fix(auth): redirect para login quando token expira — 2026-05-25
- `a241c43` fix(cors): simplifica CORS para sempre permitir frontend em producao — 2026-05-25
- `89f1661` Phase 17.1: Observability Hardening — release tracking, noise filtering, source maps, CI validado — 2026-05-22
- `ae30989` Phase 17: Observability & Monitoring — Sentry, structured logging, healthchecks, error UX — 2026-05-22
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
- [x] Phase 15: PWA Offline — manifest.webmanifest, IndexedDB cache, OfflineFallback, InstallPrompt, vite-plugin-pwa SW ✅
- [x] Phase 16: Infra Polish — Celery Beat, rate limiting, periodic tasks ✅
- [x] Phase 17: Observability & Monitoring — Sentry, logging, healthchecks, error UX ✅
- [x] Phase 17.1: Hardening — release tracking, noise filtering, source maps, CI/CD validated, .gitignore cleanup ✅
- [ ] Phase 17.2: Production Activation Closure — DSNs, ingest validation, docs sync, operational test

## Accumulated Context

- Options API no Vue — Composition API migration candidate for next milestone
- PostgreSQL em produção (Railway) — SQLite mantido para dev
- ML model on-demand training — consider Celery/persisted model for large datasets
- 55+ automated backend tests (pytest) covering auth, family, gastos, receitas, metas, dashboard, and cache
- 4 frontend tests (Vitest) para EmptyState, BaseCard, DashboardInsights, ToastProvider
- Pagination partial (simple limit, no full metadata)
- Git tag v1.0 pushado para origin
- Git tag v3.0 criado (push pending)
- Celery Beat interno ativo (django-celery-beat) — cron-job.org mantido como backup
- Cache backend com invalidação automática em create/update/delete
- PWA completo: manifest + IndexedDB + OfflineFallback + InstallPrompt + vite-plugin-pwa SW
- Playwright E2E configurado (fluxo crítico login→dashboard→add gasto)
- Email verification disabled for testing — `email_verified=True` on register; login bypasses check
- Assistente IA funcional com fallback regex
- Deploy automatizado (GitHub Actions → Railway + Vercel)
- Dashboard com visual hierarchy madura (3 níveis), motion system oficial, mobile-first consolidado
- `clamp()` para fontes dinâmicas no mobile
- Canvas gradients para charts orgânicos
- Sentry integrado (frontend Vue + backend Django + Celery)
- Structured logging com request/correlation IDs
- Detailed healthcheck (/health/detailed) com checks de DB, Redis, Celery, email, OpenAI
- ErrorBoundary com UX premium e mensagens humanizadas
- Performance monitoring: FCP, LCP, long tasks, API latency, chunk errors
- PWA observability: offline/online, SW events, install tracking, IndexedDB errors
- Release tracking: sem-aperreio@v2.1.0 (frontend package.json + backend _get_release())
- Noise filtering: ResizeObserver, extensions, AbortError, analytics errors
- Source maps ativados no Vite build para debugging em producao
- Healthcheck timeout-safe: Celery sem bloqueio, Redis com fallback rapido
- ErrorBoundary: recovery automatico para chunk errors (page reload)
- .gitignore: test-results, coverage, playwright-report, .sentryclirc
- CI/CD validado: working-directory correto no workflow, npm ci + build passando
