# Phase 4: ML com Dados Reais + Exportação — Context

**Gathered:** 2026-04-29
**Status:** Ready for planning
**Source:** Discuss-phase + requirements

## Phase Boundary

Esta phase substitui o modelo ML hardcoded por um modelo treinado com dados reais do grupo familiar do usuário logado. Também adiciona exportação de gastos para CSV e Excel.

## Implementation Decisions

### ML Pipeline
- **Retreinamento**: On-demand via endpoint (não background/Celery para MVP)
- **Features**: mês (1-12), categoria (one-hot encoded), valor médio histórico por categoria
- **Algoritmo**: scikit-learn LinearRegression (já no requirements.txt)
- **Persistência**: pickle do modelo por grupo familiar (não global)
- **Fallback**: se < 6 meses de dados, retornar mensagem explicativa

### Exportação
- **CSV**: Python csv module + StreamingHttpResponse
- **Excel**: openpyxl (adicionar ao requirements.txt)
- **Filtros**: respeitar mesmos filtros da view de gastos (data_inicio, data_fim, categoria)
- **Colunas**: data, categoria, valor, descricao, criado_por (username)

### Endpoint de Previsão
- POST /api/prever/ → treina modelo com dados do grupo + retorna previsão
- Considerar mês solicitado e categoria (se fornecida)
- Retornar também confiança/metricas básicas (R² ou similar)

## Canonical References

- `api/views.py` — endpoint prever_gasto atual (hardcoded)
- `api/models.py` — Gasto model com FK Family
- `api/urls.py` — roteamento
- `requirements.txt` — dependências

## Deferred Ideas

- Celery/background job para retreinamento automático
- Múltiplos algoritmos (RandomForest, XGBoost)
- Previsão por categoria individual (além do total)
