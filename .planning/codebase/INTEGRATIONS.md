# Integrações Externas

## APIs Internas

### Backend API (Django REST Framework)

Base URL: `http://127.0.0.1:8000/api/`

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/api/gastos/` | GET, POST | Listar (com filtros) e criar gastos |
| `/api/gastos/<id>/` | GET, PUT, DELETE | CRUD individual de gasto |
| `/api/prever/` | POST | Previsão de gasto por mês (IA) |

### Parâmetros de Query Suportados

- `?categoria=<slug>` — filtro por categoria
- `?data_inicio=YYYY-MM-DD` — data mínima
- `?data_fim=YYYY-MM-DD` — data máxima
- `?limite=<n>` — paginação manual (máx. 100)

## Comunicação Frontend ↔ Backend

- **Protocolo**: HTTP REST via `fetch()` nativo
- **Formato**: JSON
- **CORS**: Configurado para `ALLOW_ALL_ORIGINS` em DEBUG; origins explícitas em produção
- **Autenticação**: Nenhuma (`AllowAny` + sem auth classes)

## Bibliotecas de Terceiros

| Biblioteca | Uso no Código | Onde |
|-----------|--------------|------|
| scikit-learn `LinearRegression` | Modelo de previsão mensal | `treinar_modelo.py`, `api/views.py` |
| pandas `DataFrame` | Input/estruturação para o modelo ML | `treinar_modelo.py`, `api/views.py` |
| Chart.js + registerables | Gráficos de doughnut e linha | `DashboardCharts.vue` |
| PrimeVue (Button, InputNumber, InputText) | Componentes de formulário | `App.vue` |
| PrimeIcons (pi-spinner, pi-exclamation-triangle, pi-inbox, pi-plus) | Ícones da interface | `App.vue` |

## Arquivos de Configuração de Integração

- `backend/.env` — chave secreta, DEBUG, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, DB_NAME
- `frontend-ia/.env.local` — `VITE_API_URL` apontando para o backend
- `frontend-ia/src/config/api.js` — centraliza endpoints e helper `apiRequest`

## Observações

- Não há integrações com serviços de terceiros (Stripe, SendGrid, etc.)
- Não há autenticação OAuth/JWT
- Não há CI/CD, CDN ou serviços cloud configurados
