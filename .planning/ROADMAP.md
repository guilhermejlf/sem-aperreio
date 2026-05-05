# Roadmap: Sem Aperreio

**Project:** Sem Aperreio — Controle de Gastos Doméstico
**Defined:** 2026-04-24
**Current Milestone:** v2 — Orçamento, Notificações e Deploy

---

## Milestones

- ✅ **v1.0 MVP** — Phases 1-4 (shipped 2026-04-30)
- ✅ **v2.0 Production** — Shipped 2026-05-05

---

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) — SHIPPED 2026-04-30</summary>

### Phase 1 — Autenticação JWT (2 plans)
- [x] Backend JWT: djangorestframework-simplejwt, endpoints auth
- [x] Frontend auth: telas login/cadastro, token storage, interceptador, logout

### Phase 2 — Grupo Familiar + Refatoração de Gastos (2 plans)
- [x] Backend: Family/FamilyMembership models, FamilyViewSet, gastos filtrados por family
- [x] Frontend: FamilyView.vue, drawer, badge no header, gerenciamento de membros

### Phase 3 — Dashboard Inteligente com Filtros (2 plans)
- [x] Backend: endpoint `/api/dashboard/` com agregações, ranking, comparativo
- [x] Frontend: seletor mês/ano, cards responsivos, gráficos Chart.js, estado vazio

### Phase 4 — ML com Dados Reais + Exportação (1 plan)
- [x] ML: previsão por categoria via LinearRegression, fallback média
- [x] Export: CSV (StreamingHttpResponse), XLSX (openpyxl)

See archive: `.planning/milestones/v1.0-ROADMAP.md`
</details>

### Phase 5 — Orçamento e Metas ✅ SHIPPED 2026-05-04

**Goal:** Usuários podem definir metas de gasto por categoria e acompanhar progresso no dashboard.

**Depends on:** v1.0 (all phases)

**Requirements:** BUDG-01, BUDG-02, BUDG-03

**Deliverables:**
- ✅ Modelo `MetaGasto` (categoria, valor meta, mês/ano, usuário)
- ✅ Endpoint CRUD `/api/metas/` com campos computados (gasto_realizado, percentual, status)
- ✅ Dashboard integration — `/api/dashboard/` retorna `metas` (geral + por_categoria)
- ✅ Frontend: `BudgetView.vue` com seletor de período, meta geral, grid de categorias
- ✅ Frontend: `BudgetEditModal.vue` com confirmação ao editar meta com gastos existentes
- ✅ Dashboard mini block — progress bars de metas entre comportamento e gráficos
- ✅ App.vue: nova aba "Metas" (`pi pi-bullseye`) com `BudgetView`
- ✅ Dashboard: barra de progresso por categoria
- ✅ Alerta visual quando gasto ultrapassa 80% da meta (toast + dashboard insights)
- ✅ Alerta crítico quando > 100%

**Verification:**
- [x] Usuário define meta de R$ 500 para "Mercado"
- [x] Dashboard mostra progresso "R$ 320 / R$ 500 (64%)"
- [x] Alerta aparece quando gasto > 80% da meta (toast warn + dashboard warning)
- [x] Alerta muda para crítico quando > 100% (toast error + dashboard alert)

---

### Phase 6 — Notificações e Deploy ✅ SHIPPED 2026-05-05

**Goal:** Notificações push/email e infraestrutura de produção (PostgreSQL, CI/CD, deploy).

**Depends on:** Phase 5

**Requirements:** NOTF-01, NOTF-02, INFR-01, INFR-02, INFR-03

**Deliverables:**
- ✅ Tasks de notificação: `send_weekly_reminder`, `check_monthly_average` (`api/tasks.py`)
- ✅ Endpoint `/api/tasks/trigger/` protegido por secret (para cron-job.org)
- ✅ SendGrid SMTP configurado (settings + Railway env vars)
- ✅ PostgreSQL via `DATABASE_URL` (Railway add-on)
- ✅ CI/CD GitHub Actions: check + deploy backend + deploy frontend
- ✅ Backend Railway: `campo-valor-production.up.railway.app`
- ✅ Frontend Vercel: `https://sem-aperreio.vercel.app`

**Verification:**
- [x] Tasks de email prontas (`send_weekly_reminder`, `check_monthly_average`)
- [x] Healthcheck `/api/health/` responde `{"status":"ok"}`
- [x] PostgreSQL funcional em produção (`DATABASE_URL` override)
- [x] Push no `main` dispara deploy automático
- [x] Frontend acessível via HTTPS (Vercel)

**Production URLs:**
- Backend: `https://campo-valor-production.up.railway.app`
- Frontend: `https://sem-aperreio.vercel.app`

---

## Milestone Summary

| Milestone | Phases | Status |
|-----------|--------|--------|
| v1.0 | 1–4 | ✅ Shipped (2026-04-30) |
| v2.0 | 5–6 | ✅ Shipped (2026-05-05) |

---
*Last updated: 2026-05-05 after Phase 6 completion*
