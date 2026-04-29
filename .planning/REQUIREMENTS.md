# Requirements: Sem Aperreio

**Defined:** 2026-04-24
**Core Value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: Usuário pode criar conta com email, nome e senha
- [ ] **AUTH-02**: Usuário pode fazer login e receber token JWT (access + refresh)
- [ ] **AUTH-03**: Token JWT é enviado em toda requisição à API
- [ ] **AUTH-04**: Logout invalida/limpa token no frontend
- [ ] **AUTH-05**: Apenas usuário autenticado pode criar/editar/excluir seus próprios gastos

### Family Group

- [ ] **FAM-01**: Usuário pode criar um "grupo familiar" (ex: "Família Silva")
- [ ] **FAM-02**: Usuário pode convidar outro usuário para o grupo via código/link
- [ ] **FAM-03**: Membros do mesmo grupo veem todos os gastos do grupo
- [ ] **FAM-04**: Gastos são vinculados ao usuário que os criou, mas visíveis ao grupo

### Gastos (refatoração do existente)

- [ ] **GAST-01**: CRUD de gastos com autenticação (reutilizar modelo existente + user FK)
- [ ] **GAST-02**: Filtro por categoria funciona com autenticação
- [ ] **GAST-03**: Filtro por período (mês/ano) funciona com autenticação
- [ ] **GAST-04**: Paginação com metadados (count, next, previous)

### Dashboard

- [ ] **DASH-01**: Exibe total do mês atual vs. mês anterior
- [ ] **DASH-02**: Gráfico de pizza: gastos por categoria (mês atual)
- [ ] **DASH-03**: Gráfico de linha: evolução mensal (últimos 12 meses)
- [ ] **DASH-04**: Ranking das categorias mais onerosas
- [ ] **DASH-05**: Média diária e maior gasto do mês
- [ ] **DASH-06**: Dashboard filtra por mês/ano selecionado pelo usuário

### Previsão (ML)

- [ ] **ML-01**: Endpoint de previsão usa dados reais do usuário/grupo para treinar modelo
- [ ] **ML-02**: Modelo considera categoria como feature adicional
- [ ] **ML-03**: Retorna previsão de gasto total para o próximo mês

### Exportação

- [ ] **EXP-01**: Exportar gastos filtrados para CSV
- [ ] **EXP-02**: Exportar gastos filtrados para Excel (XLSX)

## v2 Requirements

### Orçamento e Metas

- **BUDG-01**: Usuário pode definir meta de gasto mensal por categoria
- **BUDG-02**: Dashboard exibe progresso da meta (barra visual)
- **BUDG-03**: Alerta visual quando gasto ultrapassa 80% da meta

### Notificações

- **NOTF-01**: Lembrete semanal para registrar gastos
- **NOTF-02**: Alerta quando gasto do mês ultrapassa média histórica

### Deploy e Infra

- **INFR-01**: PostgreSQL como banco de produção
- **INFR-02**: CI/CD com GitHub Actions
- **INFR-03**: Deploy automatizado backend + frontend

## Out of Scope

| Feature | Reason |
|---------|--------|
| Integração bancária (Open Banking) | Complexidade regulatória e técnica muito alta para MVP |
| Multi-moeda (USD, EUR) | Público-alvo brasileiro; BRL suficiente |
| PWA com cache offline | Web responsive atende; offline não é crítico para registro ocasional |
| Chat entre familiares | Fora do escopo de controle de gastos |
| Receitas / controle de renda | Foco em gastos; receitas adicionaria complexidade de planejamento |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| AUTH-04 | Phase 1 | Pending |
| AUTH-05 | Phase 1 | Pending |
| FAM-01 | Phase 2 | Pending |
| FAM-02 | Phase 2 | Pending |
| FAM-03 | Phase 2 | Pending |
| FAM-04 | Phase 2 | Pending |
| GAST-01 | Phase 2 | Pending |
| GAST-02 | Phase 2 | Pending |
| GAST-03 | Phase 2 | Pending |
| GAST-04 | Phase 2 | Pending |
| DASH-01 | Phase 3 | Pending |
| DASH-02 | Phase 3 | Pending |
| DASH-03 | Phase 3 | Pending |
| DASH-04 | Phase 3 | Pending |
| DASH-05 | Phase 3 | Pending |
| DASH-06 | Phase 3 | Pending |
| ML-01 | Phase 4 | Pending |
| ML-02 | Phase 4 | Pending |
| ML-03 | Phase 4 | Pending |
| EXP-01 | Phase 4 | Pending |
| EXP-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 22 total
- Mapped to phases: 22
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-24*
*Last updated: 2026-04-24 after initial definition*
