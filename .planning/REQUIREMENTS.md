# Requirements: Sem Aperreio — v3.1 Auth Polish

**Defined:** 2026-05-11
**Core Value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

---

## v3.1 Requirements

### Autenticação (AUTH)

- [ ] **AUTH-04**: Usuário pode solicitar redefinição de senha via email (esqueci minha senha)
- [ ] **AUTH-05**: Login aceita username OU email no mesmo campo
- [ ] **AUTH-06**: Registro exige senha forte (mínimo 8 caracteres, 1 maiúscula, 1 número) e confirmação de senha
- [ ] **AUTH-07**: Email de confirmação enviado no cadastro; conta fica inativa até confirmação

### UX / Interface (UI)

- [ ] **UI-02**: Tela de login/registro com melhorias visuais (feedback de erro, acessibilidade, loading states)

---

## Future / Out of Scope for v3.1

| Feature | Reason |
|---------|--------|
| 2FA/MFA | Overkill para app de controle de gastos familiar |
| OAuth (Google/Facebook) | Boa ideia para v3.2, mas fora do escopo de polish |
| Troca de senha logada | Pode ser adicionada no perfil do usuário depois |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-04 | Phase 8 | Pending |
| AUTH-05 | Phase 8 | Pending |
| AUTH-06 | Phase 8 | Pending |
| AUTH-07 | Phase 8 | Pending |
| UI-02 | Phase 8 | Pending |

**Coverage:**
- v3.1 requirements: 5 total
- Mapped to phases: 5
- Unmapped: 0 ✓

---

*Requirements defined: 2026-05-11 after v3.1 milestone initialization*
