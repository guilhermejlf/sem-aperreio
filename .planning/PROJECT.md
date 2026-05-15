# Sem Aperreio — Controle de Gastos Doméstico

## What This Is

Sistema web para controle de gastos domésticos onde integrantes de uma família se autenticam, registram seus gastos por categoria e visualizam dashboards com análises que ajudam a identificar onde estão gastando mais e como economizar.

## Core Value

Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

## Requirements

### Validated (v1.0 — shipped 2026-04-30)

- ✓ Cadastro de gastos com categorias — Phase 0
- ✓ Dashboard com gráficos (pizza + linha) e estatísticas — Phase 0
- ✓ Previsão de gastos por mês via ML — Phase 0
- ✓ Interface responsiva com tema escuro — Phase 0
- ✓ **AUTH-01**: Usuários podem criar conta e fazer login (JWT) — v1.0
- ✓ **AUTH-02**: Gastos ficam vinculados ao usuário logado — v1.0
- ✓ **AUTH-03**: Usuários podem pertencer a um "grupo familiar" (compartilhar gastos) — v1.0
- ✓ **DASH-01**: Dashboard exibe gastos filtrados por período (mês/ano) — v1.0
- ✓ **DASH-02**: Ranking de categorias por valor total — v1.0
- ✓ **DASH-03**: Comparativo mês atual vs. mês anterior — v1.0
- ✓ **ML-01**: Modelo de previsão treinado com dados reais do usuário/família — v1.0
- ✓ **ML-02**: Previsão considera categoria (não apenas mês) — v1.0
- ✓ **EXP-01**: Exportar gastos para CSV/Excel — v1.0

### Validated (v1.1 — shipped 2026-05-08)

- ✓ **RECEITAS-01**: CRUD de receitas (entradas financeiras) com data de competência
- ✓ **EXTRATO-01**: Visualização detalhada de gastos e receitas por período
- ✓ **BUDG-01**: Definir meta de gasto mensal por categoria ou geral — v1.1
- ✓ **BUDG-02**: Dashboard e tela de metas exibem progresso com barra visual — v1.1
- ✓ **BUDG-03**: Alerta visual e por API quando gasto ultrapassa 80% da meta (status: danger/critical) — v1.1
- ✓ **AI-01**: Assistente de IA integrado para dúvidas e análise de gastos — v1.1
- ✓ **NOTF-01**: Lembretes semanais por email com resumo dos gastos — v1.1
- ✓ **NOTF-02**: Alerta por email quando gasto do mês ultrapassa média histórica +20% — v1.1
- ✓ **INFR-01**: PostgreSQL como banco de produção — v1.1
- ✓ **INFR-02**: CI/CD com GitHub Actions (deploy automático) — v1.1
- ✓ **INFR-03**: Deploy automatizado backend (Railway) + frontend (Vercel) — v1.1
- ✓ **EXP-02**: Exportação para PDF — v1.1
- ✓ **UI-01**: Header glassmorphism sticky com logo, navegação centrada e menu de usuário

### Validated (v3.2 — shipped 2026-05-15)

- ✓ **DASH-04**: Hierarquia visual com 3 níveis de protagonismo (saldo/insights vs comportamento vs terciários)
- ✓ **DASH-05**: Motion System oficial integrado (tokens, easing, stagger, shimmer, reduced-motion)
- ✓ **DASH-06**: Insights contextuais inteligentes com glow semântico por tipo
- ✓ **DASH-07**: Gráfico de linha com gradient fill orgânico (Canvas linearGradient)
- ✓ **UI-03**: Mobile-first refinado: saldo com clamp(), cards sem quebra, previsão centralizado
- ✓ **UI-04**: Loading system premium com skeletons estruturais e fallbacks async
- ✓ **UI-05**: Micro refinamentos de alinhamento óptico, saturação e profundidade visual

### Active (v2.0)

- [ ] **TEST-01**: Testes automatizados (unitários + integração)
- [ ] **CACHE-01**: Cache Redis para dashboard e previsões
- [ ] **MOB-01**: PWA com cache offline
- [ ] **BANK-01**: Integração bancária (Open Banking) — avaliar viabilidade regulatória

### Out of Scope

