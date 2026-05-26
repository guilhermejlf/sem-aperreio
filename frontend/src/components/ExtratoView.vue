<template>
  <div class="extrato-page">
    <!-- Loading -->
    <StatementSkeleton v-if="loading" />

    <!-- Content -->
    <template v-else>
      <!-- Filters -->
      <StatementFilters
        v-model="filters"
        :categorias="categorias"
        :meses-labels="mesesLabels"
        @change="carregarExtrato"
      />

      <!-- Summary -->
      <StatementSummary
        v-if="resumo"
        :resumo="resumo"
      />

      <!-- Summary Strip -->
      <div class="summary-strip" v-if="itens.length > 0">
        <span>
          {{ itens.length }} lançamento{{ itens.length === 1 ? '' : 's' }}
        </span>
        <span v-if="resumo?.total_gastos > 0">
          • {{ formatarValor(resumo.total_gastos) }} em despesas
        </span>
        <span v-if="resumo?.total_receitas > 0">
          • {{ formatarValor(resumo.total_receitas) }} em receitas
        </span>
      </div>

      <!-- Empty -->
      <StatementEmptyState
        v-if="itens.length === 0"
        @action="$emit('add-transaction')"
      />

      <!-- Timeline -->
      <StatementTimeline
        v-else
        :itens="itens"
        :categorias="categorias"
      />
    </template>

    <!-- Export FAB -->
    <div v-if="itens.length > 0" class="export-fab-wrapper">
      <button
        class="export-fab"
        @click="toggleExportDropdown"
        ref="exportBtn"
        title="Exportar"
      >
        <i class="pi pi-download"></i>
      </button>
      <Transition name="fade">
        <div v-if="showExportDropdown" class="export-menu" ref="exportDropdown">
          <button @click="exportar('csv'); showExportDropdown = false">
            <i class="pi pi-file-export"></i> CSV
          </button>
          <button @click="exportar('xlsx'); showExportDropdown = false">
            <i class="pi pi-file-excel"></i> Excel
          </button>
          <button @click="exportar('pdf'); showExportDropdown = false">
            <i class="pi pi-file-pdf"></i> PDF
          </button>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import StatementTimeline from './statement/StatementTimeline.vue'
import StatementSummary from './statement/StatementSummary.vue'
import StatementFilters from './statement/StatementFilters.vue'
import StatementEmptyState from './statement/StatementEmptyState.vue'
import StatementSkeleton from './statement/StatementSkeleton.vue'
import { fetchExtrato, downloadExport } from '../config/api.js'
import { toastMessages, toastTitles } from '../utils/toastMessages.js'

export default {
  name: 'ExtratoView',

  components: {
    StatementTimeline,
    StatementSummary,
    StatementFilters,
    StatementEmptyState,
    StatementSkeleton
  },

  emits: ['add-transaction'],

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
        this.$toast.error(toastMessages.export.loadError, { title: toastTitles.error })
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

    async exportar(formato) {
      try {
        const params = {}
        if (this.filters.mes) params.mes = this.filters.mes
        if (this.filters.ano) params.ano = this.filters.ano
        if (this.filters.categoria) params.categoria = this.filters.categoria
        if (this.filters.tipo) params.tipo = this.filters.tipo
        if (this.filters.pago !== '') params.pago = this.filters.pago

        await downloadExport(formato, params)
        this.$toast.success(toastMessages.export.downloaded(formato), { title: toastTitles.success })
      } catch (error) {
        console.error('Erro ao exportar:', error)
        this.$toast.error(toastMessages.export.exportError, { title: toastTitles.error })
      }
    },

    formatarValor(valor) {
      return parseFloat(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    }
  }
}
</script>

<style scoped>
.extrato-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}

/* Summary Strip */
.summary-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 12px;
  padding: 10px 16px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #64748b;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

/* Export FAB */
.export-fab-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}

.export-fab {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #3b82f6;
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.35);
  transition: all 0.2s ease;
}

.export-fab:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45);
}

.export-fab:active {
  transform: translateY(0);
}

.export-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 6px;
  min-width: 160px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.export-menu button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #cbd5e1;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
}

.export-menu button:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #e5e7eb;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

@media (max-width: 768px) {
  .extrato-page {
    padding: 16px;
  }

  .summary-strip {
    font-size: 12px;
    padding: 8px 12px;
    margin-bottom: 16px;
  }

  .export-fab-wrapper {
    bottom: 80px;
    right: 16px;
  }

  .export-fab {
    width: 48px;
    height: 48px;
    font-size: 16px;
  }
}
</style>
