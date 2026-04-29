# Phase 4: ML com Dados Reais + Exportação — Plan

## Wave 1: ML Pipeline com Dados Reais

### Task 1.1: Atualizar requirements.txt
**Files modified:** `requirements.txt`
**Action:** Adicionar `openpyxl>=3.1.0` ao requirements.txt.

### Task 1.2: Criar módulo de ML (`api/ml.py`)
**Files modified:** `api/ml.py` (new)
**Action:**
- Criar função `treinar_modelo(gastos_queryset)` que recebe queryset de gastos
- Feature engineering: extrair mês da data, one-hot encode categoria, calcular valor médio histórico por categoria
- Usar scikit-learn LinearRegression
- Retornar modelo treinado + métricas (R² score)
- Retornar None com mensagem se < 6 registros de dados
- Função `prever(modelo, mes, categoria=None)` que retorna previsão

### Task 1.3: Atualizar endpoint `/api/prever/`
**Files modified:** `api/views.py`
**Action:**
- Substituir lógica hardcoded por chamada ao módulo ML
- Buscar gastos do grupo/family do usuário logado (mesmo padrão da view `gastos`)
- Aceitar parâmetro opcional `categoria` no POST
- Treinar modelo on-demand
- Retornar: `{"mes", "previsao", "moeda", "categoria" (se fornecida), "dados_usados", "r2_score"}`
- Se < 6 dados, retornar 400 com mensagem amigável

## Wave 2: Exportação de Dados

### Task 2.1: Endpoint CSV
**Files modified:** `api/views.py`, `api/urls.py`
**Action:**
- Criar `@api_view(['GET'])` `exportar_csv(request)`
- Reutilizar mesmos filtros da view `gastos` (categoria, data_inicio, data_fim)
- Usar `StreamingHttpResponse` com `content_type='text/csv'`
- Header `Content-Disposition: attachment; filename="gastos.csv"`
- Colunas: `data`, `categoria`, `valor`, `descricao`, `criado_por`

### Task 2.2: Endpoint Excel (XLSX)
**Files modified:** `api/views.py`, `api/urls.py`
**Action:**
- Criar `@api_view(['GET'])` `exportar_xlsx(request)`
- Mesmos filtros do CSV
- Usar openpyxl para gerar workbook em memória
- Retornar `HttpResponse` com `content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'`
- Header `Content-Disposition: attachment; filename="gastos.xlsx"`
- Colunas: `data`, `categoria`, `valor`, `descricao`, `criado_por`

### Task 2.3: Registrar rotas
**Files modified:** `api/urls.py`
**Action:**
- Adicionar `path("export/csv/", exportar_csv, name="export_csv")`
- Adicionar `path("export/xlsx/", exportar_xlsx, name="export_xlsx")`

## Wave 3: Frontend

### Task 3.1: Botões de exportação na aba Gastos
**Files modified:** `frontend-ia/src/App.vue`, `frontend-ia/src/config/api.js`
**Action:**
- Adicionar funções `exportarCSV()` e `exportarXLSX()` em `api.js`
- Adicionar botões "Exportar CSV" e "Exportar Excel" no `gastos-toolbar` do `App.vue`
- Usar `window.URL.createObjectURL` para trigger download
- Ícones: `pi pi-file-export` e `pi pi-file-excel`

### Task 3.2: Feedback de download
**Files modified:** `frontend-ia/src/App.vue`
**Action:**
- Toast de sucesso após download iniciar
- Toast de erro se falhar

## Verification

- [ ] POST /api/prever/ com dados reais retorna previsão > 0
- [ ] Previsão muda quando novos gastos são adicionados
- [ ] GET /api/export/csv/ baixa arquivo com colunas corretas
- [ ] GET /api/export/xlsx/ baixa arquivo abrível no Excel/LibreOffice
- [ ] Exportação respeita filtros de data/categoria
- [ ] Frontend mostra botões e download funciona
