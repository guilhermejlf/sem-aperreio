# Como Funciona a Infraestrutura do Sem Aperreio

## Visão Geral

```
┌─────────────────┐     HTTPS      ┌──────────────────┐
│   Vercel        │ ──────────────> │    Railway       │
│  (Frontend)     │                 │   (Backend API)  │
│  Vue 3 + Vite   │                 │  Django + Gunicorn│
└─────────────────┘                 └────────┬─────────┘
      ▲                                      │
      │                                      │ PostgreSQL
      │                                      │ (dados)
      │                                      │
      │          ┌─────────────────┐        │
      │          │  cron-job.org   │        │
      │          │  (Agendador)    │        │
      │          │                 │        │
      │          │  Seg 9h ────────┼────────┘
      │          │  Seg 10h ───────┘
      │          │  (a cada 10min) │
      │          └─────────────────┘
      │
      │          ┌─────────────────┐
      └──────────│   SendGrid      │
                 │  (Email SMTP)   │
                 │                 │
                 │  smtp.sendgrid   │
                 │     .net:587    │
                 └─────────────────┘
```

---

## 1. Railway (Backend)

### O que é
Plataforma de deploy de aplicações. Você conecta seu repositório GitHub e ela faz o deploy automaticamente.

### O que roda lá
- **Django** (backend Python)
- **Gunicorn** (servidor WSGI que recebe requests HTTP e passa para o Django)
- **PostgreSQL** (banco de dados, Railway oferece como add-on)

### Como funciona o deploy
1. Push no branch `main` do GitHub
2. GitHub Actions dispara o workflow `.github/workflows/deploy.yml`
3. O workflow roda `railway up` (CLI do Railway)
4. Railway detecta que é Python (via `railway.json` ou `Procfile`)
5. Instala dependências (`pip install -r requirements.txt`)
6. Roda migrações (`python manage.py migrate`)
7. Inicia Gunicorn (`gunicorn backend.wsgi`)

### Variáveis de ambiente (Settings → Variables)
```
DATABASE_URL=postgresql://postgres:senha@host:5432/railway
SECRET_KEY=sk-jlf-2026-...
FRONTEND_URL=https://sem-aperreio.vercel.app
TASK_TRIGGER_SECRET=sk-jlf-2026-phase6-notifications-abc123xyz789
EMAIL_HOST_PASSWORD=SG.xxxxx
```

### Free tier vs Pago
| | Free | Hobby (~$5/mês) |
|---|---|---|
| CPU/Memória | Limitada | Melhor |
| Sleep | Dorme após inatividade | Sempre ligado |
| Banco PostgreSQL | Limitado a 500MB | Ilimitado |
| Logs | 7 dias | 30 dias |

> **Cold start**: No free tier, se ninguém acessa por ~15 min, o Railway "dorme" o container. O primeiro request demora 10-30s para "acordar". Por isso criamos o cron-job de warmup.

---

## 2. Vercel (Frontend)

### O que é
Plataforma de deploy para frontend. Otimizada para React, Vue, Next.js, etc.

### O que roda lá
- **Vue 3** (framework JavaScript)
- **Vite** (build tool — empacota Vue em HTML/CSS/JS estático)
- Arquivos estáticos (não há servidor Node rodando, é só CDN)

### Como funciona o deploy
1. Push no branch `main` do GitHub
2. GitHub Actions dispara o workflow
3. O workflow roda:
   ```bash
   cd frontend
   npm ci
   npm run build   # Vite gera a pasta dist/
   vercel --prod   # Envia dist/ para Vercel
   ```
4. Vercel serve os arquivos de `dist/` via CDN global

### Por que `vercel.json`?
```json
{
  "routes": [
    { "handle": "filesystem" },
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```
- SPA (Single Page Application): Vue gerencia rotas no browser
- Sem o `vercel.json`, tentar acessar `/dashboard` daria 404 (arquivo não existe)
- O `filesystem` primeiro tenta servir arquivos reais (JS, CSS, imagens)
- Se não encontrar, redireciona para `index.html` (Vue pega e renderiza a rota certa)

