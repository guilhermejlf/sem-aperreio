<template>
  <div class="extrato-page">
    <!-- Loading -->
    <div v-if="loading" class="extrato-loading">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      <p>Carregando extrato...</p>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- FILTERS -->
      <div class="extrato-filters">
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
            <option value="gastos">Gastos</option>
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

        <button class="btn-clear" @click="limparFiltros">
          <i class="pi pi-filter-slash"></i>
          Limpar
        </button>
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
            <span class="summary-label">Gastos</span>
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

      <!-- EXPORT BUTTONS -->
      <div class="extrato-toolbar">
        <button class="btn-export" @click="exportar('csv')" :disabled="itens.length === 0">
          <i class="pi pi-file-export"></i>
          Exportar CSV
        </button>
        <button class="btn-export btn-export--xlsx" @click="exportar('xlsx')" :disabled="itens.length === 0">
          <i class="pi pi-file-excel"></i>
          Exportar Excel
        </button>
        <span v-if="itens.length > 0" class="extrato-count">
          {{ itens.length }} registro{{ itens.length === 1 ? '' : 's' }}
        </span>
      </div>

      <!-- EMPTY STATE -->
      <div v-if="itens.length === 0" class="empty-state">
        <i class="pi pi-list empty-icon"></i>
        <h3>Nenhum registro encontrado</h3>
        <p>Adicione receitas ou gastos para ver o extrato financeiro.</p>
      </div>

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

    <Toast position="top-right" />
  </div>
</template>

<script>
import { fetchExtrato, downloadExport } from '../config/api.js'
import Toast from 'primevue/toast'

export default {
  name: 'ExtratoView',
  components: { Toast },

  data() {
    const hoje = new Date()
    return {
      loading: false,
      itens: [],
      resumo: null,
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
        this.$toast.add({
          severity: 'error',
          summary: 'Erro',
          detail: 'Não foi possível carregar o extrato.',
          life: 3000
        })
      } finally {
        this.loading = false
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
        this.$toast.add({
          severity: 'success',
          summary: 'Exportado',
          detail: `Arquivo ${formato.toUpperCase()} baixado com sucesso!`,
          life: 3000
        })
      } catch (error) {
        console.error('Erro ao exportar:', error)
        this.$toast.add({
          severity: 'error',
          summary: 'Erro',
          detail: 'Erro ao exportar o extrato.',
          life: 3000
        })
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
  max-width: 900px;
  margin: 0 auto;
  padding: 16px;
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

/* Filters */
.extrato-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-group label {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 8px 12px;
  color: #e5e7eb;
  font-size: 14px;
  min-width: 120px;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: #22c55e;
}

.filter-select option {
  background: #1e293b;
  color: #e5e7eb;
}

.btn-clear {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 8px 14px;
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  height: fit-content;
}

.btn-clear:hover {
  border-color: #ef4444;
  color: #ef4444;
}

/* Summary */
.extrato-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
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
  border-left: 3px solid #22c55e;
}

.summary-gastos {
  border-left: 3px solid #ef4444;
}

.summary-saldo {
  border-left: 3px solid #3b82f6;
}

.saldo-positivo .summary-value {
  color: #22c55e;
}

.saldo-negativo .summary-value {
  color: #ef4444;
}

/* Toolbar */
.extrato-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.btn-export {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 8px 14px;
  color: #e5e7eb;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.btn-export:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: #3b82f6;
}

.btn-export:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-export--xlsx:hover:not(:disabled) {
  border-color: #22c55e;
}

.extrato-count {
  font-size: 13px;
  color: #64748b;
  margin-left: auto;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  color: #e5e7eb;
  font-size: 1.2rem;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* List */
.extrato-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.extrato-item {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 14px 16px;
  transition: all 0.2s ease;
}

.extrato-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.extrato-item__icon {
  font-size: 22px;
  flex-shrink: 0;
  width: 36px;
  text-align: center;
}

.extrato-item__info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.extrato-item__title {
  font-size: 15px;
  font-weight: 500;
  color: #e5e7eb;
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
  background: rgba(255, 255, 255, 0.08);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.item-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.status-pago {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-pendente {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.extrato-item__value {
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
  white-space: nowrap;
}

.valor-receita {
  color: #22c55e;
}

.valor-gasto {
  color: #ef4444;
}

/* Responsive */
@media (max-width: 768px) {
  .extrato-filters {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .btn-clear {
    width: 100%;
    justify-content: center;
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

  .extrato-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-export {
    width: 100%;
    justify-content: center;
  }

  .extrato-count {
    margin-left: 0;
    text-align: center;
  }
}
</style>
