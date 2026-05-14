<template>
  <div class="extrato-page">
    <!-- Loading -->
    <div v-if="loading" class="extrato-loading">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      <p>Carregando extrato...</p>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- TOOLBAR -->
      <div class="toolbar">
        <div class="toolbar-filters">
          <div class="filter-group">
            <label>Mês</label>
            <select v-model="filters.mes" class="filter-select" @change="carregarExtrato">
              <option value="">Todos</option>
              <option v-for="m in 12" :key="m" :value="m">
                {{ mesesLabels[m - 1] }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Ano</label>
            <select v-model="filters.ano" class="filter-select" @change="carregarExtrato">
              <option value="">Todos</option>
              <option v-for="a in anosDisponiveis" :key="a" :value="a">
                {{ a }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Categoria</label>
            <select v-model="filters.categoria" class="filter-select" @change="carregarExtrato">
              <option value="">Todas</option>
              <option v-for="cat in categorias" :key="cat.value" :value="cat.value">
                {{ cat.label }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Tipo</label>
            <select v-model="filters.tipo" class="filter-select" @change="carregarExtrato">
              <option value="">Todos</option>
              <option value="receitas">Receitas</option>
              <option value="gastos">Despesas</option>
            </select>
          </div>

          <div v-if="filters.tipo !== 'receitas'" class="filter-group">
            <label>Status</label>
            <select v-model="filters.pago" class="filter-select" @change="carregarExtrato">
              <option value="">Todos</option>
              <option value="true">Já pagos</option>
              <option value="false">Ainda a pagar</option>
            </select>
          </div>

        </div>

        <div class="toolbar-actions">
          <button class="btn-clear" @click="limparFiltros" title="Limpar filtros">
            <i class="pi pi-filter-slash"></i>
          </button>

          <div class="export-dropdown-wrapper" v-if="itens.length > 0">
            <button
              class="btn-export-toggle"
              @click="toggleExportDropdown"
              ref="exportBtn"
              title="Exportar"
            >
              <i class="pi pi-download"></i>
              <i class="pi pi-chevron-down" :class="{ rotated: showExportDropdown }"></i>
            </button>
            <div v-if="showExportDropdown" class="export-dropdown" ref="exportDropdown">
              <button class="export-option" @click="exportar('csv'); showExportDropdown = false">
                <i class="pi pi-file-export"></i>
                Exportar CSV
              </button>
              <button class="export-option" @click="exportar('xlsx'); showExportDropdown = false">
                <i class="pi pi-file-excel"></i>
                Exportar Excel
              </button>
              <button class="export-option" @click="exportar('pdf'); showExportDropdown = false">
                <i class="pi pi-file-pdf"></i>
                Exportar PDF
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SUMMARY CARDS -->
      <div class="extrato-summary" v-if="resumo">
        <div class="summary-card summary-receitas">
          <span class="summary-icon">💰</span>
          <div class="summary-info">
            <span class="summary-label">Receitas</span>
            <span class="summary-value">{{ formatarValor(resumo.total_receitas) }}</span>
          </div>
        </div>
        <div class="summary-card summary-gastos">
          <span class="summary-icon">💳</span>
          <div class="summary-info">
            <span class="summary-label">Despesas</span>
            <span class="summary-value">{{ formatarValor(resumo.total_gastos) }}</span>
          </div>
        </div>
        <div class="summary-card summary-saldo" :class="saldoClasse">
          <span class="summary-icon">⚖️</span>
          <div class="summary-info">
            <span class="summary-label">Saldo</span>
            <span class="summary-value">{{ formatarValor(resumo.saldo) }}</span>
          </div>
        </div>
      </div>

      <!-- LIST HEADER -->
      <div class="extrato-list-header">
        <div class="list-header-info">
          <h2 class="list-header-title">Extrato Financeiro</h2>
          <span class="list-header-count">
            {{ itens.length }} registro{{ itens.length === 1 ? '' : 's' }} encontrado{{ itens.length === 1 ? '' : 's' }}
          </span>
        </div>
      </div>

      <EmptyState
        v-if="itens.length === 0"
        title="Tá vazio por aqui 😄"
        description="Adicione receitas ou despesas pra ver o extrato financeiro."
        icon="pi pi-list"
      />

      <!-- LIST -->
      <div v-else class="extrato-list">
        <div
          v-for="item in itens"
          :key="`${item.tipo}-${item.id}`"
          class="extrato-item"
        >
          <div class="extrato-item__icon">
            {{ item.tipo === 'receita' ? '💰' : getCategoriaIcon(item.categoria) }}
          </div>
          <div class="extrato-item__info">
            <div class="extrato-item__title">
              {{ item.descricao || getCategoriaLabel(item.categoria) || 'Receita' }}
            </div>
            <div class="extrato-item__subtitle">
              <span v-if="item.categoria" class="item-categoria">
                {{ getCategoriaLabel(item.categoria) }}
              </span>
              <span class="item-data">{{ formatarData(item.data) }}</span>
              <span v-if="item.tipo === 'gasto'" class="item-status" :class="item.pago ? 'status-pago' : 'status-pendente'">
                {{ item.pago ? 'Pago' : 'Pendente' }}
              </span>
            </div>
          </div>
          <div class="extrato-item__value" :class="item.tipo === 'receita' ? 'valor-receita' : 'valor-gasto'">
            {{ item.tipo === 'receita' ? '+' : '-' }} {{ formatarValor(item.valor) }}
          </div>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
import EmptyState from './EmptyState.vue'
import { fetchExtrato, downloadExport } from '../config/api.js'
export default {
  components: { EmptyState },
  name: 'ExtratoView',

  data() {
    const hoje = new Date()
    return {
      loading: false,
      itens: [],
      resumo: null,
      showExportDropdown: false,
      filters: {
        mes: hoje.getMonth() + 1,
        ano: hoje.getFullYear(),
        categoria: '',
        tipo: '',
        pago: ''
      },
      categorias: [
        { value: 'moradia', label: 'Moradia' },
        { value: 'mercado', label: 'Mercado' },
        { value: 'restaurantes', label: 'Restaurantes / Delivery' },
        { value: 'transporte', label: 'Transporte' },
        { value: 'saude', label: 'Saúde' },
        { value: 'educacao', label: 'Educação' },
        { value: 'lazer', label: 'Lazer' },
        { value: 'contas', label: 'Contas e serviços' },
        { value: 'compras', label: 'Compras' },
        { value: 'outros', label: 'Outros' }
      ],
      mesesLabels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    }
  },

  computed: {
    anosDisponiveis() {
      const atual = new Date().getFullYear()
      return [atual, atual - 1, atual - 2]
    },

    saldoClasse() {
      if (!this.resumo) return ''
      return this.resumo.saldo >= 0 ? 'saldo-positivo' : 'saldo-negativo'
    }
  },

  mounted() {
    this.carregarExtrato()
    document.addEventListener('click', this.closeExportDropdown)
  },

  beforeUnmount() {
    document.removeEventListener('click', this.closeExportDropdown)
  },

  methods: {
    async carregarExtrato() {
      this.loading = true
      try {
        const params = {}
        if (this.filters.mes) params.mes = this.filters.mes
        if (this.filters.ano) params.ano = this.filters.ano
        if (this.filters.categoria) params.categoria = this.filters.categoria
        if (this.filters.tipo) params.tipo = this.filters.tipo
        if (this.filters.pago !== '') params.pago = this.filters.pago

        const data = await fetchExtrato(params)
        this.itens = data.itens || []
        this.resumo = data.resumo || null
      } catch (error) {
        console.error('Erro ao carregar extrato:', error)
        this.$toast.error('Não foi possível carregar o extrato.', { title: 'Erro' })
      } finally {
        this.loading = false
      }
    },

    toggleExportDropdown() {
      this.showExportDropdown = !this.showExportDropdown
    },

    closeExportDropdown(e) {
      if (
        this.$refs.exportDropdown &&
        !this.$refs.exportDropdown.contains(e.target) &&
        !this.$refs.exportBtn.contains(e.target)
      ) {
        this.showExportDropdown = false
      }
    },

    limparFiltros() {
      this.filters = {
        mes: '',
        ano: '',
        categoria: '',
        tipo: '',
        pago: ''
      }
      this.carregarExtrato()
    },

    async exportar(formato) {
      try {
        const params = {}
        if (this.filters.mes) params.mes = this.filters.mes
        if (this.filters.ano) params.ano = this.filters.ano
        if (this.filters.categoria) params.categoria = this.filters.categoria
        if (this.filters.tipo) params.tipo = this.filters.tipo
        if (this.filters.pago !== '') params.pago = this.filters.pago

        await downloadExport(formato, params)
        this.$toast.success(`Arquivo ${formato.toUpperCase()} baixado com sucesso!`, { title: 'Exportado' })
      } catch (error) {
        console.error('Erro ao exportar:', error)
        this.$toast.error('Erro ao exportar o extrato.', { title: 'Erro' })
      }
    },

    formatarValor(valor) {
      return parseFloat(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    formatarData(dataStr) {
      if (!dataStr) return ''
      try {
        const data = new Date(dataStr + 'T12:00:00')
        if (isNaN(data.getTime())) return dataStr
        return data.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: 'short',
          year: 'numeric'
        })
      } catch {
        return dataStr
      }
    },

    getCategoriaLabel(categoriaValue) {
      if (!categoriaValue) return ''
      const categoria = this.categorias.find(c => c.value === categoriaValue)
      return categoria ? categoria.label : categoriaValue
    },

    getCategoriaIcon(categoria) {
      const icons = {
        moradia: '🏠',
        mercado: '🛒',
        restaurantes: '🍔',
        transporte: '🚗',
        saude: '🏥',
        educacao: '📚',
        lazer: '🎮',
        contas: '💡',
        compras: '🛍️',
        outros: '📦'
      }
      return icons[categoria] || '💳'
    }
  }
}
</script>

<style scoped>
.extrato-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.extrato-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #94a3b8;
  gap: 16px;
}

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 8px;
  flex-wrap: nowrap;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.toolbar-filters {
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  align-items: flex-end;
  flex: 1;
  min-width: 0;
  overflow: visible;
}

.toolbar-actions {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  flex-shrink: 0;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1 1 auto;
  min-width: 0;
}

.filter-group label {
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.filter-select {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 7px 6px;
  color: #cbd5e1;
  font-size: 12px;
  min-width: 80px;
  width: 100%;
  cursor: pointer;
  transition: border-color 0.15s ease;
  height: 34px;
  box-sizing: border-box;
}

.filter-select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.15);
}

.filter-select option {
  background: #1e293b;
  color: #cbd5e1;
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
  padding: 4px;
  height: 34px;
  width: 34px;
  box-sizing: border-box;
  line-height: 1;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.btn-clear:hover {
  color: #ef4444;
}

/* Summary */
.extrato-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}

.summary-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-icon {
  font-size: 24px;
}

.summary-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.summary-label {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 18px;
  font-weight: 600;
  color: #e5e7eb;
}

.summary-receitas {
  border-left: 3px solid #60A637;
}

.summary-gastos {
  border-left: 3px solid #ef4444;
}

.summary-saldo {
  border-left: 3px solid #3b82f6;
}

.saldo-positivo .summary-value {
  color: #60A637;
}

.saldo-negativo .summary-value {
  color: #ef4444;
}

/* List Header */
.extrato-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.list-header-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.list-header-title {
  font-size: 15px;
  font-weight: 600;
  color: #e5e7eb;
  margin: 0;
  letter-spacing: -0.2px;
}

.list-header-count {
  font-size: 12px;
  color: #64748b;
  opacity: 0.7;
}

/* Export Dropdown */
.export-dropdown-wrapper {
  position: relative;
}

.btn-export-toggle {
  background: none;
  border: none;
  color: #64748b;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px;
  height: 34px;
  width: 34px;
  box-sizing: border-box;
  line-height: 1;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.btn-export-toggle:hover {
  color: #3b82f6;
}

.btn-export-toggle .pi-chevron-down {
  font-size: 10px;
  transition: transform 0.2s ease;
}

.btn-export-toggle .pi-chevron-down.rotated {
  transform: rotate(180deg);
}

.export-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 6px;
  min-width: 170px;
  z-index: 100;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.export-option {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 10px;
  border-radius: 6px;
  background: transparent;
  border: none;
  color: #cbd5e1;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s ease;
  text-align: left;
}

.export-option:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #e5e7eb;
}

/* List */
.extrato-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.extrato-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 10px;
  padding: 12px 14px;
  transition: all 0.2s ease;
}