### Free tier
- **Ilimitado** para projetos pessoais
- CDN global automático
- Custom domain grátis (`.vercel.app`)
- Não dorme — sempre online

---

## 3. SendGrid (Email)

### O que é
Serviço de envio de email da Twilio. Oferece SMTP e API REST.

### Como funciona no Django
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'          # sempre "apikey"
EMAIL_HOST_PASSWORD = 'SG.xxxxx'     # API key do SendGrid
```

### Fluxo de envio
```
Django → smtp.sendgrid.net:587 → SendGrid → Gmail/Yahoo/etc
```

### `fail_silently=True`
Se o email falhar (ex: SendGrid offline, conta suspensa), o Django **não quebra** a aplicação. Só ignora o erro e continua.

### Por que não usar Gmail direto?
| | Gmail pessoal | SendGrid |
|---|---|---|
| Limite diário | 100 emails | 100 emails/dia (free) |
| Reputação | Pode ir para spam | Melhor entregabilidade |
| Configuração | App password + less secure apps | API key simples |
| Logs | Nenhum | Dashboard com aberturas, cliques, bounces |

### Como pegar a API key
1. Crie conta em https://sendgrid.com
2. Verifique um "sender" (domínio ou email)
3. Settings → API Keys → Create API Key → Full Access
4. Copie a key (SG.xxxxx) e coloque na variável `EMAIL_HOST_PASSWORD` do Railway

---

## 4. cron-job.org (Agendador)

### O que é
Serviço gratuito que faz requests HTTP em horários agendados. É como um "despertador" para sua API.

### Por que usar?
O Railway free tier **não permite workers persistentes** (Celery, cron interno). Então usamos cron-job.org para "acordar" o Railway e rodar tarefas.

### Os 3 jobs configurados

| Job | URL | Quando | Para quê |
|-----|-----|--------|----------|
| **Warmup** | `/api/health/` | A cada 10 min | Mantém Railway acordado (evita cold start) |
| **Weekly Reminder** | `/api/tasks/trigger/?task=reminder` | Segunda 9h | Envia resumo semanal por email |
| **Average Alert** | `/api/tasks/trigger/?task=average` | Segunda 10h | Verifica se gasto > média + 20% |

### Headers configurados
```
X-Trigger-Secret: sk-jlf-2026-phase6-notifications-abc123xyz789
```
Isso protege o endpoint — sem a secret, retorna 403 Unauthorized.

### Como funciona o fluxo
```
1. cron-job.org faz POST para /api/tasks/trigger/?task=reminder
2. Railway recebe, valida X-Trigger-Secret
3. Inicia thread de background com send_weekly_reminder()
4. Retorna imediatamente: {"status":"started","task":"reminder"}
5. Thread continua rodando e envia emails via send_mass_mail()
```

### Limitações do free tier do cron-job.org
- Timeout de 30 segundos (por isso usamos thread de background)
- Máximo de alguns jobs (suficiente para 3)
- Logs básicos de execução

---

## Resumo: Quem faz o quê?

| Serviço | Função | Pago? |
|---------|--------|-------|
| **Railway** | Roda o backend Django + PostgreSQL | Free (limitado) |
| **Vercel** | Serve o frontend Vue estático via CDN | Free (ilimitado) |
| **SendGrid** | Envia emails transacionais | Free (100/dia) |
| **cron-job.org** | Agenda chamadas HTTP para tarefas | Free |
| **GitHub** | Repositório + CI/CD (GitHub Actions) | Free (público) |

**Custo total: $0/mês** (todos os tiers free).

---

## Possíveis upgrades futuros

| Serviço | Upgrade | Custo | Benefício |
|---------|---------|-------|-----------|
| Railway | Hobby tier | ~$5/mês | Sem cold start, mais recursos |
| SendGrid | Essentials | ~$20/mês | 50k emails/mês, melhor reputação |
| cron-job.org | Pro | ~$5/mês | Mais jobs, timeout maior, webhooks |
| Vercel | Pro | ~$20/mês | Analytics, mais bandwidth, suporte |
