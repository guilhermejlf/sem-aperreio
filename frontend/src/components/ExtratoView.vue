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
        @export="exportar"
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
      <StatementEmptyState v-if="itens.length === 0" />

      <!-- Timeline -->
      <StatementTimeline
        v-else
        :itens="itens"
        :categorias="categorias"
      />

      <!-- Paginação -->
      <div v-if="pagination.pages > 1" class="pagination-bar">
        <button
          :disabled="!pagination.previous"
          @click="goToPage(pagination.page - 1, carregarExtrato)"
          class="btn-pagination"
        >
          <i class="pi pi-chevron-left"></i>
        </button>
        <span class="pagination-info">Página {{ pagination.page }} de {{ pagination.pages }}</span>
        <button
          :disabled="!pagination.next"
          @click="goToPage(pagination.page + 1, carregarExtrato)"
          class="btn-pagination"
        >
          <i class="pi pi-chevron-right"></i>
        </button>
      </div>
    </template>

    <!-- Export FAB -->
    <ExportFAB
      v-if="itens.length > 0"
      @export="exportar"
    />

    <div class="page-spacer" v-if="itens.length > 0"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StatementTimeline from './statement/StatementTimeline.vue'
import StatementSummary from './statement/StatementSummary.vue'
import StatementFilters from './statement/StatementFilters.vue'
import StatementEmptyState from './statement/StatementEmptyState.vue'
import StatementSkeleton from './statement/StatementSkeleton.vue'
import ExportFAB from './ExportFAB.vue'
import { fetchExtrato, downloadExport } from '../config/api.js'
import { toastMessages, toastTitles } from '../utils/toastMessages.js'
import { formatarValor } from '../utils/formatCurrency.js'
import { usePagination } from '../composables/usePagination.js'
import { toastStore } from '../stores/toast.store.js'

const emit = defineEmits(['add-transaction'])

const { pagination, goToPage, applyPagination } = usePagination()

const loading = ref(false)
const itens = ref([])
const resumo = ref(null)
const filters = ref({
  mes: '',
  ano: '',
  categoria: '',
  tipo: '',
  pago: ''
})
const categorias = ref([
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
])
const mesesLabels = ref(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])

async function carregarExtrato(page = 1) {
  loading.value = true
  try {
    const params = {}
    if (filters.value.mes) params.mes = filters.value.mes
    if (filters.value.ano) params.ano = filters.value.ano
    if (filters.value.categoria) params.categoria = filters.value.categoria
    if (filters.value.tipo) params.tipo = filters.value.tipo
    if (filters.value.pago !== '') params.pago = filters.value.pago

    const data = await fetchExtrato(params, page, pagination.value.pageSize)
    itens.value = data.itens || []
    resumo.value = data.resumo || null
    applyPagination(data)
  } catch (err) {
    console.error('Erro ao carregar extrato:', err)
    toastStore.error(toastMessages.export.loadError, { title: toastTitles.error })
  } finally {
    loading.value = false
  }
}

async function exportar(formato) {
  try {
    const params = {}
    if (filters.value.mes) params.mes = filters.value.mes
    if (filters.value.ano) params.ano = filters.value.ano
    if (filters.value.categoria) params.categoria = filters.value.categoria
    if (filters.value.tipo) params.tipo = filters.value.tipo
    if (filters.value.pago !== '') params.pago = filters.value.pago

    await downloadExport(formato, params)
    toastStore.success(toastMessages.export.downloaded(formato), { title: toastTitles.success })
  } catch (err) {
    console.error('Erro ao exportar:', err)
    toastStore.error(toastMessages.export.exportError, { title: toastTitles.error })
  }
}

onMounted(() => {
  carregarExtrato()
})
</script>

<style scoped>
.extrato-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}

.page-spacer {
  height: 64px;
}

/* Summary Strip */
.summary-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  padding: 10px 16px;
  margin-bottom: 20px;
  font-size: 12px;
  line-height: 1.5;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

@media (max-width: 768px) {
  .extrato-page {
    padding: 20px 20px max(20px, env(safe-area-inset-bottom)) 20px;
  }

  .summary-strip {
    font-size: 11px;
    padding: 8px 12px;
    margin-bottom: 16px;
    line-height: 1.5;
  }

  .page-spacer {
    display: none;
  }
}
</style>
