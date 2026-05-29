# Phase 19 — Onboarding Experience — Implementation Plan

## Step 1: Backend — UserProfile fields + endpoint
- Add `onboarding_completed`, `seen_*_tooltip` fields to UserProfile
- Create `OnboardingStatusView` (GET /api/onboarding/)
- Add migration
- Register URL

## Step 2: Frontend — Onboarding components
- Create `components/onboarding/` directory
- `WelcomeModal.vue` — simple modal, two buttons, no carousel
- `OnboardingChecklist.vue` — checklist card with progress bar, 4 items

## Step 3: Frontend — Integration into Dashboard
- Show WelcomeModal on first login (when onboarding not done)
- Show Checklist on dashboard, above main cards
- Hide checklist button when 100%
- Connect to /api/onboarding/ endpoint

## Step 4: Frontend — Contextual tooltips
- Create lightweight tooltip component (small, dismissible, once-only)
- Add to Família, Metas, Bené (AI), Extrato views
- Check `seen_*_tooltip` flag before showing

## Step 5: Frontend — Improved empty states
- Update empty states with guided CTAs
- Dashboard, Extrato, Metas, Receitas, Família

## Step 6: Frontend — Settings "Resume onboarding"
- Add toggle/button in user settings to re-open onboarding
- Reset visual flags only (not user data)

## Step 7: Build + commit + push