.extrato-item:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.08);
}

.extrato-item__icon {
  font-size: 20px;
  flex-shrink: 0;
  width: 32px;
  text-align: center;
  line-height: 1;
}

.extrato-item__info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.extrato-item__title {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.extrato-item__subtitle {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 12px;
  color: #64748b;
}

.item-categoria {
  background: rgba(255, 255, 255, 0.05);
  padding: 1px 7px;
  border-radius: 4px;
  font-size: 11px;
  color: #94a3b8;
}

.item-status {
  padding: 1px 7px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.status-pago {
  background: rgba(96, 166, 55, 0.1);
  color: #60A637;
}

.status-pendente {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.extrato-item__value {
  font-size: 15px;
  font-weight: 600;
  flex-shrink: 0;
  white-space: nowrap;
}

.valor-receita {
  color: #60A637;
}

.valor-gasto {
  color: #ef4444;
}

/* Responsive */
@media (max-width: 768px) {
  .toolbar {
    flex-wrap: wrap;
    gap: 10px;
  }

  .toolbar-filters {
    flex-wrap: wrap;
    width: 100%;
  }

  .filter-group {
    flex: 1 1 45%;
    min-width: 120px;
  }

  .toolbar-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .filter-select {
    width: 100%;
    height: auto;
  }

  .btn-clear {
    flex: 1;
    justify-content: center;
    height: 38px;
  }

  .btn-export-toggle {
    flex: 1;
    justify-content: center;
    height: 38px;
  }

  .export-dropdown-wrapper {
    width: 100%;
  }

  .export-dropdown {
    right: auto;
    left: 0;
    width: 100%;
  }

  .extrato-summary {
    grid-template-columns: 1fr;
  }

  .extrato-item {
    gap: 10px;
    padding: 12px;
  }

  .extrato-item__icon {
    font-size: 20px;
    width: 30px;
  }

  .extrato-item__value {
    font-size: 14px;
  }

  .extrato-list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
}
</style>
