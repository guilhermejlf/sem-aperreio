# Phase 1: Autenticação JWT — UI Design Contract

**Phase:** 01-authentication
**Date:** 2026-04-24
**Source:** Discuss-phase decisions + existing App.vue visual patterns

---

## Screen: AuthView (Login / Cadastro)

**Purpose:** Primeira tela do app quando usuário não tem token. Permite login ou cadastro em tabs.

### Layout

- **Container**: Tela cheia, fundo `radial-gradient(circle at center, #0f172a 0%, #020617 100%)` — mesmo do App.vue
- **Card centralizado**:
  - `max-width: 420px`
  - `padding: 2rem`
  - `border-radius: 16px`
  - `border: 1px solid rgba(255, 255, 255, 0.1)`
  - `background: rgba(255, 255, 255, 0.05)`
  - `backdrop-filter: blur(12px)`
  - Centralizado vertical e horizontalmente com flexbox

### Header do Card

- **Logo/Ícone**: Ícone de casa ou "wallet" (PrimeVue `pi pi-wallet` ou `pi pi-home`) em `#22c55e`, tamanho 48px, centered
- **Título**: "Sem Aperreio" — fonte 1.75rem, weight 700, cor branca
- **Subtítulo**: "Controle seus gastos domésticos" — fonte 0.875rem, cor `rgba(255,255,255,0.6)`

### Tabs

- **Estilo**: Pills (botões arredondados) ou underline — preferência por **pills**
- **Container**: `display: flex`, `gap: 0.5rem`, `margin-bottom: 1.5rem`, centered
- **Tab ativa**: `background: #22c55e`, `color: #020617`, `border-radius: 999px`, `padding: 0.5rem 1.25rem`, `font-weight: 600`
- **Tab inativa**: `background: transparent`, `color: rgba(255,255,255,0.6)`, `border: 1px solid rgba(255,255,255,0.15)`, mesmo border-radius e padding
- **Transição**: `transition: all 0.2s ease`
- **Tabs**: "Entrar" | "Criar Conta"

### Form — Login (Tab "Entrar")

- **Campo username**:
  - Label: "Usuário" — cor branca, fonte 0.875rem, margin-bottom 0.25rem
  - Input: PrimeVue `InputText`, fundo `rgba(255,255,255,0.05)`, border `1px solid rgba(255,255,255,0.1)`, border-radius 8px, padding 0.75rem, cor texto branca
  - Placeholder: "seu_usuario"
  - Focus: border-color `#22c55e`

- **Campo password**:
  - Label: "Senha"
  - Input: `InputText type="password"`, mesmo estilo do username
  - Placeholder: "••••••"

- **Botão "Entrar"**:
  - `width: 100%`, `padding: 0.75rem`, `border-radius: 8px`
  - Fundo: gradiente `linear-gradient(135deg, #22c55e, #16a34a)`
  - Texto: branco, weight 600
  - Hover: `filter: brightness(1.1)`
  - Loading: spinner branco dentro do botão, desabilitado

- **Mensagem de erro**: texto `#ef4444` (vermelho), fonte 0.875rem, margin-top 0.75rem, centered

### Form — Cadastro (Tab "Criar Conta")

- **Campo nome**:
  - Label: "Nome"
  - Input: mesmo estilo
  - Placeholder: "Seu nome"

- **Campo email**:
  - Label: "E-mail"
  - Input: `InputText type="email"`, mesmo estilo
  - Placeholder: "seu@email.com"

- **Campo username**:
  - Label: "Usuário"
  - Placeholder: "seu_usuario"

- **Campo password**:
  - Label: "Senha"
  - Input: password, placeholder "Mínimo 6 caracteres"

- **Campo confirmar senha**:
  - Label: "Confirmar senha"
  - Input: password
  - Validação inline: se não coincidir, borda vermelha + mensagem abaixo

- **Botão "Criar Conta"**: mesmo estilo do botão "Entrar", texto "Criar Conta"

- **Mensagem de erro**: mesmo estilo vermelho

### Estados

| Estado | Visual |
|--------|--------|
| Default | Form limpo, tabs em estado inicial |
| Loading | Botão com spinner, inputs desabilitados (`opacity: 0.5`, `pointer-events: none`) |
| Erro | Mensagem vermelha abaixo do form, shake sutil no card (opcional) |
| Sucesso login | Tab some (ou não — depende de UX), App.vue mostra dashboard |
| Sucesso cadastro | Login automático, transição direta para dashboard |

### Transições

- **Tab switch**: sem animação ou fade de 150ms no conteúdo do form
- **Auth success**: fade-out do card (opacity 0 → removed) enquanto App.vue fade-in o conteúdo principal

---

## Screen: App.vue (Já Logado) — Adições

### Header / Nav

- **Botão Logout**: ícone `pi pi-sign-out` + texto "Sair" ou só ícone
- **Posição**: canto superior direito, ao lado do seletor de tema (se houver)
- **Estilo**: `padding: 0.5rem`, `border-radius: 8px`, `background: rgba(239,68,68,0.15)` (vermelho suave), `color: #ef4444`, `border: 1px solid rgba(239,68,68,0.3)`
- **Hover**: `background: rgba(239,68,68,0.25)`

---

## Component Breakdown

| Component | Responsabilidade | Props / Events |
|-----------|------------------|---------------|
| `AuthView.vue` | Card, tabs, layout, logo | `@authenticated` |
| `LoginForm.vue` | Form de login, chamada API, validação | `@success` |
| `RegisterForm.vue` | Form de cadastro, validação local, chamada API, auto-login | `@auth-success` |

---

## Responsive

- **Mobile (< 640px)**: Card `width: 100%`, `margin: 1rem`, padding reduzido para `1.5rem`
- **Tablet+**: Card centralizado com max-width 420px

---

## Accessibility

- Labels associados aos inputs (`for` attribute)
- Botões com `type="submit"` dentro de `<form>`
- Estados de erro anunciados via `aria-live="polite"` (opcional, não bloqueante)
- Contraste: texto branco sobre fundo escuro — OK

---

## Design Tokens (Reutilizados do App.vue)

| Token | Valor | Uso |
|-------|-------|-----|
| `--bg-dark` | `#0f172a` | Fundo principal |
| `--bg-darker` | `#020617` | Fundo gradiente edge |
| `--accent` | `#22c55e` | Tabs ativas, botões, focus |
| `--accent-dark` | `#16a34a` | Gradient botão |
| `--danger` | `#ef4444` | Erros |
| `--text-primary` | `#ffffff` | Títulos, labels |
| `--text-secondary` | `rgba(255,255,255,0.6)` | Subtítulos, placeholders |
| `--surface` | `rgba(255,255,255,0.05)` | Card background |
| `--border` | `rgba(255,255,255,0.1)` | Bordas |

---

*UI-SPEC gerado a partir das decisões do discuss-phase (2026-04-24).*
