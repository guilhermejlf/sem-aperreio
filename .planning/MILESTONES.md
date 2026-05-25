# Milestones: Sem Aperreio

## Milestone: v1.0 MVP — Autenticação, Grupos Familiares e Dashboard Inteligente

**Shipped:** 2026-04-30
**Tag:** `v1.0`
**Phases:** 4 | **Plans:** 7
**Git range:** `fcf429b` → `8a0ac9f`
**Files changed:** 11 files, +1,314/-501 LOC
**Timeline:** 2026-04-24 → 2026-04-30 (6 days)

### What Was Built

1. **Autenticação JWT completa** — Registro, login, refresh token, logout. Frontend com interceptador automático e tela de login/cadastro em tema escuro.
2. **Grupos Familiares** — Criação com código de convite de 6 caracteres, expiração de 7 dias, papéis admin/member, gerenciamento de membros (expulsar, sair, deletar grupo).
3. **Dashboard Inteligente** — Filtro por mês/ano, comparativo mês atual vs. anterior, ranking de categorias, evolução 12 meses, insights automáticos, estado vazio amigável.
4. **ML com Dados Reais** — Previsão por categoria usando LinearRegression (scikit-learn), fallback para média com poucos dados, dados históricos de contexto.
5. **Exportação CSV/Excel** — StreamingHttpResponse para CSV, openpyxl para XLSX, respeitando filtros ativos.
6. **Tema Escuro Responsivo** — Interface unificada com PrimeIcons, cards modulares, drawer de grupo, dropdown de usuário.

### What Worked

- Lazy-load do modelo ML (on-demand training) evitou startup lento
- Deep-clone + deferred init resolveu o loop de reatividade do Chart.js
- Auto-refresh de token silencioso no frontend melhorou UX sem complexidade extra
- SQLite para MVP permitiu zero-config no desenvolvimento

### What Was Inefficient

- Implementação fora do workflow formal `/gsd-execute-phase` — SUMMARY.md criados manualmente depois
- Fases implementadas em um único commit (`8a0ac9f`) — dificulta rastreamento histórico
- Sem testes automatizados — só testes manuais

### Patterns Established

- FamilyMembership como OneToOneField per user (um user = uma family)
- Pre-join gastos permanecem privados (não retroativemente linkados)
- `data_competencia` como data efetiva com fallback para `data`
- Dashboard data computed on-demand (sem cache para MVP)

### Key Lessons

- Options API do Vue 3 é suficiente para MVPs pequenos; migração para Composition pode ser feita no v2
- On-demand ML training é aceitável para datasets pequenos (< 1000 registros); persistir modelo faz sentido para scale
- StreamingHttpResponse é essencial para exportação de CSV com grandes datasets
- ConfirmDialog + Toast (PrimeVue) padrão para ações destrutivas no frontend

### Cost Observations

- Modelo: balanced (Sonnet para execução)
- Sessions: ~4-5 sessões de desenvolvimento
- Notável: Fase de dashboard (charts + reatividade) consumiu mais tokens que as outras combinadas

---

## Milestone: v3.2 Dashboard Premium — Refinamento Visual, Hierarquia e Motion System

**Shipped:** 2026-05-15
**Tag:** `v3.2`
**Phases:** 9–11 (Visual Hierarchy, Proportion Refinement, Micro Refinements) | **Plans:** 3
**Git range:** `6df3a2d` → `dfe5695`
**Files changed:** 8 files, +120/-45 LOC
**Timeline:** 2026-05-15 (1 sessão)

### What Was Built

1. **Dashboard Visual Hierarchy Refinement** — Redução de peso visual dos cards COMPORTAMENTO (fundo, borda, ícone, fonte). Aumento de respiro vertical entre blocos. Refinamento do previsão-card (mais compacto, menos banner). Gráfico de linha com gradient fill orgânico (Canvas linearGradient fade).
2. **Dashboard Proportion & Rhythm** — Largura dos insights reduzida para 92% (camada contextual elegante). Títulos de bloco refinados (menor contraste, letter-spacing reduzido). Saldo-destaque ganhou protagonismo definitivo (box-shadow sutil, hover mais refinado). Donut chart reduzido ~9% (255px vs 280px).
3. **Dashboard Micro Refinements** — Alinhamento óptico entre gráficos (padding-top 6px no line chart). Saturaçãodo card "Ainda a pagar" reduzida (~20%). Subtítulo do saldo com opacity mais suave. Pulse-risco menos chamativo. Profundidade visual ultra-sutil (radial-gradient no dashboard).
4. **Mobile Fixes** — Layout saldo-destaque corrigido (flex column, gap 12px). Saldo-valor com `clamp()` e `white-space: nowrap` para nunca quebrar linha. Previsão-card centralizado. Border-radius ajustado no mobile.

