# ROADMAP: Sem Aperreio — v2.0 Infra & Quality

**Milestone:** v2.0
**Objective:** Elevar a qualidade técnica do produto com testes, performance e experiência mobile avançada.
**Timeline Estimate:** 2–3 semanas

---

## Phase Overview

| Phase | Name | Focus | Depends On |
|-------|------|-------|------------|
| 12 | Backend Tests | pytest + Django test client | — |
| 13 | Frontend Tests | Vitest + component testing | Phase 12 |
| 14 | Redis Cache | Cache backend + invalidation | Phase 12 |
| 15 | PWA Offline | Manifest, SW, offline support | Phase 13 |
| 16 | Infra Polish | Celery Beat, rate limiting | Phase 14 |

---

## Phase 12 — Backend Tests

**Goal:** Backend coberto por testes unitários e de integração.

**Deliverables:**
- `pytest` configurado com `pytest-django`
- Fixtures para User, Family, Gasto, Receita, Meta
- Testes de integração para endpoints críticos:
  - Auth: registro, login, refresh, logout
  - Family: criação, convite, entrada, saída
  - Gastos: CRUD, filtros, pagamento
  - Receitas: CRUD
  - Metas: CRUD, alertas
  - Dashboard: dados por período
- Testes para ML: dados mínimos → fallback, dados suficientes → previsão real

**Verification:**
- `pytest` passa com >80% de cobertura nos módulos críticos
- CI/CD roda testes antes de deploy

**Files:**
- `backend/pytest.ini`
- `backend/conftest.py`
- `backend/api/tests/`

---

## Phase 13 — Frontend Tests

**Goal:** Componentes críticos do frontend testados.

**Deliverables:**
- `vitest` configurado no projeto Vite
- Testes unitários para:
  - `EmptyState.vue` — renderização, props, eventos
  - `BaseCard.vue` — slots, badges, ações
  - `DashboardInsights.vue` — insights gerados corretamente
  - `ToastProvider.vue` — toast show/hide
- Testes de composição:
  - DashboardCharts carrega e renderiza
  - App.vue troca de tabs corretamente
- E2E: Playwright ou Cypress
  - Fluxo: login → dashboard → adicionar gasto → ver saldo atualizado

**Verification:**
- `npm run test` passa
- E2E passa em headless

**Files:**
- `frontend/vitest.config.js`
- `frontend/src/components/**/*.test.js`
- `frontend/e2e/`

---

## Phase 14 — Redis Cache

**Goal:** Dashboard e previsões respondem mais rápido com cache inteligente.

**Deliverables:**
- Redis configurado como `CACHES` no Django settings
- Cache por view: `dashboard_data:{user_id}:{mes}:{ano}` com TTL de 5min
- Cache de previsões ML com TTL de 1h
- Invalidação automática:
  - Quando gasto/receita/meta é criada/atualizada/deletada
  - Quando usuário muda de família
- Cache de categorias e metas com TTL longo (24h)
- Fallback: se Redis não disponível, buscar do banco (graceful degradation)

**Verification:**
- Dashboard carrega < 200ms com cache (vs > 500ms sem)
- Invalidação funciona corretamente (teste de integração)
- Sem erros se Redis cair

**Files:**
- `backend/settings/base.py` (CACHES config)
- `backend/api/cache_utils.py`
- Decoradores `@cache_dashboard` e `@cache_prediction`

---

## Phase 15 — PWA Offline

**Goal:** App funciona offline para leitura e instala como app nativo.

**Deliverables:**
- `manifest.json` com ícones, tema escuro, display standalone
- Service Worker via `vite-pwa-plugin` ou workbox manual
- Cache de assets: JS bundles, CSS, fonts, PrimeIcons
- Cache de dados: IndexedDB ou Cache API para dashboard atual e metas
- Offline fallback page ("Você está offline — dados do último acesso disponíveis")
- Install prompt customizado (botão "Instalar app" no header/settings)

**Verification:**
- Lighthouse PWA audit: score > 90
- App instala em Android/iOS
- Dashboard abre offline com dados cacheados
- Novos dados sincronizam quando online

**Files:**
- `frontend/public/manifest.json`
- `frontend/vite.config.js` (vite-pwa-plugin)
- `frontend/src/sw.js`
- `frontend/src/components/InstallPrompt.vue`

---

## Phase 16 — Infra Polish

**Goal:** Infraestrutura robusta e self-contained.

**Deliverables:**
- Celery Beat interno (migrar de cron-job.org)
  - Scheduler Django + tasks periódicas
  - Weekly reminder (segunda 9h)
  - Average alert (segunda 10h)
- Rate limiting na API
  - `django-ratelimit` ou custom middleware
  - 100 req/min por IP, 1000 req/min por usuário autenticado
  - Headers `X-RateLimit-*` na resposta

**Verification:**
- Tasks rodam localmente (sem cron-job.org)
- Rate limit bloqueia excesso e retorna 429
- Logs de tasks acessíveis

**Files:**
- `backend/celerybeat_schedule.py`
- `backend/api/ratelimit.py`

---

## Success Criteria for v2.0

1. **Testes:** `pytest` passa, cobertura > 80% nos módulos críticos
2. **Performance:** Dashboard < 200ms com cache ativo
3. **Mobile:** PWA instalável, funciona offline para leitura
4. **Infra:** Sem dependências externas de cron (Celery Beat)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Redis não disponível no Railway free tier | Medium | High | Graceful fallback para SQLite/memory cache |
| PWA caching quebra deploy (assets stale) | Medium | Medium | Versioned assets + skipWaiting no SW |
| Testes de ML lentos ou não-determinísticos | Low | Medium | Mock sklearn para testes unitários |
| Celery Beat consome muitos recursos | Low | Low | Use short polling interval (1min) no free tier |

---

*Roadmap defined: 2026-05-15*
