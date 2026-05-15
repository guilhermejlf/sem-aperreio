<template>
  <div class="receitas-page">
    <!-- Loading -->
    <div v-if="loading" class="receitas-loading">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      <p>Carregando receitas...</p>
    </div>

    <!-- Conteúdo -->
    <template v-else>
      <!-- Lista -->
      <EmptyState
        v-if="receitas.length === 0"
        title="Bora adicionar tua primeira receita?"
        description="Registra teus ganhos pra ter o controle completo."
        icon="pi pi-wallet"
        action-label="Adicionar receita"
        @action="abrirModal"
      />

      <div v-else>
        <div class="receitas-toolbar">
          <div class="mobile-primary-action">
            <button @click="abrirModal" class="btn-primary btn-sm">
              Nova Receita
            </button>
          </div>
        </div>
        <div class="receitas-list">
          <BaseCard
          v-for="r in receitas"
          :key="r.id"
          :title="r.descricao || 'Receita'"
          :subtitle="formatarData(r.data)"
          :value="formatarValor(r.valor)"
          valueColor="#60A637"
        >
          <template #meta>
            <small v-if="r.user_name" class="receita-user">@{{ r.user_name }}</small>
          </template>
          <template #actions>
            <template v-if="podeEditarReceita(r)">
              <button @click="abrirEdicao(r)" class="edit-btn" title="Editar ">
                <i class="pi pi-pencil"></i>
              </button>
              <button @click="excluirReceita(r.id)" class="delete-btn" title="Excluir">
                <i class="pi pi-trash"></i>
              </button>
            </template>
          </template>
        </BaseCard>
      </div>
      </div>
    </template>


    <RevenueModal
      :visible="showModal"
      :editing-data="revenueEditingData"
      @close="fecharModal"
      @saved="onRevenueSaved"
    />
  </div>
</template>

<script>
import BaseCard from './BaseCard.vue'
import RevenueModal from './modals/RevenueModal.vue'
import EmptyState from './EmptyState.vue'
import { fetchReceitas, deleteReceita } from '../config/api.js'

export default {
  name: 'ReceitasView',
  components: {
    BaseCard,
    RevenueModal,
    EmptyState,
  },
  props: {
    initialEditData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      receitas: [],
      loading: false,
      showModal: false,
      revenueEditingData: null
    }
  },
  watch: {
    initialEditData: {
      handler(newVal) {
        if (newVal) {
          this.revenueEditingData = { id: null, ...newVal }
          this.showModal = true
        }
      }
    }
  },
  computed: {
    totalReceitas() {
      return this.receitas.reduce((soma, r) => soma + parseFloat(r.valor || 0), 0)
    }
  },
  mounted() {
    this.carregarReceitas()
  },
  methods: {
    async carregarReceitas() {
      try {
        this.loading = true
        const res = await fetchReceitas()
        this.receitas = res.receitas || []
      } catch (error) {
        console.error('Erro ao carregar receitas:', error)
      } finally {
        this.loading = false
      }
    },
    abrirModal() {
      this.revenueEditingData = null
      this.showModal = true
    },
    abrirEdicao(receita) {
      this.revenueEditingData = receita
      this.showModal = true
    },
    fecharModal() {
      this.showModal = false
      this.revenueEditingData = null
    },
    async onRevenueSaved() {
      await this.carregarReceitas()
    },
    podeEditarReceita(receita) {
      // Simples: todas as receitas são editáveis pelo usuário logado
      // (receitas não têm family filter complexo como gastos)
      return true
    },
    excluirReceita(id) {
      this.$confirm.require({
        message: 'Tem certeza que deseja excluir esta receita?',
        header: 'Excluir Receita',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Sim, excluir',
        rejectLabel: 'Cancelar',
        acceptClass: 'p-button-danger',
        accept: async () => {
          try {
            await deleteReceita(id)
            this.receitas = this.receitas.filter(r => r.id !== id)
            this.$toast.success('Receita excluída!')
          } catch (error) {
            console.error('Erro ao excluir receita:', error)
            this.$toast.error('Erro ao excluir receita: ' + error.message)
          }
        }
      })
    },
    formatarValor(valor) {
      return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },
    formatarData(dataStr) {
      if (!dataStr) return ''
      const data = new Date(dataStr + 'T00:00:00')
      return data.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.receitas-page {
  max-width: 1200px;
  margin: 0 auto;
}

.receitas-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
  color: #9ca3af;
}

.receitas-toolbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.receitas-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.receita-user {
  color: #64748b;
  font-size: 11px;
  display: block;
}

.edit-btn,
.delete-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* Modal form styles - Design System v2.0 */
.receita-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: rgba(248, 250, 252, 0.72);
  margin-bottom: 10px;
}

.form-input {
  width: 100%;
  height: 56px;
  padding: 0 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 16px;
  font-weight: 500;
  color: #F8FAFC;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input::placeholder {
  color: rgba(248, 250, 252, 0.35);
}

.form-input:focus {
  outline: none;
  border-color: #60A637;
  box-shadow: 0 0 0 4px rgba(96, 166, 55, 0.12);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 16px;
  color: rgba(248, 250, 252, 0.45);
  font-weight: 500;
  font-size: 15px;
  pointer-events: none;
  z-index: 1;
}

.input-field {
  padding-left: 44px;
}

.btn-secondary {
  height: 48px;
  padding: 0 24px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(248, 250, 252, 0.82);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.06);
}

.btn-primary {
  height: 48px;
  padding: 0 24px;
  border-radius: 16px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 18px rgba(96, 166, 55, 0.12);
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.05);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.4);
}

@media (max-width: 768px) {
  .receitas-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

}
</style>
