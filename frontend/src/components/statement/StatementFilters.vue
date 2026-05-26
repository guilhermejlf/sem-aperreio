<template>
  <div class="statement-filters">
    <!-- Desktop: inline filters -->
    <div class="filters-desktop">
      <div class="filters-row">
        <div class="filter-chip" v-if="activeFilters.length > 0">
          <span v-for="f in activeFilters" :key="f.key" class="chip">
            {{ f.label }}
            <i class="pi pi-times" @click="clearFilter(f.key)"></i>
          </span>
        </div>
        <span v-else class="filters-placeholder">
          Extrato • {{ currentPeriod }}
        </span>
      </div>

      <div class="filters-inline">
        <div class="filter-group">
          <label>Mês</label>
          <select v-model="filters.mes" @change="onChange">
            <option value="">Todos</option>
            <option v-for="m in 12" :key="m" :value="m">{{ mesesLabels[m-1] }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Ano</label>
          <select v-model="filters.ano" @change="onChange">
            <option value="">Todos</option>
            <option v-for="a in anosDisponiveis" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Categoria</label>
          <select v-model="filters.categoria" @change="onChange">
            <option value="">Todas</option>
            <option v-for="cat in categorias" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Tipo</label>
          <select v-model="filters.tipo" @change="onChange">
            <option value="">Todos</option>
            <option value="receitas">Receitas</option>
            <option value="gastos">Despesas</option>
          </select>
        </div>
        <div class="filter-group" v-if="filters.tipo !== 'receitas'">
          <label>Status</label>
          <select v-model="filters.pago" @change="onChange">
            <option value="">Todos</option>
            <option value="true">Pagos</option>
            <option value="false">Pendentes</option>
          </select>
        </div>
        <button class="btn-clear" @click="limparFiltros" title="Limpar">
          <i class="pi pi-filter-slash"></i>
        </button>
      </div>
    </div>

    <!-- Mobile: compact header + bottom sheet -->
    <div class="filters-mobile">
      <div class="filters-mobile-header">
        <span class="filters-period">Extrato • {{ currentPeriod }}</span>
        <button class="btn-filters" @click="showSheet = true">
          <i class="pi pi-filter"></i>
          Filtros
          <span v-if="activeCount > 0" class="filters-badge">{{ activeCount }}</span>
        </button>
      </div>
      <div v-if="activeFilters.length > 0" class="filters-mobile-chips">
        <span v-for="f in activeFilters" :key="f.key" class="chip">
          {{ f.label }}
          <i class="pi pi-times" @click="clearFilter(f.key)"></i>
        </span>
      </div>
    </div>

    <!-- Mobile Bottom Sheet -->
    <Teleport to="body">
      <Transition name="sheet">
        <div v-if="showSheet" class="bottom-sheet-overlay" @click.self="showSheet = false">
          <div class="bottom-sheet">
            <div class="bottom-sheet__header">
              <h3>Filtros</h3>
              <button class="btn-close" @click="showSheet = false">
                <i class="pi pi-times"></i>
              </button>
            </div>
            <div class="bottom-sheet__content">
              <div class="sheet-field">
                <label>Mês</label>
                <select v-model="filters.mes">
                  <option value="">Todos</option>
                  <option v-for="m in 12" :key="m" :value="m">{{ mesesLabels[m-1] }}</option>
                </select>
              </div>
              <div class="sheet-field">
                <label>Ano</label>
                <select v-model="filters.ano">
                  <option value="">Todos</option>
                  <option v-for="a in anosDisponiveis" :key="a" :value="a">{{ a }}</option>
                </select>
              </div>
              <div class="sheet-field">
                <label>Categoria</label>
                <select v-model="filters.categoria">
                  <option value="">Todas</option>
                  <option v-for="cat in categorias" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
                </select>
              </div>
              <div class="sheet-field">
                <label>Tipo</label>
                <select v-model="filters.tipo">
                  <option value="">Todos</option>
                  <option value="receitas">Receitas</option>
                  <option value="gastos">Despesas</option>
                </select>
              </div>
              <div class="sheet-field" v-if="filters.tipo !== 'receitas'">
                <label>Status</label>
                <select v-model="filters.pago">
                  <option value="">Todos</option>
                  <option value="true">Pagos</option>
                  <option value="false">Pendentes</option>
                </select>
              </div>
            </div>
            <div class="bottom-sheet__footer">
              <button class="btn-secondary" @click="limparFiltros">Limpar</button>
              <button class="btn-primary" @click="applyFilters">Aplicar</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
export default {
  name: 'StatementFilters',

  props: {
    modelValue: {
      type: Object,
      required: true
    },
    categorias: {
      type: Array,
      default: () => []
    },
    mesesLabels: {
      type: Array,
      default: () => ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    }
  },

  emits: ['update:modelValue', 'change'],

  data() {
    return {
      showSheet: false,
      filters: { ...this.modelValue }
    }
  },

  computed: {
    anosDisponiveis() {
      const atual = new Date().getFullYear()
      return [atual, atual - 1, atual - 2]
    },

    activeFilters() {
      const list = []
      if (this.modelValue.mes) list.push({ key: 'mes', label: this.mesesLabels[this.modelValue.mes - 1] })
      if (this.modelValue.ano) list.push({ key: 'ano', label: String(this.modelValue.ano) })
      if (this.modelValue.categoria) {
        const cat = this.categorias.find(c => c.value === this.modelValue.categoria)
        list.push({ key: 'categoria', label: cat?.label || this.modelValue.categoria })
      }
      if (this.modelValue.tipo) list.push({ key: 'tipo', label: this.modelValue.tipo === 'receitas' ? 'Receitas' : 'Despesas' })
      if (this.modelValue.pago !== '') list.push({ key: 'pago', label: this.modelValue.pago === 'true' ? 'Pagos' : 'Pendentes' })
      return list
    },

    activeCount() {
      return this.activeFilters.length
    },

    currentPeriod() {
      const mes = this.modelValue.mes
      const ano = this.modelValue.ano
      if (mes && ano) return `${this.mesesLabels[mes - 1]} ${ano}`
      if (mes) return this.mesesLabels[mes - 1]
      if (ano) return String(ano)
      return 'Todos'
    }
  },

  watch: {
    modelValue: {
      handler(val) {
        this.filters = { ...val }
      },
      deep: true
    }
  },

  methods: {
    onChange() {
      this.$emit('update:modelValue', { ...this.filters })
      this.$emit('change')
    },

    applyFilters() {
      this.$emit('update:modelValue', { ...this.filters })
      this.$emit('change')
      this.showSheet = false
    },

    limparFiltros() {
      this.filters = { mes: '', ano: '', categoria: '', tipo: '', pago: '' }
      this.$emit('update:modelValue', { ...this.filters })
      this.$emit('change')
    },

    clearFilter(key) {
      this.filters[key] = key === 'pago' ? '' : ''
      this.onChange()
    }
  }
}
</script>

<style scoped>
/* Desktop */
.filters-desktop {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.filters-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filters-placeholder {
  font-size: 15px;
  font-weight: 600;
  color: #e2e8f0;
}

.filter-chip {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 12px;
  color: #cbd5e1;
  cursor: default;
}

.chip i {
  cursor: pointer;
  font-size: 10px;
  opacity: 0.6;
  transition: opacity 0.15s;
}

.chip i:hover {
  opacity: 1;
  color: #ef4444;
}

.filters-inline {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.filter-group label {
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.filter-group select {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 7px 10px;
  color: #cbd5e1;
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.15s ease;
  height: 36px;
  box-sizing: border-box;
}

.filter-group select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.15);
}

.btn-clear {
  background: none;
  border: none;
  color: #64748b;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  height: 36px;
  width: 36px;
  border-radius: 8px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-clear:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.08);
}

/* Mobile */
.filters-mobile {
  display: none;
}

.filters-mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.filters-period {
  font-size: 15px;
  font-weight: 600;
  color: #e2e8f0;
}

.btn-filters {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-filters:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filters-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  background: #3b82f6;
  color: #fff;
  font-size: 10px;
  font-weight: 600;
  padding: 0 5px;
}

.filters-mobile-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

/* Bottom Sheet */
.bottom-sheet-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bottom-sheet {
  width: 100%;
  max-width: 480px;
  max-height: 85vh;
  background: #0f172a;
  border-radius: 20px 20px 0 0;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: none;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
}

.bottom-sheet__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.bottom-sheet__header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
}

