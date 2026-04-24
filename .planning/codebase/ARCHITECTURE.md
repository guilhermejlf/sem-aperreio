# Arquitetura do Sistema

## Visão Geral

Sistema monolito dividido em duas camadas principais:

```
┌─────────────────────────────┐
│     Frontend (Vue 3)        │  ← SPA rodando em Vite dev server
│  localhost:5173             │
├─────────────────────────────┤
│     HTTP/JSON (CORS)        │
├─────────────────────────────┤
│     Backend (Django + DRF)    │  ← API REST rodando em runserver
│  localhost:8000 /api/       │
├─────────────────────────────┤
│     SQLite + Pickle         │  ← Persistência de dados + modelo ML
└─────────────────────────────┘
```

## Camada Backend

### App Django: `api`

Responsabilidade única: domínio de **Gastos** + **Previsão IA**.

| Componente | Arquivo | Responsabilidade |
|-----------|---------|-----------------|
| Modelo | `api/models.py` | `Gasto` (valor, categoria, descrição, data) |
| Serializer | `api/serializers.py` | Validação + formatação de datas (ISO) |
| Views | `api/views.py` | CRUD gastos + endpoint `/prever` com lazy-load do modelo |
| URLs | `api/urls.py` | Rotas `/gastos/`, `/gastos/<pk>/`, `/prever/` |
| Admin | `api/admin.py` | (não verificado) |

### Decisões Arquiteturais

- **CBV vs FBV**: Usa Function-Based Views com `@api_view` (não generics/viewsets)
- **Lazy Loading do Modelo**: `_modelo_ia` carregado via `get_modelo_ia()` sob demanda; tratamento de erro em caso de arquivo ausente
- **Sem camada de serviço**: Lógica de negócio diretamente nas views
- **Sem autenticação**: `DEFAULT_AUTHENTICATION_CLASSES = []` + `AllowAny`
- **CORS condicional**: `CORS_ALLOW_ALL_ORIGINS = True` apenas em DEBUG

### Modelo de Machine Learning

- **Algoritmo**: `LinearRegression` (scikit-learn)
- **Features**: apenas `mes` (1–12)
- **Target**: `gasto` (valor estimado)
- **Dados de treino**: hardcoded no script `treinar_modelo.py`
- **Persistência**: `pickle.dump()` → `backend/api/modelo.pkl`
- **Limite de previsão**: clamp entre 0 e 100.000 BRL

## Camada Frontend

### Estrutura de Componentes

```
App.vue (root)
├── DashboardCharts.vue  ← stats cards + doughnut chart + line chart + top categorias
```

### Gerenciamento de Estado

- **Estado**: Todo em `App.vue` via `data()` (não Pinia/Vuex)
- **Comunicação**: Props down (`:gastos`) para `DashboardCharts.vue`
- **Tabs**: `activeTab` controla qual seção renderiza ('dashboard' | 'gastos' | 'adicionar')

### Separação de Responsabilidades

| Responsabilidade | Onde |
|-----------------|------|
| Fetching de API | `apiRequest()` em `config/api.js` |
| Transformação de dados | Computed properties em `App.vue` e `DashboardCharts.vue` |
| Renderização de gráficos | `DashboardCharts.vue` (Chart.js diretamente) |
| Formatação de datas/valores | Métodos helpers nos componentes |

## Fluxo de Dados Típico

1. Usuário acessa frontend (`localhost:5173`)
2. `App.vue` monta → chama `carregarGastos()`
3. `apiRequest()` faz GET para `localhost:8000/api/gastos/`
4. Backend: `Gasto.objects.all()` → `GastoSerializer` → JSON
5. Frontend: popula `this.gastos` → computeds reagem → charts atualizam
6. Adição de gasto: POST → backend valida → salva no SQLite → retorna objeto
7. Previsão: POST `/api/prever/` com `{mes: N}` → modelo pickle prediz valor

## Decisões Arquiteturais Não Padronizadas

- **Gráficos com Chart.js diretamente**: Não usa `vue-chartjs` no componente (`vue-chartjs` está no package.json mas não é importado)
- **Estilização inline**: CSS scoped em cada `.vue`; não usa Tailwind/Bootstrap/PrimeFlex
- **Sem router**: Tabs controladas por estado local (`activeTab`)
- **Sem store global**: Estado distribuído em `App.vue`
