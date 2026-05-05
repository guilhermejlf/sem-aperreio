# Phase 6 Context: Notificações e Deploy

**Captured:** 2026-05-05 via `/gsd-discuss-phase 6`
**Status:** Ready for planning
**Source:** Discuss-phase com usuário

---

## Domain Boundary

Esta fase entrega infraestrutura de produção (PostgreSQL, CI/CD, deploy automatizado) e notificações por email (lembretes semanais + alertas de média histórica). Não adiciona novas features visuais — torna o sistema confiável e comunicativo em produção.

---

## Implementation Decisions

### 1. Lembrete Semanal (NOTF-01)

**Canal:** Email (SMTP/SendGrid)
- Razão: Mais confiável que push (funciona com app fechado); Django tem suporte nativo (`django.core.mail`)
- Serviço: SendGrid (free tier = 100 emails/dia) ou SMTP do provedor de hospedagem

**Agendamento:** Celery + Redis
- Razão: Padrão da comunidade Django; suporta tarefas periódicas (celery beat)
- Redis: broker e backend de resultados; free tier no Render/Railway
- Alternativa descartada: cron job (depende de suporte da plataforma), polling frontend (não é push real)

**Conteúdo do email:**
- Assunto: "Sem Aperreio — Lembrete semanal de gastos"
- Corpo: Resumo dos gastos da semana (total, categoria mais gasta, meta mais próxima do limite)
- Link CTA: "Registrar gasto →" (link para o app)

### 2. Alerta de Média Histórica (NOTF-02)

**Cálculo:** Média dos últimos 6 meses (excluindo mês atual)
- Razão: Equilíbrio entre estabilidade e resposta a mudanças de padrão
- Fórmula: `media = sum(gastos dos últimos 6 meses) / 6`
- Alerta dispara quando: `gasto_mes_atual > media * 1.2` (20% acima da média)

**Disparo:** Job agendado via Celery (email semanal)
- Razão: Não requer usuário abrir o app; unificado com NOTF-01 na mesma infraestrutura
- Frequência: Semanal (mesmo job que o lembrete, ou job separado)
- Conteúdo: "Seu gasto em [CATEGORIA] este mês está 35% acima da média histórica (R$ 450 vs média R$ 300)"

**Alternativa descartada:** Toast síncrono (ao adicionar gasto) — mantido para alertas de meta (Phase 5), mas para média histórica o email semanal é mais apropriado (usuário não precisa estar no app).

### 3. CI/CD (INFR-02)

**Escopo:** Lint + build + deploy (sem testes automatizados)
- Razão: Foco em entregar infraestrutura rápido; testes ficam para backlog v2.1
- GitHub Actions: workflow em `.github/workflows/deploy.yml`
- Passos:
  1. Checkout
  2. Setup Python + Node
  3. `python manage.py check` (validação Django)
  4. `npm run build` (frontend)
  5. Deploy backend (Railway via CLI)
  6. Deploy frontend (Vercel via CLI)

**Testes:** Diferidos para fase futura (backlog)
- Razão: Adicionaria 1-2 dias ao escopo; Phase 6 já tem 5 deliverables grandes
- Nota: Quando testes forem implementados, CI já está pronto para rodá-los

### 4. Deploy + PostgreSQL (INFR-01/03)

**Plataforma:**
- Backend: Railway (web service + PostgreSQL add-on)
- Frontend: Vercel (static site, build a partir do diretório `frontend/dist`)
- Razão: Railway tem melhor DX para Django; Vercel é padrão para Vue/Vite

**Migração SQLite → PostgreSQL:**
- Estratégia: PostgreSQL só em produção; SQLite continua para dev local
- Django settings: `DATABASE_URL` via env var; fallback para SQLite se não definido
- Migrations: Rodam automaticamente no deploy via `python manage.py migrate` (Railway start command)
- Risco: Possíveis incompatibilidades SQLite vs PostgreSQL (ex: JSONField, DateTimeField com timezone)
- Mitigação: Django ORM abstrai a maioria; testar campos específicos antes do deploy

**Alternativa descartada:** Testar PostgreSQL local primeiro — requer instalação local do Postgres/Docker; migração no deploy é aceitável para este escopo.

---

## Integration Points

- Reusa infraestrutura de email do Django (`django.core.mail`)
- Reusa Celery/Redis para ambos os jobs (lembrete + alerta de média)
- `settings.py`: `DATABASE_URL` para PostgreSQL em produção, SQLite em dev
- ` Procfile` ou equivalente Railway: `web: gunicorn backend.wsgi`
- GitHub Actions: secrets para `RAILWAY_TOKEN` e `VERCEL_TOKEN`

---

## Deferred Ideas

- Testes automatizados (v2.1 ou v3)
- Blacklist de tokens JWT (não necessário para MVP)
- Push notifications do navegador (PWA/service worker — pode ser v2.1)
- Notificações por WhatsApp/Telegram
- Backup automatizado do banco PostgreSQL (Railway faz snapshots, mas backup externo é futuro)

---

## Canonical References

- `.planning/PROJECT.md` — Tech stack, constraints, key decisions
- `.planning/REQUIREMENTS.md` — NOTF-01, NOTF-02, INFR-01, INFR-02, INFR-03
- `.planning/ROADMAP.md` — Phase 6 boundary
- `.planning/STATE.md` — Current state, tech debt notes
- `backend/backend/settings.py` — Current database/settings
- `frontend/package.json` — Build scripts
- `api/views.py` — Existing views to integrate with

---

*Phase: 06-notifications-deploy*
*Context gathered: 2026-05-05 via discuss-phase*
