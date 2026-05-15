<template>
  <div class="budget-view">
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
    <BudgetEditModal
      v-if="modalVisible"
      :visible="modalVisible"
      :meta="metaSelecionada"
      :modo-criar="true"
      :categoria-pre-selecionada="null"
      :categorias-usadas="categoriasUsadas"
      @save="onSaveMeta"
      @cancel="modalVisible = false"
    />
  </div>
</template>

<script>
import { fetchMetas, createMeta, updateMeta, deleteMeta } from '../config/api.js'
import BudgetEditModal from './BudgetEditModal.vue'
import EmptyState from './EmptyState.vue'

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
  'contas': '�',
  'compras': '�️',
  'outros': '📦'
}

export default {
  name: 'BudgetView',
  components: { BudgetEditModal, EmptyState },
  data() {
    const hoje = new Date()
    return {
      periodo: {
        mes: hoje.getMonth() + 1,
        ano: hoje.getFullYear()
      },
      metasData: { geral: null, por_categoria: [] },
      loading: false,
      modalVisible: false,
      metaSelecionada: null,
      metaToDelete: null
    }
  },
  computed: {
    mesesNomes() {
      return MES_NOMES
    },
    anosDisponiveis() {
      const atual = new Date().getFullYear()
      return [atual, atual - 1, atual - 2]
    },
    mesNome() {
      return MES_NOMES[this.periodo.mes - 1]
    },
    temMetas() {
      return this.metaGeral || this.metasPorCategoria.length > 0
    },
    metaGeral() {
      return this.metasData && this.metasData.geral ? this.metasData.geral : null
    },
    metasPorCategoria() {
      const lista = (this.metasData && this.metasData.por_categoria) ? this.metasData.por_categoria : []
      return [...lista].sort((a, b) => (b.percentual_usado || 0) - (a.percentual_usado || 0))
    },
    categoriasUsadas() {
      const cats = (this.metasData && this.metasData.por_categoria) ? this.metasData.por_categoria : []
      return cats.map(m => m.categoria)
    }
  },
  mounted() {
    this.carregarMetas()
  },
  watch: {
    periodo: {
      deep: true,
      handler() {
        this.carregarMetas()
      }
    }
  },
  methods: {
    async carregarMetas() {
      try {
        this.loading = true
        const data = await fetchMetas(this.periodo.mes, this.periodo.ano)
        const metas = data.metas || { geral: null, por_categoria: [] }
        // Normaliza: se API retornar lista plana, converte para objeto
        if (Array.isArray(metas)) {
          this.metasData = {
            geral: metas.find(m => m.categoria === null) || null,
            por_categoria: metas.filter(m => m.categoria !== null)
          }
        } else {
          this.metasData = metas
        }
      } catch (error) {
        console.error('Erro ao carregar metas:', error)
        this.metasData = { geral: null, por_categoria: [] }
      } finally {
        this.loading = false
      }
    },

    pctClamped(pct) {
      return Math.min(pct || 0, 100)
    },

    formatarValor(valor) {
      return parseFloat(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    categoriaEmoji(categoria) {
      return CATEGORIA_EMOJIS[categoria] || '🏷️'
    },

    formatarCategoriaDisplay(categoria, categoriaNome) {
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
    },

    abrirEditar(meta) {
      this.metaSelecionada = { ...meta, modo: 'editar' }
      this.modalVisible = true
    },

    abrirCriarMetaGeral() {
      this.metaSelecionada = {
        categoria: null,
        categoria_nome: 'Geral',
        valor_meta: '',
        mes: this.periodo.mes,
        ano: this.periodo.ano,
        modo: 'criar'
      }
      this.modalVisible = true
    },

    abrirCriarCategoria() {
      this.metaSelecionada = {
        categoria: '',
        categoria_nome: '',
        valor_meta: '',
        mes: this.periodo.mes,
        ano: this.periodo.ano,
        modo: 'criar_categoria'
      }
      this.modalVisible = true
    },

    onDeleteMeta(meta) {
      const nome = this.formatarCategoriaDisplay(meta.categoria, meta.categoria_nome) || 'Meta Geral'
      this.$confirm.require({
        message: `Deseja deletar a meta "${nome}" para ${MES_NOMES[this.periodo.mes - 1]} ${this.periodo.ano}?`,
        header: 'Deletar Meta',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Deletar',
        rejectLabel: 'Cancelar',
        acceptClass: 'p-button-danger',
        accept: async () => {
          try {
            if (meta && meta.id) {
              await deleteMeta(meta.id)
              this.carregarMetas()
              this.$toast.success('Meta deletada!')
            }
          } catch (error) {
            console.error('Erro ao deletar meta:', error)
            this.$toast.error(error.message || 'Erro ao deletar meta')
          }
        }
      })
    },
    async onSaveMeta(meta) {
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
        this.modalVisible = false
        this.carregarMetas()
        this.$toast.success('Meta salva!')
      } catch (error) {
        console.error('Erro ao salvar meta:', error)
        this.$toast.error(error.message || 'Erro ao salvar meta')
      }
    }
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
