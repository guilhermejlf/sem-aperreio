# Convenções de Código

## Backend (Python / Django)

### Estilo e Formatação

- **Idioma**: Código misto português/inglês. Classes/modelos em português (`Gasto`), métodos em português (`prever_gasto`), comentários em português.
- **Docstrings**: Ausentes; comentários em bloco (`# --- TÍTULO ---`) separam seções
- **Emojis em comentários**: Usados como marcadores (`👈`, `⚠️`)
- **Imports**: Agrupados por origem (stdlib, Django, DRF, locais)

### Padrões de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Modelos | PascalCase, PT | `Gasto` |
| Serializers | PascalCase + Suffixo | `GastoSerializer` |
| Views | snake_case, PT | `prever_gasto`, `gasto_detail` |
| Variáveis | snake_case, PT | `categoria`, `data_inicio` |
| Constantes | snake_case, PT | `CATEGORIAS_CHOICES` |
| Globals (lazy) | snake_case leading `_` | `_modelo_ia` |

### Organização de Views

- FBVs (Function-Based Views) com `@api_view` ao invés de CBVs/ViewSets
- Tratamento de erro envolvido em blocos `try/except` grandes
- Respostas padronizadas: `{"erro": "..."}` ou `{"mensagem": "..."}`

### Validação

- Dupla validação: `Model.clean()` + `Serializer.validate_<field>()`
- `Model.save()` chama `self.full_clean()` explicitamente
- Valores de dinheiro validados em serializer: `> 0` e `< 999999.99`

---

## Frontend (Vue 3 / JavaScript)

### Estilo e Formatação

- **Vue API**: Options API (não Composition API / `<script setup>`)
- **Idioma**: Componentes e métodos em português (`adicionarGasto`, `carregarGastos`)
- **Template**: HTML com diretivas Vue (`v-if`, `v-for`, `v-model`, `@click`)

### Padrões de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Componentes | PascalCase, PT | `DashboardCharts.vue` |
| Props | camelCase | `gastos` |
| Data | camelCase, PT | `gastosDoMes`, `totalMes` |
| Métodos | camelCase, PT | `formatarData`, `getCategoriaLabel` |
| Computed | camelCase, PT | `dadosPorCategoria` |
| Classes CSS | kebab-case | `.gastos-container`, `.stat-badge` |

### Estilização

- CSS puro (não SASS/LESS)
- Estilos `scoped` em componentes `.vue`
- CSS global em `style.css` com variáveis CSS e `prefers-color-scheme: dark`
- Unidades: px predominante, rem usado em poucos lugares
- Gradientes e `backdrop-filter: blur()` frequentes no visual

### Organização de Componente Vue

```
<template> ... </template>
<script>
  import ...
  export default {
    components: { ... },
    data() { ... },
    computed: { ... },
    mounted() { ... },
    watch: { ... },
    methods: { ... }
  }
</script>
<style> ... </style>
```

---

## Geral

- **Mensagens de erro**: Sempre em português, amigáveis ao usuário final
- **Moeda**: BRL (Real brasileiro), locale `pt-BR`
- **Datas**: ISO 8601 no backend (`YYYY-MM-DD`), `pt-BR` no frontend
- **Emojis**: Usados em labels de categoria e ícones de UI (`🍔`, `🚗`, etc.)
- **Sem ESLint / Prettier / Black / Flake8 configurados**
