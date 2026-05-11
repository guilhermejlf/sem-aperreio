# Roadmap: Sem Aperreio

**Project:** Sem Aperreio — Controle de Gastos Doméstico
**Defined:** 2026-04-24
**Current Milestone:** v3.1 — Auth Polish

---

## Milestones

- **v1.0 MVP** — Phases 1-4 (shipped 2026-04-30) — See .planning/milestones/v1.0-ROADMAP.md
- **v3.0 AI** — Phases 5-7 (shipped 2026-05-07) — See .planning/milestones/v3.0-ROADMAP.md
- **v3.1 Auth Polish** — Phase 8 (in progress)

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

### v3.1 Auth Polish (In Progress)

#### Phase 8 — Melhorias de Autenticação (2 plans)

**Goal:** Polir UX de autenticação com password reset, login por email, validação de senha e confirmação de email.

**Requirements:** AUTH-04, AUTH-05, AUTH-06, AUTH-07, UI-02

**Success Criteria:**
1. Usuário pode solicitar reset de senha e receber email com link
2. Campo de login aceita username ou email indistintamente
3. Registro rejeita senhas fracas e exige confirmação
4. Email de verificação enviado no cadastro; login bloqueado até confirmação
5. Tela de login com feedback visual claro, estados de loading e mensagens de erro amigáveis

**Plans:**
- [ ] **08-01**: Backend — password reset token, email verification, login por email, validação de senha
- [ ] **08-02**: Frontend — tela de forgot password, ajustes login/registro, verificação de email

---

## Progress

| Phase             | Milestone | Plans Complete | Status      | Completed  |
| ----------------- | --------- | -------------- | ----------- | ---------- |
| 1. Foundation     | v1.0      | 2/2            | Complete    | 2026-04-30 |
| 2. Authentication | v1.0      | 2/2            | Complete    | 2026-04-30 |
| 3. Core Features  | v1.0      | 2/2            | Complete    | 2026-04-30 |
| 4. ML + Export    | v1.0      | 1/1            | Complete    | 2026-04-30 |
| 5. Budget Goals   | v3.0      | 2/2            | Complete    | 2026-05-04 |
| 6. Notifications  | v3.0      | 2/2            | Complete    | 2026-05-05 |
| 7. AI Assistant   | v3.0      | 1/1            | Complete    | 2026-05-07 |
| 8. Auth Polish    | v3.1      | 0/2            | Not started | —          |

---

*Last updated: 2026-05-11 — milestone v3.1 started*
