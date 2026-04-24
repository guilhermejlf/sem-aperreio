# Sem Aperreio — Controle de Gastos Doméstico

## What This Is

Sistema web para controle de gastos domésticos onde integrantes de uma família se autenticam, registram seus gastos por categoria e visualizam dashboards com análises que ajudam a identificar onde estão gastando mais e como economizar.

## Core Value

Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

## Requirements

### Validated

- ✓ Cadastro de gastos com categorias — Phase 0 (código base existente)
- ✓ Dashboard com gráficos (pizza + linha) e estatísticas — Phase 0 (código base existente)
- ✓ Previsão de gastos por mês via ML — Phase 0 (código base existente, modelo fixo)
- ✓ Interface responsiva com tema escuro — Phase 0 (código base existente)

### Active

- [ ] **AUTH-01**: Usuários podem criar conta e fazer login (JWT)
- [ ] **AUTH-02**: Gastos ficam vinculados ao usuário logado
- [ ] **AUTH-03**: Usuários podem pertencer a um "grupo familiar" (compartilhar gastos)
- [ ] **DASH-01**: Dashboard exibe gastos filtrados por período (mês/ano)
- [ ] **DASH-02**: Ranking de categorias por valor total
- [ ] **DASH-03**: Comparativo mês atual vs. mês anterior
- [ ] **ML-01**: Modelo de previsão treinado com dados reais do usuário/família
- [ ] **ML-02**: Previsão considera categoria (não apenas mês)
- [ ] **EXP-01**: Exportar gastos para CSV/Excel

### Out of Scope

- Pagamentos / integração bancária — muito complexo para MVP, entrada manual suficiente
- Orçamentos / metas de gasto — pode ser adicionado futuramente
- Notificações push/email — não essencial para análise de gastos
- PWA offline-first — web responsive já atende o uso case
- Multi-moeda — foco em BRL (Brasil)

## Context

Código base existente em Python/Django (backend) e Vue 3 + Vite (frontend). O sistema já possui CRUD de gastos, dashboard com Chart.js e previsão via regressão linear. O maior gap é a ausência de autenticação — todos os gastos são públicos. O modelo ML usa dados hardcoded e não aprende com os gastos reais cadastrados.

## Constraints

- **Tech Stack**: Manter Django + DRF + Vue 3 + Vite (código já existe)
- **Banco de Dados**: SQLite para MVP (fácil de rodar localmente), PostgreSQL para produção futura
- **ML Framework**: scikit-learn (já instalado, evitar adicionar peso)
- **Idioma**: Português brasileiro na interface e mensagens
- **Autenticação**: JWT via Django REST Framework SimpleJWT (padrão da comunidade)
- **Deploy**: Backend no Render/Railway, frontend no Netlify/Vercel (futuro)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Manter Options API no Vue | Código já usa Options API; migrar para Composition seria retrabalho sem ganho imediato | — Pending |
| SQLite para MVP | Zero configuração para desenvolvimento local; migração para PostgreSQL é trivial com Django | — Pending |
| Lazy-load do modelo ML | pickle carregado sob demanda; evita startup lento se arquivo ausente | ✓ Good |
| JWT ao invés de session cookies | Frontend SPA separado do backend; JWT facilita CORS e mobile futuro | — Pending |
| Grupo familiar (User → Family) | Um gasto pertence a um User que pertence a uma Family; permite múltiplos usuários verem os mesmos gastos | — Pending |

---
*Last updated: 2026-04-24 after /gsd-new-project brownfield initialization*
