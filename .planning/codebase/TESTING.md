# Estado de Testes

## Resumo

| Tipo | Status | Cobertura |
|------|--------|-----------|
| Testes unitários backend | ❌ Não existe | 0% |
| Testes unitários frontend | ❌ Não existe | 0% |
| Testes de integração API | ❌ Não existe | 0% |
| Testes E2E | ❌ Não existe | 0% |
| Testes do modelo ML | ⚠️ Scripts manuais | Baixa |
| CI/CD | ❌ Não existe | — |

## Scripts de Verificação Manual

### `treinar_modelo.py`

- **Propósito**: Treinar `LinearRegression` com dados hardcoded (12 meses)
- **Saída**: Arquivo `modelo.pkl` em `backend/api/`
- **Limitação**: Não verifica acurácia, overfitting ou métricas

### `testar_modelo.py`

- **Propósito**: Carregar `modelo.pkl` e prever valor para mês 6
- **Execução**: Manual, via linha de comando
- **Limitação**: Testa apenas um caso; não é um teste automatizado

## Pontos Críticos Sem Testes

1. **Validação de serializer** (`GastoSerializer`): `validate_valor`, `validate_data`, `validate_categoria`
2. **Validação de modelo** (`Gasto.clean()`): regra de 1 ano no passado
3. **Views da API**:
   - Filtros combinados (`categoria` + `data_inicio` + `data_fim`)
   - Paginação (`limite` > 100 deve ser clamped)
   - Erro 404 em `gasto_detail`
   - Erro 503 quando `modelo.pkl` está ausente
4. **Lazy loading do modelo ML**: comportamento quando arquivo não existe
5. **Formatadores do frontend**:
   - `formatarData` com múltiplos formatos de entrada
   - `formatarTempo` (relativo: "agora", "5 min atrás", etc.)
6. **Gráficos Chart.js**: inicialização/destruição correta dos canvases

## Como Executar Verificações Atuais

```bash
# Backend
python manage.py migrate        # verifica migrations
python manage.py runserver      # verifica startup
python treinar_modelo.py        # gera modelo

# Frontend
npm install                     # verifica instalação
npm run dev                     # verifica build/dev
npm run build                   # verifica build de produção
```

## Recomendação

Adicionar:
- `pytest-django` para testes de API
- `pytest` para testes do modelo ML
- `vitest` ou `@vue/test-utils` + `jest` para componentes Vue
- Testes de contrato (status codes, shape de JSON) nos endpoints