| Feature | Reason |
|---------|--------|
| Integração bancária (Open Banking) | Complexidade regulatória e técnica muito alta para MVP |
| Multi-moeda (USD, EUR) | Público-alvo brasileiro; BRL suficiente |
| PWA com cache offline | Web responsive atende; offline não é crítico para registro ocasional |
| Chat entre familiares | Fora do escopo de controle de gastos |

## Context

Sistema completo de controle de gastos domésticos com autenticação JWT, grupos familiares, dashboard com filtros por período (mês/ano), ranking de categorias, comparativo mês a mês, previsão via ML com dados reais, exportação CSV/Excel/PDF, receitas, metas de orçamento com alertas visuais, assistente de IA, notificações por email e interface moderna em tema escuro com glassmorphism. Backend Django + DRF + PostgreSQL, frontend Vue 3 + Vite, deploy automatizado via Railway + Vercel.

### Tech Stack (v1.1 — Produção)

- **Backend**: Django 4.2 + Django REST Framework + djangorestframework-simplejwt
- **Frontend**: Vue 3 (Options API) + Vite + Chart.js + PrimeVue + PrimeIcons
- **ML**: scikit-learn (LinearRegression por categoria)
- **Banco**: PostgreSQL (produção), SQLite (dev)
- **Cache/Tarefas**: Redis + Celery
- **Export**: openpyxl (XLSX), csv/StreamingHttpResponse (CSV), reportlab (PDF)
- **Email**: SendGrid
- **IA**: OpenAI API
- **Deploy**: Railway (backend) + Vercel (frontend)
- **CI/CD**: GitHub Actions

### Known Issues / Tech Debt

- Options API no Vue — Composition API seria mais moderna, mas código legado funcional
- Modelo ML treinado on-demand — não persistido; recomenda-se cache Redis ou Celery para datasets grandes
- Falta paginação completa com metadados (count/next/previous) — implementado apenas limite simples (50 itens)
- Sem testes automatizados — apenas testes manuais realizados
- Cron jobs externos (cron-job.org) — idealmente migrar para Celery Beat interno

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

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
| Manter Options API no Vue | Código já usa Options API; migrar para Composition seria retrabalho sem ganho imediato | — Pending (candidato v2) |
| SQLite para MVP / PostgreSQL produção | Zero config local; DATABASE_URL em produção trivial com Django | ✓ Good |
| Lazy-load do modelo ML | pickle carregado sob demanda; evita startup lento se arquivo ausente | ✓ Good |
| JWT ao invés de session cookies | Frontend SPA separado do backend; JWT facilita CORS e mobile futuro | ✓ Good |
| Grupo familiar (User → Family) | Um gasto pertence a um User que pertence a uma Family; permite múltiplos usuários verem os mesmos gastos | ✓ Good |
| Endpoint + cron-job.org para tasks | Celery worker não roda no Railway free tier; endpoint com secret é suficiente | ✓ Good |
| Fallback parser IA (regex) | OpenAI pode estar indisponível ou sem créditos; regex cobre 80% dos casos | ✓ Good |
| Drawer lateral para chat IA | Modal bloqueia interação; drawer permite acesso ao dashboard enquanto conversa | ✓ Good |

## Current Milestone: v3.1 — Auth Polish

**Goal:** Melhorar UX de autenticação com password reset, login por email, validação de senha e confirmação de email.

**Target features:**
- Password reset via email (esqueci minha senha)
- Login com username OU email
- Validação de senha forte + confirmação de senha no registro
- Confirmação de email no cadastro
- Melhorias visuais na tela de login/registro

**Active backlog (future milestones):**
- [ ] **TEST-01**: Testes automatizados (unitários + integração)
- [ ] **CACHE-01**: Cache Redis para dashboard e previsões
- [ ] **MOB-01**: PWA com cache offline
- [ ] **BANK-01**: Integração bancária (Open Banking) — avaliar viabilidade regulatória
- [ ] **CRON-01**: Migrar cron jobs externos para Celery Beat interno

**Key context:**
- Sistema em produção estável (Railway + Vercel + PostgreSQL + SendGrid)
- Sem testes automatizados — risco técnico para evolução
- Modelo ML treinado on-demand — oportunidade de cache
- Options API no Vue pode ser mantido ou migrado gradualmente
- Deploy automatizado funcional — focar em qualidade e novas features

---
*Last updated: 2026-05-11 — milestone v3.1 Auth Polish started*
