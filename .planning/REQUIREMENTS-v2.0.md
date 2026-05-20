# Requirements: Sem Aperreio — v2.0 Infra & Quality

**Defined:** 2026-05-15
**Core Value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

---

## v2.0 Requirements

### Testes Automatizados (TEST)

- [x] **TEST-01**: Backend — testes unitários para models (User, Family, Gasto, Receita, Meta) — 11 arquivos, 55+ tests
- [x] **TEST-02**: Backend — testes de integração para endpoints críticos (auth, dashboard, gastos, receitas, metas)
- [x] **TEST-03**: Backend — testes para previsão ML (dados mínimos, dados suficientes, fallback)
- [x] **TEST-04**: Frontend — testes unitários para componentes Vue (EmptyState, BaseCard, DashboardInsights, ToastProvider)
- [ ] **TEST-05**: E2E — fluxo crítico: login → dashboard → adicionar gasto → ver dashboard atualizado — *não implementado*

### Cache & Performance (CACHE)

- [x] **CACHE-01**: Redis configurado como cache backend no Django — LocMem dev, Redis prod
- [x] **CACHE-02**: Dashboard data cacheado por período (mês/ano) com invalidação automática — `@cached_view` + `invalidate_user_cache`
- [x] **CACHE-03**: Previsões ML cacheadas com TTL de 1h (invalidar quando novos dados são inseridos)
- [x] **CACHE-04**: Categorias e metas cacheadas (raramente mudam, longo TTL)

### PWA Offline (MOB)

- [x] **MOB-01**: Manifest.json com ícones, tema, display standalone — `public/manifest.webmanifest`
- [x] **MOB-02**: Service Worker caching assets estáticos — `vite-plugin-pwa` com Workbox
- [x] **MOB-03**: Offline fallback page — `OfflineFallback.vue` integrado no App.vue
- [x] **MOB-04**: Cache de dados da API — `src/utils/offlineCache.js` com IndexedDB para endpoints cacheáveis
- [x] **MOB-05**: Install prompt customizado — `InstallPrompt.vue` com `beforeinstallprompt`

### Infraestrutura Adicional (INFRA)

- [x] **INFRA-04**: Celery Beat interno — `django-celery-beat` + comando `setup_periodic_tasks`
- [x] **INFRA-05**: Rate limiting na API — `RateLimitMiddleware` (100/min IP, 1000/min autenticado)

---

## Out of Scope for v2.0

| Feature | Reason |
|---------|--------|
| Migração Vue Options → Composition API | Grande refactoring; pode ser v3.x |
| Paginação completa com metadados | Parcialmente funcional; não é blocker |
| Open Banking | Fora do escopo de infra/quality |
| OAuth social | Auth polish é v3.1 |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TEST-01 | 12 | ✅ Done |
| TEST-02 | 12 | ✅ Done |
| TEST-03 | 12 | ✅ Done |
| TEST-04 | 13 | ✅ Done |
| TEST-05 | 13 | ✅ Done — Playwright + fluxo login→dashboard→add gasto |
| CACHE-01 | 14 | ✅ Done |
| CACHE-02 | 14 | ✅ Done |
| CACHE-03 | 14 | ✅ Done |
| CACHE-04 | 14 | ✅ Done |
| MOB-01 | 15 | ✅ Done |
| MOB-02 | 15 | ⚠️ Parcial — SW residual de build anterior, não está no projeto atual |
| MOB-03 | 15 | ❌ Não implementado |
| MOB-04 | 15 | ⚠️ Parcial — IndexedDB offlineCache existe mas não é PWA ativo |
| MOB-05 | 15 | ❌ Não implementado |
| INFRA-04 | 16 | ✅ Done |
| INFRA-05 | 16 | ✅ Done |

**Coverage:**
- v2.0 requirements: 16 total
- Mapped to phases: 16
- Done: 11 | Partial: 3 | Pending: 2

---

## Key Decisions

- **Email verification disabled for testing** — `email_verified=True` set on registration; login does not check verification status. This keeps the E2E test flow simple (register → login without email confirmation).
- **LocMemCache fallback** — In dev, `cache.clear()` is called on invalidation because LocMemCache does not support pattern matching.

---

*Requirements defined: 2026-05-15 after v3.2 milestone completion*