### What Worked

- Micro ajustes de CSS (~5-15% de alteração) tiveram impacto perceptivo grande na sensação premium
- `clamp()` para font-size responsivo resolveu overflow de valores grandes no mobile
- Gradient fills no Chart.js via `createLinearGradient` deram visual orgânico sem libs extras
- `max-width: 92%` nos insights criou "respiro lateral" sofisticado sem quebrar layout

### What Was Inefficient

- Onboarding Experience Phase 1 foi implementado e depois revertido pelo usuário — decisão de não incluir no milestone
- Os refinamentos foram feitos em 3 commits separados dentro de 1 sessão — poderiam ter sido consolidados

### Patterns Established

- Visual hierarchy: 3 níveis (protagonistas / secundários / terciários) com peso proporcional
- Mobile-first clamp() para fontes dinâmicas
- Canvas gradients para charts orgânicos
- `white-space: nowrap` + `clamp()` para valores monetários no mobile

### Key Lessons

- Menos é mais: ajustes de 5-10% em opacity, padding, font-size criam percepção premium
- Alinhamento óptico é mais importante que alinhamento matemático
- O dashboard deve transmitir "estabilidade financeira" — menos alertas visuais = mais confiança

---

## Milestone: v3.0 AI — Orçamento, Notificações, Deploy e Assistente Conversacional

**Shipped:** 2026-05-07
**Tag:** `v3.0`
**Phases:** 5-7 (incluindo 7.1, 7.2) | **Plans:** 6
**Git range:** `8a0ac9f` → `dae643a`
**Files changed:** 75 files, +11,256/-1,207 LOC
**Timeline:** 2026-04-30 → 2026-05-07 (7 days)

### What Was Built

1. **Orçamento e Metas** — Modelo MetaGasto com CRUD completo, dashboard integration com progress bars color-coded, alertas visuais em 80% e crítico em 100%.
2. **Notificações por Email** — Tasks semanais e alertas de média histórica via SendGrid, protegidas por endpoint com secret para cron-job.org.
3. **Infraestrutura de Produção** — PostgreSQL no Railway, CI/CD via GitHub Actions, deploy automatizado backend (Railway) + frontend (Vercel).
4. **Assistente IA Conversacional** — Parser OpenAI GPT-4o-mini com fallback regex, drawer chat com drawer lateral, FAB flutuante, confirmação de gastos/receitas.
5. **IA Contextual Multi-Etapas** — Perguntas complementares quando faltam dados (ex: "Quanto você gastou com Internet?").
6. **Continuidade Conversacional** — Detecta continuações ("e", "também"), saudações e despedidas, histórico de sessão.
7. **Exportação PDF** — Exportação de extrato para PDF com reportlab e logo personalizado.
8. **Receitas e Extrato** — CRUD de receitas com data de competência e visualização detalhada de gastos e receitas por período.

### What Worked

- Endpoint + cron-job.org como fallback para Celery no free tier funcionou bem
- PostgreSQL migration via DATABASE_URL foi transparente com Django
- Fallback parser IA funciona sem OpenAI API key (reconhecimento básico de valor e categoria)
- Drawer de IA responsivo com tema dark consistente com o app

### What Was Inefficient

- Fases 6 e 7 não tiveram SUMMARY.md criados durante execução (adicionados retrospectivamente)
- Zero testes automatizados continuam — risco técnico crescente
- Cron jobs externos (cron-job.org) ao invés de Celery Beat interno

### Patterns Established

- Config de produção via variáveis de ambiente (DATABASE_URL, EMAIL_HOST_PASSWORD)
- CORS fallback para FRONTEND_URL quando lista vazia
- Parser IA com response padronizada (intent, confirmation_required, message, data)
- sessionContext no frontend para gerenciar estado da conversa IA

