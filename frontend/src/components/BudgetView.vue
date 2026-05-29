<template>
  <div class="budget-view">
    <ContextualTooltip
      v-if="showBudgetTooltip"
      text="Defina limites de gastos e receba alertas antes de ultrapassar o orçamento."
      @dismiss="dismissBudgetTooltip"
    />
    <!-- Seletor de Período -->
    <div class="period-selector">
      <select v-model="periodo.mes" class="period-select">
        <option v-for="(nome, idx) in mesesNomes" :key="idx" :value="idx + 1">{{ nome }}</option>
      </select>
      <select v-model="periodo.ano" class="period-select">
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="dashboard-loading">
      <i class="pi pi-spin pi-spinner"></i>
      <p>Carregando metas...</p>
    </div>

    <EmptyState
      v-else-if="!temMetas"
      title="Nenhuma meta definida"
      :description="periodo ? `Definir metas ajuda a evitar aperreio 👀` : 'Defina metas pra acompanhar tuas despesas.'"
      icon="pi pi-bullseye"
      action-label="Definir meta"
      @action="abrirCriarMetaGeral"
    />

    <!-- Conteúdo -->
    <template v-else>
      <!-- Bloco Meta Geral -->
      <div class="section-header">
        <div class="block-title">Orçamento Geral</div>
      </div>
      <div v-if="!metaGeral" class="nova-meta-section">
        <div class="mobile-primary-action">
          <button @click="abrirCriarMetaGeral" class="btn-primary">
            Definir Meta Geral
          </button>
        </div>
      </div>
      <div v-else class="meta-geral-card" :class="metaGeral.status">
        <div class="meta-card__body">
          <div class="meta-card__left">
            <div class="meta-card__info">
              <div class="meta-card__header">
                <span class="meta-card__icon"><i class="pi pi-bullseye"></i></span>
                <h4 class="meta-card__title">Meta Geral — {{ mesNome }} {{ periodo.ano }}</h4>
              </div>
              <p class="meta-card__subtitle">
                <span :class="metaGeral.status">{{ formatarValor(metaGeral.gasto_realizado) }}</span>
                <span class="meta-sep"> / </span>
                <span>{{ formatarValor(metaGeral.valor_meta) }}</span>
              </p>
            </div>
            <div class="meta-bar-row">
              <div class="meta-bar-container">
                <div class="meta-bar-fill" :class="metaGeral.status" :style="{width: pctClamped(metaGeral.percentual_usado) + '%'}"></div>
              </div>
              <div class="meta-card__value" :class="metaGeral.status">{{ metaGeral.percentual_usado }}%</div>
            </div>
          </div>
          <div class="meta-card__actions">
            <button class="btn-edit" @click="abrirEditar(metaGeral)" title="Editar meta geral">
              <i class="pi pi-pencil"></i>
            </button>
            <button class="btn-edit delete-btn" @click="onDeleteMeta(metaGeral)" title="Deletar meta geral">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Bloco Categorias -->
      <div class="section-header">
        <div class="block-title">Metas por Categoria</div>
        <div class="mobile-primary-action">
          <button @click="abrirCriarCategoria" class="btn-primary btn-sm">
            Adicionar Meta
          </button>
        </div>
      </div>
      <div class="categorias-grid">
        <div
          v-for="meta in metasPorCategoria"
          :key="meta.id"
          class="categoria-card"
          :class="meta.status"
        >
          <div class="meta-card__body">
            <div class="meta-card__left">
              <div class="meta-card__info">
                <div class="meta-card__header">
                  <h4 class="meta-card__title">{{ categoriaEmoji(meta.categoria) }} {{ formatarCategoriaDisplay(meta.categoria, meta.categoria_nome) }}</h4>
                </div>
                <p class="meta-card__subtitle">
                  <span :class="meta.status">{{ formatarValor(meta.gasto_realizado) }}</span>
                  <span class="categoria-sep"> / </span>
                  <span>{{ formatarValor(meta.valor_meta) }}</span>
                </p>
              </div>
              <div class="meta-bar-row">
                <div class="categoria-bar-container">
                  <div class="categoria-bar-fill" :class="meta.status" :style="{width: pctClamped(meta.percentual_usado) + '%'}"></div>
                </div>
                <div class="meta-card__value" :class="meta.status">{{ meta.percentual_usado }}%</div>
              </div>
            </div>
            <div class="meta-card__actions">
              <button class="btn-edit" @click="abrirEditar(meta)" title="Editar meta">
                <i class="pi pi-pencil"></i>
              </button>
              <button class="btn-edit delete-btn" @click="onDeleteMeta(meta)" title="Deletar meta de categoria">
                <i class="pi pi-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Modal -->
    <GoalModal
      v-if="modalVisible"
      :visible="modalVisible"
      :meta="metaSelecionada"
      :categorias-usadas="categoriasUsadas"
      @save="onSaveMeta"
      @cancel="modalVisible = false"
    />

    <ConfirmModal
      :visible="confirmVisible"
      :title="confirmTitle"
      :message="confirmMessage"
      :danger="confirmDanger"
      :accept-label="confirmAcceptLabel"
      :reject-label="confirmRejectLabel"
      @accept="onConfirmAccept"
      @reject="confirmVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { fetchMetas, createMeta, updateMeta, deleteMeta } from '../config/api.js'
