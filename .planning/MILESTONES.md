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