### Key Lessons

- python-decouple lê .env primeiro — usar os.environ.get() para override em produção
- Vercel SPA routing precisa de "handle": "filesystem" antes do catch-all
- OpenAI GPT-4o-mini é suficiente para parsing simples de gastos; fallback regex cobre 80% dos casos
- Drawer lateral funciona melhor que modal para conversas multi-mensagem

### Cost Observations

- Modelo: balanced
- Sessions: ~3-4 sessões para fases 5-7
- Notável: Fase 7 (IA) consumiu mais tokens devido à iteração de UX do chat

---

## Milestone: v2.0 Infra & Quality — Testes, Cache, PWA e Infraestrutura

**Shipped:** 2026-05-20
**Tag:** `v2.0`
**Phases:** 12–16 (Backend Tests, Frontend Tests, Redis Cache, PWA Offline, Infra Polish) | **Plans:** 5
**Git range:** `76720a6` → `d7dd056`
**Files changed:** 25+ files
**Timeline:** 2026-05-18 → 2026-05-20 (3 sessões)

### What Was Built

1. **Backend Tests** — 55+ tests pytest cobrindo auth, family, gastos, receitas, metas, dashboard, ML, cache
2. **Frontend Tests** — 4 component tests com Vitest (EmptyState, BaseCard, DashboardInsights, ToastProvider)
3. **E2E Tests** — Playwright configurado com fluxo crítico login→dashboard→add gasto
4. **Redis Cache** — `@cached_view` decorator com TTL de 5min, invalidação automática em create/update/delete
5. **PWA Completo** — manifest.webmanifest, Service Worker via vite-plugin-pwa, offline fallback page, install prompt customizado, IndexedDB + Cache API runtime caching
6. **Infra Polish** — Celery Beat interno (django-celery-beat), rate limiting na API (100/min IP, 1000/min autenticado), anti-cache headers
7. **Cache Fix** — LocMemCache fallback com `cache.clear()` para invalidação em dev

### What Worked

- `vite-plugin-pwa` gerou SW automaticamente sem precisar de SW manual
- `cache.clear()` fallback resolveu stale data em dev (LocMemCache)
- Playwright E2E login via API + localStorage tokens bypassa verificação de email
- Rate limiting middleware customizado sem dependências externas

### What Was Inefficient

- E2E test precisa backend Django rodando em paralelo — não é self-contained
- MOB-04 (IndexedDB) e MOB-02 (Workbox) são sistemas duplicados de cache offline
- v2.0 foi implementado fora da ordem numérica (depois do v3.2) — confusão de versionamento

### Patterns Established

- `invalidate_user_cache()` padrão para invalidação após mutations
- `NetworkFirst` para API caching no Workbox (dados frescos > offline)
- `beforeinstallprompt` para install prompt customizado no PWA
- Test setup via API direto (bypass UI) para E2E de autenticação

### Key Lessons

- Cache invalidation é mais difícil que cache implementation — especialmente com LocMemCache
- Service worker residual de builds anteriores causa bugs misteriosos de stale data
- Playwright é mais confiável que Cypress para E2E moderno com SPA Vue
- Documentação deve ser atualizada junto com o código — drift de docs é perigoso

### Cost Observations

- Modelo: balanced
- Sessions: ~3 sessões para fases 12-16
- Notável: Debug de cache stale consumiu mais tempo que implementação de features

---

## Phase 17: Observability & Monitoring — Sentry, Logging, Healthchecks, Error UX

**Implemented:** 2026-05-22
**Phases:** 17 (Observability & Monitoring) | **Plan:** Ad-hoc
**Git range:** `9f1bf61` → `ae30989`
**Files changed:** 14 files
**Timeline:** 2026-05-22 (1 sessão)

### What Was Built

