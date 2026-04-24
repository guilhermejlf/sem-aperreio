# Roadmap: Sem Aperreio

**Project:** Sem Aperreio — Controle de Gastos Doméstico
**Defined:** 2026-04-24
**Current Milestone:** v1 — Autenticação, Grupos Familiares e Dashboard Inteligente

---

## Milestone: v1

> Familiares se autenticam, compartilham gastos em grupo, visualizam análises e recebem previsões baseadas em dados reais.

### Phase 1 — Autenticação JWT

**Goal:** Usuários podem criar conta, fazer login e acessar a API com token JWT. Gastos passam a ser protegidos.

**Depends on:** None (código base já mapeado)

**Requirements:** AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05

**Deliverables:**
- Modelo `User` custom (ou `User` padrão Django com extensão via profile)
- Integração `djangorestframework-simplejwt`
- Endpoints: `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/refresh/`
- Middleware/permission: `IsAuthenticated` nas views de gastos
- Frontend: telas de login/cadastro, armazenamento de token, interceptador de requests

**Verification:**
- [ ] Usuário não autenticado recebe 403 ao listar gastos
- [ ] Usuário autenticado vê apenas seus próprios gastos
- [ ] Token refresh funciona silenciosamente no frontend
- [ ] Logout limpa token e redireciona para login

---

### Phase 2 — Grupo Familiar + Refatoração de Gastos

**Goal:** Múltiplos usuários compartilham gastos em um grupo. CRUD de gastos é refatorado para considerar user + family.

**Depends on:** Phase 1

**Requirements:** FAM-01, FAM-02, FAM-03, FAM-04, GAST-01, GAST-02, GAST-03, GAST-04

**Deliverables:**
- Modelo `Family` (nome, código de convite)
- Modelo `FamilyMembership` (user, family, role: admin/member)
- Refatorar `Gasto`: adicionar FK para `User` (criador) e `Family`
- Views filtram gastos pelo `family` do usuário logado
- Frontend: tela de criação/entrada em grupo, sidebar/menu de grupo

**Verification:**
- [ ] Usuário cria grupo e recebe código
- [ ] Outro usuário entra no grupo via código
- [ ] Ambos veem os mesmos gastos no dashboard
- [ ] Gastos de usuários fora do grupo não aparecem

---

### Phase 3 — Dashboard Inteligente com Filtros

**Goal:** Dashboard com filtros por mês/ano, comparativos e rankings. Gráficos refletem dados do grupo.

**Depends on:** Phase 2

**Requirements:** DASH-01, DASH-02, DASH-03, DASH-04, DASH-05, DASH-06

**Deliverables:**
- Seletor de mês/ano no dashboard
- Endpoint `/api/dashboard/?mes=6&ano=2026` com agregações
- Comparativo mês atual vs. mês anterior (valor absoluto e %)
- Ranking de categorias (top 5)
- Gráficos atualizados com dados do grupo
- Cards de estatísticas responsivos

**Verification:**
- [ ] Selecionar mês anterior atualiza todos os gráficos
- [ ] Comparativo mostra variação percentual correta
- [ ] Ranking ordena do maior para o menor gasto
- [ ] Tela vazia mostra estado amigável quando não há gastos no período

---

### Phase 4 — ML com Dados Reais + Exportação

**Goal:** Modelo de previsão treinado com dados reais do grupo. Exportação de dados para CSV/Excel.

**Depends on:** Phase 3

**Requirements:** ML-01, ML-02, ML-03, EXP-01, EXP-02

**Deliverables:**
- Script/celery task para retreinar modelo periodicamente
- Feature engineering: mês, categoria (one-hot), valor histórico médio
- Endpoint `/api/prever/` retorna previsão baseada em dados do grupo
- Exportação CSV via `StreamingHttpResponse`
- Exportação XLSX via `openpyxl`

**Verification:**
- [ ] Previsão muda quando novos gastos são adicionados
- [ ] CSV exporta colunas: data, categoria, valor, descricao, criado_por
- [ ] Excel abre corretamente no LibreOffice/Excel
- [ ] Exportação respeita filtros atuais (mês/categoria)

---

## Milestone: v2 (Future)

> Metas de orçamento, notificações e infraestrutura de produção.

### Phase 5 — Orçamento e Metas
**Requirements:** BUDG-01, BUDG-02, BUDG-03

### Phase 6 — Notificações e Deploy
**Requirements:** NOTF-01, NOTF-02, INFR-01, INFR-02, INFR-03

---

## Milestone Summary

| Milestone | Phases | Status |
|-----------|--------|--------|
| v1 | 1–4 | 🔄 Active |
| v2 | 5–6 | 📋 Planned |

---
*Last updated: 2026-04-24 after /gsd-new-project*
