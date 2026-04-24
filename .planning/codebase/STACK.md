# Stack Tecnológico

## Backend

| Camada | Tecnologia | Versão | Finalidade |
|--------|-----------|--------|------------|
| Framework Web | Django | 4.2.7 | Servidor web e ORM |
| API REST | Django REST Framework | 3.14.0 | Serialização e endpoints |
| CORS | django-cors-headers | 4.3.1 | Cross-origin requests |
| Configuração | python-decouple | 3.8 | Variáveis de ambiente |
| Banco de Dados | SQLite | (builtin) | Persistência de dados |
| Machine Learning | scikit-learn | 1.3.2 | Modelo de previsão |
| Manipulação de Dados | pandas | 2.1.3 | DataFrames para ML |
| Servidor WSGI | (builtin) | - | runserver (dev) |

## Frontend

| Camada | Tecnologia | Versão | Finalidade |
|--------|-----------|--------|------------|
| Framework UI | Vue 3 | 3.5.32 | Interface reativa |
| Build Tool | Vite | 8.0.10 | Bundler e dev server |
| Componentes UI | PrimeVue | 4.5.5 | Inputs, buttons, etc. |
| Tema PrimeVue | @primevue/themes | 4.5.4 | Tema Aura |
| Ícones | PrimeIcons | 7.0.0 | Iconografia |
| Gráficos | Chart.js | 4.5.1 | Visualização de dados |
| Wrapper Vue Chart.js | vue-chartjs | 5.3.3 | Integração Chart.js/Vue |

## Infraestrutura / DevOps

| Componente | Detalhes |
|-----------|----------|
| Ambiente Python | venv (virtualenv) |
| Ambiente Node | npm (package-lock.json presente) |
| Banco de Dados Dev | SQLite (`db.sqlite3`) |
| Modelo IA Persistido | Pickle (`modelo.pkl`) |

## Resumo de Dependências

- **Backend**: 6 pacotes Python (Django, DRF, CORS, decouple, pandas, scikit-learn)
- **Frontend**: 6 dependências + 2 devDependencies (Vue, Vite, PrimeVue, Chart.js)
- **Total de linhas de código**: ~1.800 (backend) + ~1.900 (frontend)