.btn-close {
  background: none;
  border: none;
  color: #64748b;
  font-size: 16px;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-sheet__content {
  padding: 16px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sheet-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sheet-field label {
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.sheet-field select {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 12px;
  color: #cbd5e1;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.15s ease;
  height: 44px;
  box-sizing: border-box;
}

.sheet-field select:focus {
  outline: none;
  border-color: #3b82f6;
}

.bottom-sheet__footer {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.bottom-sheet__footer button {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.08);
}

.btn-primary {
  background: #3b82f6;
  color: #fff;
}

.btn-primary:hover {
  background: #2563eb;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

/* Transitions */
.sheet-enter-active,
.sheet-leave-active {
  transition: opacity 0.3s ease;
}

.sheet-enter-from,
.sheet-leave-to {
  opacity: 0;
}

.sheet-enter-active .bottom-sheet,
.sheet-leave-active .bottom-sheet {
  transition: transform 0.3s ease;
}

.sheet-enter-from .bottom-sheet,
.sheet-leave-to .bottom-sheet {
  transform: translateY(100%);
}

/* Responsive toggle */
@media (max-width: 768px) {
  .filters-desktop {
    display: none;
  }

  .filters-mobile {
    display: flex;
    flex-direction: column;
    margin-bottom: 16px;
  }
}

@media (min-width: 769px) {
  .filters-mobile {
    display: none !important;
  }
}
</style>
