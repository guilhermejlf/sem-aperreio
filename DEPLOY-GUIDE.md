# Guia de Deploy — Sem Aperreio

**URLs de Produção:**
- Backend: https://campo-valor.up.railway.app
- Frontend: https://sem-aperreio.vercel.app

**Fase:** Configuração das plataformas Railway + Vercel + SendGrid

---

## 1. SendGrid (Email)

1. Acesse [sendgrid.com](https://sendgrid.com) e crie conta gratuita
2. Verifique seu email e domínio (ou use domínio genérico por enquanto)
3. Vá em **Settings → API Keys → Create API Key**
4. Nome: `Sem Aperreio Production`
5. Permissão: **Full Access** (ou restrita para Mail Send)
6. **Copie a API key** (só aparece uma vez!)

---

## 2. Railway (Backend + PostgreSQL + Redis)

1. Acesse [railway.app](https://railway.app) e faça login com GitHub
2. Clique **New Project → Deploy from GitHub repo**
3. Selecione `guilhermejlf/sem-aperreio`
4. Railway detecta Python automaticamente

### 2.1 Add-ons
1. No projeto Railway, clique **New → Database → Add PostgreSQL**
2. Clique **New → Database → Add Redis**
3. Railway provisiona automaticamente `DATABASE_URL` e `REDIS_URL`

### 2.2 Variáveis de Ambiente
1. Vá em **Variables → Raw Editor**
2. Adicione:
   ```
   SECRET_KEY=<gerar string aleatória forte de 50+ chars>
   DEBUG=False
   EMAIL_HOST_PASSWORD=<API key do SendGrid>
   FRONTEND_URL=<URL do Vercel - obtida no passo 3>
   TASK_TRIGGER_SECRET=<string aleatória forte>
   ```
3. `DATABASE_URL` e `REDIS_URL` já estão provisionados pelos add-ons

---

## 3. Vercel (Frontend)

1. Acesse [vercel.com](https://vercel.com) e faça login com GitHub
2. Clique **Add New Project → Import Git Repository**
3. Selecione `guilhermejlf/sem-aperreio`
4. Configure:
   - **Framework Preset:** Other (ou Vite)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Adicione variável de ambiente:
   ```
   VITE_API_BASE_URL=https://<seu-projeto>.up.railway.app
   ```
   (Use a URL do Railway obtida após o deploy do backend)
6. Clique **Deploy**

**Copie a URL de produção do Vercel** (ex: `https://sem-aperreio.vercel.app`) para usar no `FRONTEND_URL` do Railway.

---

## 4. GitHub Secrets (CI/CD)

1. No GitHub, vá em **Settings → Secrets and variables → Actions**
2. Adicione cada secret:

| Secret | Valor | Onde obter |
|--------|-------|-----------|
| `RAILWAY_TOKEN` | Token do Railway | Railway Dashboard → Account Settings → Tokens |
| `VERCEL_TOKEN` | Token do Vercel | Vercel Dashboard → Account Settings → Tokens |
| `VERCEL_ORG_ID` | ID da org Vercel | Vercel Dashboard → URL contém `/teams/<org_id>` |
| `VERCEL_PROJECT_ID` | ID do projeto Vercel | Vercel Project → Settings → General → Project ID |
| `VITE_API_BASE_URL` | URL do Railway | Railway Dashboard → seu serviço → Domains |

---

## 5. Celery Beat (Agendamento de Tasks)

O projeto usa `django-celery-beat` com scheduler no banco (PostgreSQL).

### 5.1 Local
```bash
# Terminal 1 — Worker
celery -A backend worker -l info

# Terminal 2 — Beat
celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 5.2 Setup inicial das tarefas
```bash
python manage.py migrate django_celery_beat
python manage.py setup_periodic_tasks
```

### 5.3 Railway (Produção)
Adicione um segundo serviço no Railway com o mesmo repo, mas com start command:
```
celery -A backend worker -l info -c 2 && celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Ou use `Procfile`:
```
web: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A backend worker -l info -c 2
beat: celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

> **Nota:** Se o free tier do Railway não permitir múltiplos serviços, mantenha o cron-job.org como fallback (ver seção 5 Legacy abaixo).

---

## 6. Testar

1. Push para `main` dispara GitHub Actions
2. Verifique em **Actions tab** se `check` passa e deploys completam
3. Teste endpoints:
   ```
   GET https://<railway-url>/api/health/
   GET https://<railway-url>/api/notificacoes/status/
   ```
4. Teste o frontend acessando a URL do Vercel

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Railway deploy falha | Verifique `requirements.txt` tem `gunicorn` |
| PostgreSQL não conecta | Verifique `DATABASE_URL` existe nas variáveis |
| Email não envia | Verifique `EMAIL_HOST_PASSWORD` é a API key do SendGrid |
| CORS error no frontend | Verifique `FRONTEND_URL` no Railway inclui a URL do Vercel |
| cron-job retorna 403 | Verifique `TASK_TRIGGER_SECRET` é igual no Railway e na URL |

