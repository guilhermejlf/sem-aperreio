# Estrutura do Projeto

## Diretórios e Arquivos

```
projeto-ia/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           ← Modelo Gasto
│   │   ├── serializers.py      ← GastoSerializer
│   │   ├── views.py            ← CRUD + previsão IA
│   │   ├── urls.py             ← Rotas da app
│   │   ├── modelo.pkl          ← Modelo ML persistido (pickle)
│   │   └── migrations/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── settings.py         ← Config Django
│   │   ├── urls.py             ← Roteamento root (/admin, /api)
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── manage.py
│   ├── requirements.txt        ← 6 dependências Python
│   ├── db.sqlite3              ← Banco SQLite
│   ├── .env                    ← Variáveis de ambiente (gitignored)
│   └── .env.example            ← Template de env
│
├── frontend-ia/
│   ├── src/
│   │   ├── main.js             ← Bootstrap Vue + PrimeVue (Aura)
│   │   ├── App.vue             ← Root: tabs + lista + formulário
│   │   ├── style.css           ← CSS global (light/dark scheme)
│   │   ├── config/
│   │   │   └── api.js          ← API_BASE_URL + endpoints + helper fetch
│   │   ├── components/
│   │   │   ├── DashboardCharts.vue   ← Gráficos e estatísticas
│   │   │   └── HelloWorld.vue        ← Componente boilerplate (não usado)
│   │   └── assets/
│   │       └── logo.png        ← Logo do app
│   ├── index.html
│   ├── vite.config.js          ← Config mínima Vite + plugin Vue
│   ├── package.json            ← 6 deps + 2 devDeps
│   └── public/
│       ├── favicon.svg
│       └── icons.svg
│
├── treinar_modelo.py           ← Script: treina LinearRegression com dados fixos
├── testar_modelo.py            ← Script: carrega e testa modelo.pkl
├── README.md                   ← Documentação em português
├── venv/                       ← Ambiente virtual Python
└── .gitignore
```

## Tamanho por Diretório

| Diretório | Arquivos Relevantes | Estimativa Linhas |
|-----------|-------------------|------------------|
| `backend/api/` | models, serializers, views, urls | ~350 |
| `backend/backend/` | settings, urls | ~200 |
| `frontend-ia/src/` | App.vue, DashboardCharts.vue, api.js, main.js, style.css | ~1.900 |
| `treinar_modelo.py` + `testar_modelo.py` | Scripts auxiliares | ~40 |
| **Total codebase** | | **~2.500** |

## Arquivos Não Rastreados pelo Git

- `backend/db.sqlite3`
- `backend/.env`
- `backend/api/modelo.pkl`
- `frontend-ia/node_modules/`
- `venv/`
- `frontend-ia/.env.local`

## Pontos de Entrada

| Tipo | Arquivo | Comando |
|------|---------|---------|
| Backend | `backend/manage.py` | `python manage.py runserver` |
| Frontend | `frontend-ia/index.html` | `npm run dev` |
| ML (treino) | `treinar_modelo.py` | `python treinar_modelo.py` |

## Modelo de Dados

```python
Gasto
├── id (PK, auto)
├── valor (Decimal, 10,2)
├── categoria (Char, choices: 7 categorias)
├── descricao (Char, 200, opcional)
├── data (Date)
├── criado_em (DateTime, auto_now_add)
└── atualizado_em (DateTime, auto_now)
```
