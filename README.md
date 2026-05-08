# Sem Aperreio — Controle de Gastos Doméstico

Sistema web completo para controle de gastos domésticos em família, com previsão via IA, metas de orçamento, notificações por email e interface moderna em tema escuro.

## 🚀 Stack Tecnológico

### Backend
- **Django 4.2** — Framework web
- **Django REST Framework** — API REST
- **SimpleJWT** — Autenticação JWT
- **PostgreSQL** — Banco de dados (produção)
- **Redis + Celery** — Tarefas assíncronas e notificações
- **Scikit-learn / Pandas / NumPy** — Machine Learning
- **OpenAI** — Assistente de IA
- **SendGrid** — Envio de emails
- **Gunicorn** — Servidor WSGI

### Frontend
- **Vue 3 (Options API)** — Framework JavaScript
- **Vite** — Build tool
- **PrimeVue / PrimeIcons** — Componentes UI e ícones
- **Chart.js** — Gráficos e dashboards
- **CSS3** — Estilização com glassmorphism

## ✅ Funcionalidades Entregues

| Módulo | Funcionalidades |
|--------|----------------|
| **Autenticação** | Cadastro, login JWT, refresh token, perfil do usuário |
| **Gastos** | CRUD completo com 10 categorias, data de competência, pagamento e status |
| **Receitas** | CRUD de entradas financeiras com data de competência |
| **Grupo Familiar** | Criar grupo, convidar por código, compartilhar gastos, roles (admin/member) |
| **Dashboard** | Cards de totais, gráfico de pizza (categorias), gráfico de linha (evolução), ranking, comparativo mês a mês |
| **Extrato** | Visualização detalhada filtrada por período |
| **Metas** | Definir meta de gasto mensal por categoria (ou geral), com alerta visual de 80% |
| **ML / Previsão** | Modelo treinado com dados reais do usuário/família, prevê gasto do mês por categoria |
| **Exportação** | CSV, Excel (XLSX) e PDF |
| **Assistente IA** | Chat integrado para ajudar com dúvidas e análise de gastos |
| **Notificações** | Lembretes semanais por email + alerta quando gasto ultrapassa média histórica |
| **UI** | Tema escuro, glassmorphism, responsivo, header sticky com navegação centrada |

## 📱 Categorias de Gasto

- Moradia 🏠
- Mercado 🛒
- Restaurantes / Delivery 🍔
- Transporte 🚗
- Saúde 🏥
- Educação 📚
- Lazer 🎮
- Contas e serviços 💡
- Compras 🛍️
- Outros 📦

## 🔧 Instalação Local

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- PostgreSQL (opcional, SQLite funciona para dev)
- Redis (opcional, para tarefas assíncronas)

### Backend

```bash
# 1. Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Dependências
pip install -r requirements.txt

# 3. Variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações (DATABASE_URL, SECRET_KEY, etc.)

# 4. Banco de dados
python manage.py migrate

# 5. Criar superusuário (opcional)
python manage.py createsuperuser

# 6. Iniciar
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install

# Configurar API local
echo "VITE_API_URL=http://127.0.0.1:8000" > .env.local

npm run dev
```

## 🌐 URLs

### Desenvolvimento
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin Django: http://localhost:8000/admin/

### Produção
- **Frontend**: https://sem-aperreio.vercel.app
- **Backend**: https://campo-valor-production.up.railway.app
- **Healthcheck**: `GET /api/health/`

## 📚 Endpoints da API

### Autenticação
- `POST /api/auth/register/` — Criar conta
- `POST /api/auth/login/` — Login (retorna access + refresh)
- `POST /api/auth/refresh/` — Renovar token
- `GET /api/auth/user/` — Dados do usuário logado

### Gastos
- `GET /api/gastos/` — Listar (filtros: categoria, data_inicio, data_fim, limite)
- `POST /api/gastos/` — Criar
- `GET/PUT/DELETE /api/gastos/{id}/`

### Receitas
- `GET /api/receitas/` — Listar
- `POST /api/receitas/` — Criar
- `GET/PUT/DELETE /api/receitas/{id}/`

### Dashboard & Análises
- `GET /api/dashboard/?mes=5&ano=2026` — Cards e totais do período
- `GET /api/extrato/?mes=5&ano=2026` — Extrato detalhado
- `POST /api/prever/` — Previsão de gastos via ML

### Metas
- `GET /api/metas/` — Listar metas
- `POST /api/metas/criar/` — Criar meta
- `PUT /api/metas/{id}/` — Atualizar
- `DELETE /api/metas/{id}/deletar/` — Remover

### Grupo Familiar
- `GET/POST /api/family/` — Criar/consultar grupo
- `POST /api/family/join/` — Entrar por código
- `POST /api/family/leave/` — Sair do grupo

### Exportação
- `GET /api/export/csv/` — Exportar CSV
- `GET /api/export/xlsx/` — Exportar Excel
- `GET /api/export/pdf/` — Exportar PDF

### Notificações & IA
- `GET /api/health/` — Healthcheck
- `GET /api/notificacoes/status/` — Status das notificações
- `POST /api/tasks/trigger/` — Disparar tarefas manualmente
- `POST /api/ai/chat/` — Chat com assistente IA

## 🔒 Segurança

- Autenticação JWT com refresh token
- CORS configurado dinamicamente por ambiente
- Validação de inputs no backend e frontend
- SQL injection prevention via ORM
- Proteção XSS com escape automático
- Variáveis sensíveis em `.env`

## 🚀 Deploy & CI/CD

Deploy automatizado via **GitHub Actions**:
- Push na branch `main` dispara deploy
- **Backend** → Railway (Django + PostgreSQL + Redis)
- **Frontend** → Vercel (SPA com Vite)
- Cron jobs configurados via cron-job.org (Weekly Reminder + Average Alert)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit (`git commit -m 'feat: descrição'`)
4. Push (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

MIT
