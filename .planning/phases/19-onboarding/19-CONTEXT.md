# Phase 19 — Onboarding Experience (ONBOARD-01..05)

## Phase Boundary
User activation for new users. NOT a tutorial/wizard. Teach by doing.

## Principles
- ✅ Show value quickly
- ✅ Teach by context
- ✅ Allow free exploration
- ✅ Save progress
- ✅ Allow resume later
- ❌ No 4-8 screen wizard
- ❌ No blocking overlay
- ❌ No mandatory tooltip sequence
- ❌ No forced navigation order

## Decisions

### Format
- Single welcome modal (NOT carousel, NOT multi-screen)
- Dashboard checklist always visible until dismissed
- Contextual tooltips per tab, shown once only
- No blocking overlays anywhere

### Welcome Modal (ONBOARD-01)
- Component: `components/onboarding/WelcomeModal.vue`
- Trigger: first login + onboarding not completed
- Actions: "Começar" (focuses checklist) or "Explorar sozinho" (just close)
- No Next button, no slides

### Activation Checklist (ONBOARD-02)
- Component: `components/onboarding/OnboardingChecklist.vue`
- Position: dashboard, above main cards, below header
- Items: group created, first expense, first revenue, first goal
- Progress: calculated dynamically (not stored)
- Completion: shows celebration message + "Ocultar checklist" button
- Hidden: can be re-opened via Settings "Ver onboarding novamente"

### Contextual Tooltips (ONBOARD-03)
- 4 tooltips, one per tab, shown ONCE per user
- Tabs: Família, Metas, Bené (AI), Extrato
- Small, dismissible, never auto-reappear
- Stored per-user in backend flags

### Backend Persistence (ONBOARD-04)
- New fields on UserProfile:
  - `onboarding_completed` (bool, default=False)
  - `seen_family_tooltip` (bool)
  - `seen_budget_tooltip` (bool)
  - `seen_bene_tooltip` (bool)
  - `seen_statement_tooltip` (bool)
- New endpoint: `GET /api/onboarding/` — returns checklist state + progress%
- Progress calculated dynamically from user data

### Resume Later (ONBOARD-05)
- Settings option: "Ver onboarding novamente"
- Re-opens WelcomeModal + shows checklist
- Does NOT reset user data (expenses, revenues, goals, group)

### Empty States
- Dashboard: prompt to add first expense
- Extrato: prompt to add first transaction
- Metas: prompt to create first goal
- Receitas: prompt to add first revenue
- Família: prompt to create/join group

## Design
- Follow existing design system, motion system, dark theme, spacing tokens, visual hierarchy
- Premium card styling for checklist

## Canonical Refs
- `frontend/src/App.vue` — tab routing, auth state
- `frontend/src/components/AuthView.vue` — post-login entry point
- `api/models.py` — UserProfile model
- `api/serializers_auth.py` — UserProfile serializer
- `api/views_auth.py` — auth views
- `frontend/src/stores/toast.store.js` — toast system
- `.planning/PROJECT.md` — design system constraints
