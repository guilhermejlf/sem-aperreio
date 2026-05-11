# Phase 8: Auth Polish - Context

**Gathered:** 2026-05-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Melhorar UX de autenticação do sistema: password reset via email, login por email/username, validação de senha forte, confirmação de email e polimento visual da tela de login/registro. Não inclui novas capacidades como OAuth ou 2FA.

</domain>

<decisions>
## Implementation Decisions

### Password Reset Flow
- **D-01:** Link com token único no email — usuário clica no link e vai para página de redefinição de senha
- Token expira após 24 horas
- Página de redefinição valida token e permite nova senha

### Email Verification
- **D-02:** Bloqueia login completamente até confirmar email
- Conta criada mas inativa até clique no link de confirmação
- Login retorna erro específico: "Confirme seu email antes de entrar"
- Link de confirmação expira em 48 horas

### Login Field (Username or Email)
- **D-03:** Campo único inteligente — label "Usuário ou Email"
- Backend detecta se contém "@" e busca por email ou username automaticamente
- Frontend: um só campo, sem complicação para o usuário

### Password Strength Validation
- **D-04:** Padrão web — mínimo 8 caracteres, pelo menos 1 maiúscula, 1 minúscula, 1 número, 1 caractere especial (@!#$% etc.)
- Feedback visual em tempo real no frontend (barra de força ou checklist)
- Registro rejeita senhas fracas com mensagem clara

### Visual Polish
- **D-05:** Manter tema escuro/glassmorphism existente — não redesenhar a tela
- Adicionar link "Esqueci minha senha" abaixo do botão de login
- Adicionar campo "Confirmar senha" no registro
- Adicionar indicador de força da senha no registro
- Melhorar mensagens de erro (mais amigáveis, em português)
- Loading states claros nos botões

### Claude's Discretion
- Estilo exato do indicador de força de senha (barra vs checklist)
- Animações de transição entre login/registro
- Ícones específicos para estados de erro/sucesso
</decisions>

<specifics>
## Specific Ideas

- Link "Esqueci minha senha" deve abrir um modal ou ir para tela separada (decidir no planning)
- Página de redefinição de senha deve ser acessível via link do email (rota pública)
- Email de confirmação e reset devem usar templates HTML no padrão dark theme do app
- Mensagens de erro devem ser amigáveis: "Ops, sua senha precisa de pelo menos 8 caracteres..." em vez de erros técnicos
</specifics>

<canonical_refs>
## Canonical References

### Auth Backend
- `api/views_auth.py` — Endpoints existentes (RegisterView, LoginView, RefreshView, UserView)
- `api/serializers_auth.py` — RegisterSerializer atual (username, email, first_name, password min 6)
- `api/models.py` — User model padrão Django (usado em Family, Gasto, etc.)

### Auth Frontend
- `frontend/src/components/AuthView.vue` — Tela principal com tabs login/registro
- `frontend/src/components/LoginForm.vue` — Form de login (username + password)
- `frontend/src/components/RegisterForm.vue` — Form de registro

### Email Infrastructure
- `api/tasks.py` — Tasks de email existentes (SendGrid)
- `api/templates/emails/` — Templates HTML de email (base_email.html, etc.)
- `backend/settings/base.py` — Config de email (SendGrid SMTP)

### API Config
- `frontend/src/config/api.js` — Endpoints e apiRequest helper
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AuthView.vue` — estrutura de tabs login/registro pode ser estendida
- Templates de email em `api/templates/emails/` — reutilizar base_email.html
- `apiRequest` helper no frontend — já lida com headers, JSON, erros
- `Button` do PrimeVue — usado nos forms

### Established Patterns
- JWT via simplejwt — access + refresh tokens
- Django User model padrão — pode ser extendido com profile se necessário
- SendGrid SMTP para email — já configurado em produção
- Tema escuro com gradientes — manter consistência visual

### Integration Points
- Novo endpoint `/api/auth/password-reset/` e `/api/auth/password-reset/confirm/`
- Novo endpoint `/api/auth/verify-email/` para confirmação
- Ajuste no `LoginView` para aceitar email ou username
- Ajuste no `RegisterSerializer` para validar senha forte
- Novas rotas no frontend para password reset e email verification
</code_context>

<deferred>
## Deferred Ideas

- OAuth (Google/Facebook) — nova capacidade, fora do escopo desta fase
- Troca de senha logada (perfil do usuário) — pode ser adicionada depois
- 2FA/MFA — overkill para app de controle de gastos
- Rate limiting em endpoints de auth — boa prática, mas pode ser adicionado depois
</deferred>

---

*Phase: 08-auth-polish*
*Context gathered: 2026-05-11*
