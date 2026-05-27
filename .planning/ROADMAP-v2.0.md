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
| 17 | Observability | Sentry, logging, healthchecks | Phase 16 |
| 17.1 | Hardening | Release tracking, noise filtering | Phase 17 |
| 17.2 | Production Activation | DSN config, ingest validation | Phase 17.1 |
| 18 | Premium Statement | Timeline, componentização extrato | Phase 17.2 |
| 18.1 | Visual Harmonization | Design system, spacing, motion | Phase 18 |
| 18.4 | KPI Layout Mobile | Grid simplificado, labels reduzidas | Phase 18.1 |

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

## Phase 17 — Observability & Monitoring

**Goal:** Visibilidade completa do sistema em produção com rastreamento de erros, logging estruturado e healthchecks.

**Deliverables:**
- Sentry Integration — Frontend (Vue) + Backend (Django) + Celery workers
- Structured Logging — Middleware com request ID, correlation ID, timing
- Detailed Healthcheck — `/health/detailed/` com checks de PostgreSQL, Redis, Celery, SendGrid, OpenAI
- ErrorBoundary UX — Mensagens humanizadas, retry contextual, fallback para home
- Performance Monitoring — FCP, LCP, long tasks, API latency
- PWA Observability — Tracking de offline/online, install events, SW errors

**Verification:**
- Sentry recebe eventos de frontend e backend
- Healthcheck responde < 500ms com todos os serviços OK
- ErrorBoundary captura erros de renderização Vue

**Files:**
- `frontend/src/utils/sentry.js`
- `backend/settings/sentry.py`
- `api/middleware.py` (StructuredLoggingMiddleware)
- `api/healthcheck.py`
- `frontend/src/components/ErrorBoundary.vue`

---

## Phase 17.1 — Hardening & Production Activation

**Goal:** Preparar o sistema para produção com hardening de observabilidade.

**Deliverables:**
- Release Tracking — Versão `sem-aperreio@v2.1.0` consistente entre frontend e backend
- Noise Filtering — Filtros para ResizeObserver, browser extensions, AbortError
- Source Maps — Ativados no Vite build para debugging de stack traces
- Healthcheck Hardening — Timeout-safe, Celery sem bloqueio, Redis com fallback
- ErrorBoundary Recovery — Chunk errors disparam reload automático
- Repository Cleanup — .gitignore atualizado

**Verification:**
- Release aparece corretamente em todos os eventos Sentry
- Healthcheck responde em ~4ms total em dev
- Source maps não quebram o build

**Files:**
- `frontend/vite.config.js` (source maps)
- `frontend/package.json` (version)
- `backend/settings/base.py` (_get_release)

---

## Phase 17.2 — Production Activation Closure

**Goal:** Validar que a observabilidade está 100% funcional em produção.

**Deliverables:**
- Sentry Ingest Validation — Confirmação de eventos chegando ao dashboard
- CORS Fix — Simplificação para sempre permitir frontend em produção
- Auth Redirect — Redirecionamento automático para login quando token expira
- Docs Sync — Atualização de STATE.md, PROJECT.md, MILESTONES.md

**Verification:**
- Sentry frontend ingest: 200 OK confirmado
- Sentry backend ingest: exceptions e mensagens chegando
- Deploy automatizado funcional após CORS fix

---

## Phase 18 — Premium Statement Experience

**Goal:** Elevar a experiência do extrato com timeline organizada e componentização premium.

**Deliverables:**
- Timeline Organizada — Agrupamento de transações por data
- Componentização Premium — 7 componentes no namespace `statement/`
  - `StatementTimeline`, `StatementGroup`, `StatementItem`
  - `StatementFilters`, `StatementSummary`, `StatementEmptyState`, `StatementSkeleton`
- Filtros Adaptativos — Por período, categoria, tipo e status
- Utility `timeline.js` — Agrupamento com formatação relativa

**Verification:**
- Extrato renderiza corretamente com dados agrupados por data
- Filtros funcionam em conjunto (AND lógico)
- Stagger animation suave na entrada

**Files:**
- `frontend/src/components/statement/*.vue`
- `frontend/src/utils/timeline.js`
- `frontend/src/components/ExtratoView.vue`

---

## Phase 18.1 — Visual Harmonization

**Goal:** Consistência visual e motion system no extrato.

**Deliverables:**
- Design System Consistente — Cores, spacing e tipografia alinhados
- Spacing Refinado — Padding, gap e margin harmonizados
- Motion System — Transições de hover e entrada consistentes
- Mobile Polish — Ajustes de font-size e padding

**Verification:**
- Lighthouse audit: nenhum layout shift inesperado
- Consistência visual entre todos os componentes `statement/`

---

## Phase 18.4 — KPI Layout Simplification (mobile)

**Goal:** Otimizar o layout mobile dos KPIs do extrato.

**Deliverables:**
- Grid sem Scroll — `grid-template-columns: repeat(2, minmax(0, 1fr))`
- Saldo em Destaque — Layout reestruturado para destacar saldo
- Labels Reduzidas — 8px labels, 13px valores no mobile
- Ajustes Finais — Padding, gap, border-radius otimizados

**Verification:**
- Sem scroll horizontal no mobile
- Todos os KPIs visíveis sem quebra
- Legibilidade mantida com labels reduzidas

**Files:**
- `frontend/src/components/statement/StatementSummary.vue`

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
