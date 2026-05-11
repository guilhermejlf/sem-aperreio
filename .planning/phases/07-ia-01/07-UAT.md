# Phase 7 — UAT: Assistente Financeiro Conversacional

**Phase:** 07-ia-01 (engloba IA-01, IA-02, IA-03)
**Status:** completed
**Date:** 2026-05-07

## Tests — IA-01 (Parser Base)

| ID | Test | Status | Notes |
|----|------|--------|-------|
| IA01-01 | "uber 25 reais" → IA sugere gasto de R$ 25,00 em Transporte | pass | |
| IA01-02 | "recebi 5 mil" → IA sugere receita de R$ 5.000,00 | pass | |
| IA01-03 | Confirmação do usuário persiste no banco via API existente | pass | |
| IA01-04 | Cancelamento descarta a sugestão sem salvar | pass | |
| IA01-05 | Fallback funciona sem OPENAI_API_KEY configurada | pass | |
| IA01-06 | Botão "Editar" abre modal de gasto pré-preenchido | pass | |

## Tests — IA-02 (Contextual Multi-Etapas)

| ID | Test | Status | Notes |
|----|------|--------|-------|
| IA02-01 | "paguei internet" → IA: "Quanto você gastou com Internet?" | pass | |
| IA02-02 | "140" → IA confirma gasto de R$ 140,00 em Contas e serviços | pass | |
| IA02-03 | "mercado" → IA pergunta valor | pass | |
| IA02-04 | "320" → IA confirma gasto de R$ 320,00 em Mercado | pass | |
| IA02-05 | Contexto é limpo após confirmação ou cancelamento | pass | |
| IA02-06 | Chips de sugestões rápidas clicáveis no estado vazio | pass | |
| IA02-07 | Typing indicator com "Analisando..." | pass | |

## Tests — IA-03 (Continuidade Conversacional)

| ID | Test | Status | Notes |
|----|------|--------|-------|
| IA03-01 | "uber 25" → confirmar → "e mercado 120" → confirmação contínua | pass | |
| IA03-02 | "bom dia" → IA: "Oi! Como posso ajudar?" | pass | |
| IA03-03 | "obrigado" → IA: 👋 despedida | pass | |
| IA03-04 | "não" → IA: 👋 despedida | pass | |
| IA03-05 | Foco mantido no input durante toda a conversa | pass | |
| IA03-06 | Chips de sugestões rápidas após salvar (+ Mercado, + Transporte) | pass | |
| IA03-07 | Chip "Nenhum" para encerrar conversa naturalmente | pass | |
| IA03-08 | Botão Editar aparece em gastos e receitas | pass | |
| IA03-09 | Tom natural nas respostas ("Perfeito!" em vez de "Entendi!") | pass | |

## Verdict

**Result:** PASS (22/22)

All acceptance criteria met across IA-01, IA-02, and IA-03. No blockers.
