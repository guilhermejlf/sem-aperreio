# Roadmap: Sem Aperreio

**Project:** Sem Aperreio — Controle de Gastos Doméstico
**Defined:** 2026-04-24
**Current Milestone:** Next

---

## Milestones

- **v1.0 MVP** — Phases 1-4 (shipped 2026-04-30) — See .planning/milestones/v1.0-ROADMAP.md
- **v3.0 AI** — Phases 5-7 (shipped 2026-05-07) — See .planning/milestones/v3.0-ROADMAP.md

---

## Phases

<details>
<summary>v1.0 MVP (Phases 1-4) — SHIPPED 2026-04-30</summary>

### Phase 1 — Autenticação JWT (2 plans)
- [x] Backend JWT: djangorestframework-simplejwt, endpoints auth
- [x] Frontend auth: telas login/cadastro, token storage, interceptador, logout

### Phase 2 — Grupo Familiar + Refatoração de Gastos (2 plans)
- [x] Backend: Family/FamilyMembership models, FamilyViewSet, gastos filtrados por family
- [x] Frontend: FamilyView.vue, drawer, badge no header, gerenciamento de membros

### Phase 3 — Dashboard Inteligente com Filtros (2 plans)
- [x] Backend: endpoint /api/dashboard/ com agregações, ranking, comparativo
- [x] Frontend: seletor mês/ano, cards responsivos, gráficos Chart.js, estado vazio

### Phase 4 — ML com Dados Reais + Exportação (1 plan)
- [x] ML: previsão por categoria via LinearRegression, fallback média
- [x] Export: CSV (StreamingHttpResponse), XLSX (openpyxl)

See archive: .planning/milestones/v1.0-ROADMAP.md
</details>

<details>
<summary>v3.0 AI (Phases 5-7) — SHIPPED 2026-05-07</summary>

### Phase 5 — Orçamento e Metas (2 plans)
- [x] Modelo MetaGasto, endpoints CRUD, dashboard integration
- [x] Frontend BudgetView, BudgetEditModal, alertas 80%/100%

### Phase 6 — Notificações e Deploy (2 plans)
- [x] Backend: tasks Celery/SendGrid, endpoint trigger, cron-job.org
- [x] Infra: PostgreSQL, GitHub Actions CI/CD, Railway + Vercel

### Phase 7 — Assistente Financeiro Conversacional (1 plan)
- [x] IA-01: parser OpenAI + fallback, drawer chat, FAB, confirmação
- [x] IA-02: contextual multi-etapas
- [x] IA-03: continuidade conversacional, saudações, despedida

See archive: .planning/milestones/v3.0-ROADMAP.md
</details>

---

## Next Milestone

TBD — run /gsd-new-milestone to define next phase.

---

*Last updated: 2026-05-11 after v3.0 milestone completion*