import GoalModal from './modals/GoalModal.vue'
import ConfirmModal from './modals/ConfirmModal.vue'
import EmptyState from './EmptyState.vue'
import { toastMessages, toastTitles } from '../utils/toastMessages.js'
import { toastStore } from '../stores/toast.store.js'
import ContextualTooltip from './onboarding/ContextualTooltip.vue'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'

const MES_NOMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

const CATEGORIA_EMOJIS = {
  'moradia': '🏠',
  'mercado': '🛒',
  'restaurantes': '🍔',
  'transporte': '🚗',
  'saude': '💊',
  'educacao': '📚',
  'lazer': '🎮',
  'contas': '💡',
  'compras': '🛍️',
  'outros': '📦'
}

const hoje = new Date()
const periodo = ref({
  mes: hoje.getMonth() + 1,
  ano: hoje.getFullYear()
})
const metasData = ref({ geral: null, por_categoria: [] })
const loading = ref(false)
const modalVisible = ref(false)
const metaSelecionada = ref(null)
const confirmVisible = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmDanger = ref(false)
const confirmAcceptLabel = ref('Confirmar')
const confirmRejectLabel = ref('Cancelar')
let confirmOnAccept = null

const mesesNomes = computed(() => MES_NOMES)
const anosDisponiveis = computed(() => {
  const atual = new Date().getFullYear()
  return [atual, atual - 1, atual - 2]
})
const mesNome = computed(() => MES_NOMES[periodo.value.mes - 1])
const temMetas = computed(() => metaGeral.value || metasPorCategoria.value.length > 0)
const metaGeral = computed(() => metasData.value && metasData.value.geral ? metasData.value.geral : null)
const metasPorCategoria = computed(() => {
  const lista = (metasData.value && metasData.value.por_categoria) ? metasData.value.por_categoria : []
  return [...lista].sort((a, b) => (b.percentual_usado || 0) - (a.percentual_usado || 0))
})
const categoriasUsadas = computed(() => {
  const cats = (metasData.value && metasData.value.por_categoria) ? metasData.value.por_categoria : []
  return cats.map(m => m.categoria)
})

onMounted(() => {
  carregarMetas()
})

watch(periodo, () => {
  carregarMetas()
}, { deep: true })

async function carregarMetas() {
  try {
    loading.value = true
    const data = await fetchMetas(periodo.value.mes, periodo.value.ano)
    const metas = data.metas || { geral: null, por_categoria: [] }
    if (Array.isArray(metas)) {
      metasData.value = {
        geral: metas.find(m => m.categoria === null) || null,
        por_categoria: metas.filter(m => m.categoria !== null)
      }
    } else {
      metasData.value = metas
    }
  } catch (err) {
    console.error('Erro ao carregar metas:', err)
    metasData.value = { geral: null, por_categoria: [] }
  } finally {
    loading.value = false
  }
}

function pctClamped(pct) {
  return Math.min(pct || 0, 100)
}