1. **Sentry Integration** — Frontend (Vue) + Backend (Django) + Celery workers. Captura exceptions, crashes, async failures, API failures, chunk loading errors, SW issues.
2. **Structured Logging** — Middleware com request ID, correlation ID, timing de requests, alertas para endpoints lentos (> 500ms).
3. **Detailed Healthcheck** — `/health/detailed/` com checks de PostgreSQL, Redis, Celery, SendGrid, OpenAI.
4. **ErrorBoundary UX** — Componente Vue com mensagens humanizadas ("Teu Bené teve um aperreio aqui 😅"), retry contextual, fallback para home.
5. **Performance Monitoring** — FCP, LCP, long tasks, API latency, chart render timing, chunk load errors.
6. **PWA Observability** — Tracking de offline/online, install events, SW errors, IndexedDB failures.

### What Worked

- Sentry SDK com DjangoIntegration e CeleryIntegration funcionou sem fricção
- StructuredLoggingMiddleware adicionou headers X-Request-ID e X-Response-Time em todas as responses
- ErrorBoundary captura erros de renderização Vue e envia para Sentry
- PerformanceObserver API fornece métricas reais de Web Vitals

### What Was Inefficient

- Sentry DSN precisa ser configurado via variável de ambiente (não hardcoded)
- Performance monitoring intercepta fetch global — potencial impacto mínimo mas existe
- ErrorBoundary não captura erros em event handlers (apenas render errors)

### Patterns Established

- `init_sentry()` padrão para inicialização condicional (skip se DSN ausente)
- `captureError()` + `captureMessage()` helpers para logging contextual
- Healthcheck pattern: status por serviço + response time + overall status

### Key Lessons

- Observabilidade deve ser adicionada gradualmente — não tudo de uma vez
- ErrorBoundary com mensagens humanizadas preserva identidade do produto
- Structured logging com correlation IDs é essencial para debugging distribuído

### Cost Observations

- Modelo: balanced
- Sessions: 1 sessão para Phase 17
- Notável: Sentry SDK tem boa documentação e integração suave com Django/Vue

---

## Phase 17.1: Observability Hardening & Production Activation

**Implemented:** 2026-05-22
**Phases:** 17.1 (Hardening) | **Plan:** Ad-hoc
**Git range:** `16269da` → `89f1661`
**Files changed:** 7 files
**Timeline:** 2026-05-22 (1 sessão)

### What Was Built

1. **Release Tracking** — Versão `sem-aperreio@v2.1.0` consistente entre frontend (package.json) e backend (_get_release()).
2. **Noise Filtering** — Filtros para ResizeObserver, browser extensions, AbortError benigno, erros de analytics.
3. **Source Maps** — Ativados no Vite build para debugging de stack traces em produção.
4. **Healthcheck Hardening** — Timeout-safe, Celery sem bloqueio (inspect removido), Redis com fallback rápido.
5. **ErrorBoundary Recovery** — Chunk errors disparam reload automático da página.
6. **Repository Cleanup** — .gitignore atualizado com test-results, coverage, playwright-report, .sentryclirc.
7. **CI/CD Validation** — Workflow GitHub Actions validado com working-directory correto.

### What Worked

- Healthcheck responde em ~4ms total em dev
- Release tracking unificado entre frontend e backend
- Noise filtering reduz significativamente o volume de erros no Sentry
- Source maps não quebram o build

### Key Lessons

- Healthcheck detalhado precisa ser timeout-safe para não bloquear requisições
- `BrowserTracing` foi removido na Sentry v8 — usar `browserTracingIntegration()`
- Source maps são essenciais para debugging em produção mas devem ser gerados apenas no build

### Production Activation Checklist

- [x] Railway: `SENTRY_DSN`, `ENVIRONMENT=production`, `RELEASE=sem-aperreio@v2.1.0` — variáveis documentadas, aguardando configuração no dashboard
- [x] Vercel: `VITE_SENTRY_DSN`, `VITE_ENVIRONMENT=production`, `VITE_RELEASE=sem-aperreio@v2.1.0` — variáveis documentadas, aguardando configuração no dashboard
- [x] CORS fix: frontend sempre permitido em produção (`a241c43`)
- [x] Auth redirect: redireciona para login quando token expira (`aba481f`)
- [x] Healthcheck version: 2.1.0 em ambos endpoints
- [x] Sentry frontend ingest: ✅ confirmado — eventos chegando ao dashboard do Sentry
- [x] Sentry backend ingest: ✅ confirmado — exceptions e mensagens chegando ao dashboard do Sentry
