# Preocupações e Dívida Técnica

## Crítico

### 1. Sem Autenticação
- `DEFAULT_AUTHENTICATION_CLASSES = []` + `AllowAny`
- Qualquer pessoa pode criar, editar, excluir e listar todos os gastos
- **Impacto**: Dados abertos; não há isolamento por usuário
- **Status**: Documentado no README como "próximo passo"

### 2. Modelo de IA com Dados Fixos
- `treinar_modelo.py` usa array hardcoded de 12 meses
- Previsão baseada apenas no número do mês (feature única)
- Não utiliza dados reais do banco SQLite para treinamento
- **Impacto**: Previsões não representam o perfil do usuário
- **Status**: Documentado no README como "próximo passo"

### 3. CSRF Desabilitado em Dev (comentário perigoso)
- Comentário em `settings.py`: "vamos desabilitar CSRF para API (dev)"
- CSRF middleware ainda está na lista, mas a intenção é confusa
- Com `CORS_ALLOW_ALL_ORIGINS = True`, a API aceita requisições de qualquer origem em dev

## Alto

### 4. Pickle para Persistência de Modelo
- `pickle.load()` em `api/views.py` carrega arquivo binário sem sanitização
- **Risco**: Execução de código arbitrário se `modelo.pkl` for comprometido
- **Alternativa**: `joblib` ou formatos seguros como ONNX / JSON (skops)

### 5. Sem Testes Automatizados
- Zero cobertura de testes (ver `TESTING.md`)
- Alterações no serializer/view podem quebrar a API silenciosamente

### 6. Lógica de Negócio nas Views
- Não há camada de serviço (`services.py`, `use_cases`)
- Views acumulam validação, filtragem, serialização e previsão ML

## Médio

### 7. Tratamento de Erros Genérico
- Blocos `except Exception` capturam tudo e retornam "Erro interno no servidor"
- Dificulta debugging em produção
- Sugestão: logar traceback, retornar mensagens específicas para 4xx

### 8. Duplicação de Código
- `formatarValor`, `getCategoriaLabel`, `getCategoriaIcon` duplicados entre `App.vue` e `DashboardCharts.vue`
- Mapeamento de categorias (7 choices) existe em 4 lugares diferentes

### 9. Paginação Manual
- `queryset[:limite]` com clamp para 100
- Não usa `PageNumberPagination` do DRF
- Sem metadados de paginação (next, previous, total count real)

### 10. Estado Centralizado em App.vue
- Sem Pinia/Vuex; estado global em componente root
- Dificulta escalabilidade se novas páginas/features forem adicionadas

### 11. Gráficos Não Usam vue-chartjs
- `vue-chartjs` está no `package.json` mas `DashboardCharts.vue` importa `chart.js` diretamente
- Gerencia `destroy()` e lifecycle manualmente (potencial para memory leaks)

## Baixo

### 12. HelloWorld.vue Não Utilizado
- Componente boilerplate do scaffold Vite ainda presente

### 13. Variáveis CSS Não Integradas ao App.vue
- `style.css` define `:root` com tema claro/escuro
- `App.vue` usa cores hardcoded (ex: `#0f172a`, `#22c55e`)
- Tema não é coerente com as variáveis globais

### 14. Sem Cache
- Cada carregamento faz query full no SQLite
- Não há Redis, memcached ou cache de queryset

### 15. SQLite em Produção
- README menciona deploy com Gunicorn, mas banco continua SQLite
- Não há instruções para PostgreSQL/MySQL

## Próximos Passos Documentados (README)

- [ ] JWT Authentication
- [ ] Gráficos e dashboard (parcialmente já implementado)
- [ ] Cache com Redis
- [ ] Melhorar modelo de IA com dados reais
- [ ] Exportação de dados
- [ ] PWA
- [ ] Testes automatizados
