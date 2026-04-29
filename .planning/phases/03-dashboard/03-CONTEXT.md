# Phase 3: Dashboard Inteligente com Filtros - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Dashboard com filtros por mês/ano, comparativos e rankings. Gráficos refletem dados do grupo. Endpoint `/api/dashboard/?mes=6&ano=2026` com agregações prontas. Seletor de período atualiza cards e ranking; gráfico de evolução mantém visão histórica de 12 meses.

</domain>

<decisions>
## Implementation Decisions

### Filtro de período e evolução mensal
- **D-01:** Seletor de mês/ano no topo do dashboard filtra cards estatísticos, ranking de categorias e gráfico de pizza (categorias)
- **D-02:** Gráfico de linha "Evolução Mensal" sempre mostra últimos 12 meses completos, independente do filtro selecionado — serve como contexto histórico
- **D-03:** Padrão: mês e ano atual quando o usuário abre o dashboard

### Comparativo mês atual vs. anterior
- **D-04:** Card separado (não subtítulo) com seta ↑/↓ e percentual colorido
- **D-05:** Verde quando gasto diminuiu (bom), vermelho quando aumentou — perspectiva de economia
- **D-06:** Valor absoluto da diferença também exibido junto com a %

### Agregações: backend vs. frontend
- **D-07:** Novo endpoint `GET /api/dashboard/?mes={mes}&ano={ano}` no backend retorna todas as agregações prontas
- **D-08:** Frontend consome o endpoint e passa os dados para os componentes — sem cálculo local de agregações
- **D-09:** Endpoint retorna: total_mes, total_mes_anterior, variacao_absoluta, variacao_percentual, media_diaria, maior_gasto, ranking_categorias[], evolucao_12meses[]

### Gráfico de categorias (pizza/doughnut)
- **D-10:** Apenas categorias com gastos no período filtrado — sem fatias vazias
- **D-11:** Cores consistentes por categoria (mesma paleta já usada)
- **D-12:** Se nenhum gasto no período, mostrar estado vazio amigável em vez de gráfico vazio

### Claude's Discretion
- Design exato do seletor de mês/ano (dropdown, slider, ou input date)
- Ordenação do ranking (asc/desc toggle)
- Animações de transição entre períodos
- Precisão de casas decimais nos valores

</decisions>

<specifics>
## Specific Ideas

- Card de comparativo com seta ↑/↓ — "parecido com app de finanças"
- Ranking mostra número 1, 2, 3... com badge circular verde
- Estado vazio: ilustração + "Nenhum gasto neste período" + CTA para adicionar gasto

</specifics>

<canonical_refs>
## Canonical References

No external specs — requirements fully captured in decisions above and ROADMAP.md Phase 3 description.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `DashboardCharts.vue`: Cards de estatísticas, gráfico de pizza (doughnut), gráfico de linha, ranking de categorias — será refatorado para consumir dados do novo endpoint
- `api.js`: Função `apiRequest()` pronta para consumir novo endpoint
- Chart.js já registrado e configurado com tema escuro

### Established Patterns
- Vue 3 Options API
- Props down (gastos array → DashboardCharts)
- Computed properties para cálculos — serão substituídas por data + watch no endpoint
- Dark theme com cores hardcoded (#22c55e, #3b82f6, etc.)

### Integration Points
- Backend: Novo view `dashboard()` em `views.py` ou novo arquivo `views_dashboard.py`
- URL: Adicionar `path('dashboard/', views.dashboard)` em `urls.py`
- Frontend: `App.vue` passa mês/ano selecionado para `DashboardCharts.vue` como prop; componente chama endpoint

</code_context>

<deferred>
## Deferred Ideas

- Filtro por categoria no dashboard — pode ser adicionado futuramente
- Gráfico de barras comparativo entre membros do grupo — fase futura de análises avançadas
- Exportação dos dados do dashboard — Phase 4 (ML + Exportação)

</deferred>

---

*Phase: 03-dashboard*
*Context gathered: 2026-04-28*
