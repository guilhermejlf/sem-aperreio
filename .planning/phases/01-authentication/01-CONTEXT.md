# Phase 1: Autenticação JWT — Contexto de Decisões

**Gathered:** 2026-04-24
**Status:** Ready for execution
**Source:** Discuss-phase com usuário

## Domain Boundary

Esta fase entrega autenticação JWT completa no backend (Django + DRF + SimpleJWT) e no frontend (Vue 3). Usuários podem se registrar, fazer login, e acessar endpoints protegidos. Gastos passam a ser vinculados ao usuário autenticado.

## Implementation Decisions

### Tela de Login/Cadastro
- **Layout**: Tabs na mesma tela — um card centralizado com abas "Entrar" e "Criar Conta"
- **Razão**: Alternância rápida entre login e cadastro; padrão moderno
- **Tema**: Escuro, consistente com o App.vue existente (radial-gradient #0f172a, acentos #22c55e)

### Dados Obrigatórios no Cadastro
- **Campos**: `nome` (first_name), `email`, `username`, `password`
- **Validação**: email deve ser único; senha mínimo 6 caracteres
- **Razão**: Email será necessário para futuras features (recuperação de senha, notificações)
- **Modelo**: Usar `User` padrão do Django (não custom model); campos extras via serializer

### Banco de Dados Existente
- **Decisão**: Resetar `db.sqlite3` e refazer migrations
- **Razão**: MVP, sem dados críticos; adicionar FK `user` ao `Gasto` requer migration complexa com default
- **Ação**: Deletar db.sqlite3, remover migrations antigas, gerar nova migration inicial

### Logout e Expiração de Token
- **Access token lifetime**: 30 minutos
- **Refresh token lifetime**: 7 dias
- **Logout**: Limpa tokens do `localStorage` e redireciona para tela de login
- **Invalidação no backend**: Não ativar blacklist (SimpleJWT padrão)
- **Razão**: MVP — segurança de nível básico é suficiente; blacklist adiciona complexidade

### Grupo Familiar
- **Decisão**: NÃO incluir na Phase 1; deixar para Phase 2
- **Razão**: Manter escopo focado; autenticação individual é pré-requisito estável antes de adicionar compartilhamento
- **Implicação**: Cada usuário vê APENAS seus próprios gastos na Phase 1

### Frontend — Token Storage
- **Storage**: `localStorage` (chaves `sa_access_token`, `sa_refresh_token`)
- **Auto-refresh**: Se access token expirar (401), tentar refresh automaticamente; se falhar, redirecionar ao login
- **Razão**: localStorage é simples e persistente; interceptador garante transparência

### Backend — Views de Gastos
- **Permission**: `IsAuthenticated` global (default em settings.py)
- **Queryset**: `Gasto.objects.filter(user=request.user)` — cada usuário vê só seus gastos
- **Serializer**: `user` como `read_only_field` (auto-populado pelo view)

## Canonical References

**Downstream agents MUST read these before implementing.**

### Decisões de projeto
- `.planning/PROJECT.md` — Contexto geral, constraints, key decisions
- `.planning/REQUIREMENTS.md` — Requisitos AUTH-01 a AUTH-05
- `.planning/ROADMAP.md` — Phase boundary e entregáveis

### Código base
- `backend/backend/settings.py` — Configurações Django/DRF atuais
- `backend/api/models.py` — Modelo Gasto atual
- `backend/api/views.py` — Views de gastos atuais (function-based)
- `backend/api/serializers.py` — GastoSerializer atual
- `backend/api/urls.py` — Rotas atuais
- `frontend-ia/src/App.vue` — App root atual com tabs e gastos
- `frontend-ia/src/config/api.js` — Helper de API atual
- `frontend-ia/src/main.js` — Bootstrap Vue/PrimeVue

## Specific Ideas

- Card de login/cadastro centralizado com gradiente radial escuro (#0f172a → #020617) e bordas arredondadas (border-radius: 16px)
- Abas estilo pills ou underline (usar classes CSS consistentes com App.vue)
- Input de senha com ícone de olho para mostrar/esconder (opcional, não obrigatório)
- Botão de submit com gradiente verde (#22c55e → #16a34a) consistente com App.vue
- Mensagem de erro inline em vermelho (#ef4444) abaixo do campo
- Logo "Sem Aperreio" no topo do card de login (reutilizar logo existente)

## Deferred Ideas

- Recuperação de senha por email (futura feature)
- Blacklist de tokens no backend (não necessário para MVP)
- Grupo familiar / convites (Phase 2)
- Custom User model (usar Django padrão; se necessário, extender via Profile na Phase 2)

---
*Phase: 01-authentication*
*Context gathered: 2026-04-24 via discuss-phase*
