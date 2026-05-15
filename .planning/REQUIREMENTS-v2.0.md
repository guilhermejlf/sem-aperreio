# Requirements: Sem Aperreio — v2.0 Infra & Quality

**Defined:** 2026-05-15
**Core Value:** Familiares conseguem registrar e visualizar todos os gastos do lar em um só lugar, com análises claras que revelam padrões de consumo e oportunidades de economia.

---

## v2.0 Requirements

### Testes Automatizados (TEST)

- [ ] **TEST-01**: Backend — testes unitários para models (User, Family, Gasto, Receita, Meta)
- [ ] **TEST-02**: Backend — testes de integração para endpoints críticos (auth, dashboard, gastos, receitas, metas)
- [ ] **TEST-03**: Backend — testes para previsão ML (dados mínimos, dados suficientes, fallback)
- [ ] **TEST-04**: Frontend — testes unitários para componentes Vue (EmptyState, BaseCard, DashboardInsights)
- [ ] **TEST-05**: E2E — fluxo crítico: login → dashboard → adicionar gasto → ver dashboard atualizado

### Cache & Performance (CACHE)

- [ ] **CACHE-01**: Redis configurado como cache backend no Django
- [ ] **CACHE-02**: Dashboard data cacheado por período (mês/ano) com invalidação automática
- [ ] **CACHE-03**: Previsões ML cacheadas com TTL de 1h (invalidar quando novos dados são inseridos)
- [ ] **CACHE-04**: Categorias e metas cacheadas (raramente mudam, longo TTL)

### PWA Offline (MOB)

- [ ] **MOB-01**: Manifest.json com ícones, tema, display standalone
- [ ] **MOB-02**: Service Worker caching assets estáticos (JS, CSS, fonts, icons)
- [ ] **MOB-03**: Offline fallback page quando não há conexão
- [ ] **MOB-04**: Cache de dados da API (dashboard do mês atual, metas) para uso offline limitado
- [ ] **MOB-05**: Install prompt customizado (não usar o browser default)

### Infraestrutura Adicional (INFRA)

- [ ] **INFRA-04**: Celery Beat interno (migrar de cron-job.org para scheduler interno)
- [ ] **INFRA-05**: Rate limiting na API (prevenir abuso de endpoints públicos)

---

## Out of Scope for v2.0

| Feature | Reason |
|---------|--------|
| Migração Vue Options → Composition API | Grande refactoring; pode ser v3.x |
| Paginação completa com metadados | Parcialmente funcional; não é blocker |
| Open Banking | Fora do escopo de infra/quality |
| OAuth social | Auth polish é v3.1 |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TEST-01 | 12 | Pending |
| TEST-02 | 12 | Pending |
| TEST-03 | 12 | Pending |
| TEST-04 | 13 | Pending |
| TEST-05 | 13 | Pending |
| CACHE-01 | 14 | Pending |
| CACHE-02 | 14 | Pending |
| CACHE-03 | 14 | Pending |
| CACHE-04 | 14 | Pending |
| MOB-01 | 15 | Pending |
| MOB-02 | 15 | Pending |
| MOB-03 | 15 | Pending |
| MOB-04 | 15 | Pending |
| MOB-05 | 15 | Pending |
| INFRA-04 | 16 | Pending |
| INFRA-05 | 16 | Pending |

**Coverage:**
- v2.0 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0 ✓

---

*Requirements defined: 2026-05-15 after v3.2 milestone completion*