function formatarValor(valor) {
  return parseFloat(valor || 0).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function categoriaEmoji(categoria) {
  return CATEGORIA_EMOJIS[categoria] || '🏷️'
}

function formatarCategoriaDisplay(categoria, categoriaNome) {
  if (categoriaNome && categoriaNome !== categoria) return categoriaNome
  const map = {
    alimentacao: 'Alimentação',
    vestuario: 'Vestuário',
    servicos: 'Serviços',
    moradia: 'Moradia',
    mercado: 'Mercado',
    restaurantes: 'Restaurantes / Delivery',
    transporte: 'Transporte',
    saude: 'Saúde',
    educacao: 'Educação',
    lazer: 'Lazer',
    contas: 'Contas e serviços',
    compras: 'Compras',
    outros: 'Outros'
  }
  return map[categoria] || (categoria ? categoria.charAt(0).toUpperCase() + categoria.slice(1).replace(/_/g, ' ') : 'Geral')
}

function abrirEditar(meta) {
  metaSelecionada.value = { ...meta, modo: 'editar' }
  modalVisible.value = true
}

function abrirCriarMetaGeral() {
  metaSelecionada.value = {
    categoria: null,
    categoria_nome: 'Geral',
    valor_meta: '',
    mes: periodo.value.mes,
    ano: periodo.value.ano,
    modo: 'criar'
  }
  modalVisible.value = true
}

function abrirCriarCategoria() {
  metaSelecionada.value = {
    categoria: '',
    categoria_nome: '',
    valor_meta: '',
    mes: periodo.value.mes,
    ano: periodo.value.ano,
    modo: 'criar_categoria'
  }
  modalVisible.value = true
}

function onDeleteMeta(meta) {
  const nome = formatarCategoriaDisplay(meta.categoria, meta.categoria_nome) || 'Meta Geral'
  confirmTitle.value = 'Excluir Meta'
  confirmMessage.value = `Deseja excluir a meta "${nome}" para ${MES_NOMES[periodo.value.mes - 1]} ${periodo.value.ano}?`
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Excluir'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = async () => {
    try {
      if (meta && meta.id) {
        await deleteMeta(meta.id)
        carregarMetas()
        toastStore.success(toastMessages.goals.deleted, { title: toastTitles.success })
      }
    } catch (err) {
      console.error('Erro ao excluir meta:', err)
      toastStore.error(toastMessages.goals.deleteError, { title: toastTitles.error })
    }
  }
  confirmVisible.value = true
}

async function onConfirmAccept() {
  confirmVisible.value = false
  if (confirmOnAccept) {
    await confirmOnAccept()
    confirmOnAccept = null
  }
}

async function onSaveMeta(meta) {
  try {
    if (meta.id) {
      await updateMeta(meta.id, { valor_meta: meta.valor_meta })
    } else {
      await createMeta({
        categoria: meta.categoria,
        mes: meta.mes,
        ano: meta.ano,
        valor_meta: meta.valor_meta
      })
    }
    modalVisible.value = false
    carregarMetas()
    toastStore.success(toastMessages.goals.updated, { title: toastTitles.success })
  } catch (err) {
    console.error('Erro ao salvar meta:', err)
    toastStore.error(toastMessages.goals.saveError, { title: toastTitles.error })
  }
}
</script>

<style scoped>
.budget-view {
  max-width: 1200px;
  margin: 0 auto;
}

/* Section Header (toolbar padrão como gastos/receitas) */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.section-header .block-title {
  margin: 0;
}

/* Period Selector */
.period-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  justify-content: center;
}

.period-select {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px 16px;
  color: #e5e7eb;
  font-size: 14px;
  cursor: pointer;
  min-width: 140px;
}

.period-select:focus {
  outline: none;
  border-color: #60A637;
}

/* Meta Geral */
.meta-geral-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  margin-bottom: 16px;
  transition: all 0.2s ease;
}

.meta-geral-card:hover {
  background: rgba(255, 255, 255, 0.05);
}

.meta-card__body {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex: 1;
  min-width: 0;
}

.meta-card__left {
  flex: 1;
  min-width: 0;
}

.meta-card__info {
  flex: 1;
  min-width: 0;
}

.meta-card__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  flex-wrap: wrap;
}

.meta-card__icon {
  font-size: 18px;
  line-height: 1;
}

.meta-card__title {
  margin: 0;
  color: #e5e7eb;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.3;
}

.meta-card__subtitle {
  margin: 0 0 4px 0;
  color: #94a3b8;
  font-size: 13px;
  line-height: 1.4;
}

.meta-card__subtitle .ok,
.meta-card__value.ok { color: #10b981; }
.meta-card__subtitle .warning,
.meta-card__value.warning { color: #f59e0b; }
.meta-card__subtitle .danger,
.meta-card__value.danger { color: #ef4444; }
.meta-card__subtitle .critical,
.meta-card__value.critical { color: #dc2626; }

.meta-bar-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.meta-bar-row .meta-bar-container,
.meta-bar-row .categoria-bar-container {
  flex: 1;
  margin-top: 0;
}

.meta-bar-row .meta-card__value {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.2;
  white-space: nowrap;
  flex-shrink: 0;
}

.meta-card__actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-left: 16px;
  padding-left: 12px;
  border-left: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
}

.btn-edit {
  background: none;
  border: none;
  color: #64748b;
  font-size: 16px;
  cursor: pointer;
  transition: color 0.2s ease;
  padding: 4px;
  line-height: 1;
  min-width: 40px;
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-edit:hover {
  color: #3b82f6;
}

.delete-btn:hover {
  color: #ef4444;
}

.meta-sep {
  color: #64748b;
  font-weight: 400;
}

.meta-bar-container {
  height: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  margin-top: 8px;
  margin-bottom: 0;
}

.meta-bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.6s ease-out;
}

.meta-bar-fill.ok { background: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.3); }
.meta-bar-fill.warning { background: #f59e0b; box-shadow: 0 0 8px rgba(245, 158, 11, 0.3); }
.meta-bar-fill.danger { background: #ef4444; box-shadow: 0 0 8px rgba(239, 68, 68, 0.3); }
.meta-bar-fill.critical { background: #dc2626; box-shadow: 0 0 12px rgba(220, 38, 38, 0.5); animation: pulse-critical 2s ease-in-out infinite; }

@keyframes pulse-critical {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Categorias Grid */
.categorias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.categoria-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.2s ease;
}

.categoria-card:hover {
  background: rgba(255, 255, 255, 0.05);
}

.categoria-sep {
  color: #64748b;
  font-weight: 400;
}

.categoria-bar-container {
  height: 8px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 6px;
  margin-bottom: 0;
}

.categoria-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease-out;
}

.categoria-bar-fill.ok { background: #10b981; }
.categoria-bar-fill.warning { background: #f59e0b; }
.categoria-bar-fill.danger { background: #ef4444; }
.categoria-bar-fill.critical { background: #dc2626; animation: pulse-critical 2s ease-in-out infinite; }

/* Nova Meta Card */
.nova-meta {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-left: 4px dashed rgba(255, 255, 255, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
}

.nova-meta:hover {
  border-color: #60A637;
  background: rgba(96, 166, 55, 0.05);
}

.nova-meta-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #94a3b8;
  font-weight: 500;
}

.nova-meta-content i {
  font-size: 1.5rem;
}

/* Criar Meta Geral */
/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #60A637, #4C8932);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 12px 24px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 14px rgba(96, 166, 55, 0.18);
}

.btn-primary:hover {
  filter: brightness(1.1);
}

.btn-primary.btn-sm {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 10px;
}

.btn-primary.btn-lg {
  padding: 15px 30px;
  font-size: 1rem;
  border-radius: 14px;
}

/* Titles */
.block-title {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
  margin: 24px 0 12px 0;
  padding-left: 4px;
}

/* Loading */
.dashboard-loading {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.dashboard-loading i {
  font-size: 2rem;
  margin-bottom: 12px;
  display: block;
}

/* Responsive */
@media (max-width: 768px) {
  .budget-view {
    padding: 12px;
  }

  .meta-geral-card {
    padding: 20px;
  }

  .categorias-grid {
    grid-template-columns: 1fr;
  }

  .period-selector {
    flex-direction: column;
    align-items: stretch;
  }

  .period-select {
    width: 100%;
  }
}
</style>
