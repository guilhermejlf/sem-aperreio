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

<script>
import BaseCard from './BaseCard.vue'
import RevenueModal from './modals/RevenueModal.vue'
import ConfirmModal from './modals/ConfirmModal.vue'
import EmptyState from './EmptyState.vue'
import { fetchReceitas, deleteReceita } from '../config/api.js'

export default {
  name: 'ReceitasView',
  components: {
    BaseCard,
    RevenueModal,
    ConfirmModal,
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
      revenueEditingData: null,
      confirmVisible: false,
      confirmTitle: '',
      confirmMessage: '',
      confirmDanger: false,
      confirmAcceptLabel: 'Confirmar',
      confirmRejectLabel: 'Cancelar',
      confirmOnAccept: null
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
      this.confirmTitle = 'Excluir Receita'
      this.confirmMessage = 'Tem certeza que deseja excluir esta receita?'
      this.confirmDanger = true
      this.confirmAcceptLabel = 'Sim, excluir'
      this.confirmRejectLabel = 'Cancelar'
      this.confirmOnAccept = async () => {
        try {
          await deleteReceita(id)
          this.receitas = this.receitas.filter(r => r.id !== id)
          this.$toast.success('Receita excluída!')
        } catch (error) {
          console.error('Erro ao excluir receita:', error)
          this.$toast.error('Erro ao excluir receita: ' + error.message)
        }
      }
      this.confirmVisible = true
    },

    async onConfirmAccept() {
      this.confirmVisible = false
      if (this.confirmOnAccept) {
        await this.confirmOnAccept()
        this.confirmOnAccept = null
      }
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


@media (max-width: 768px) {
  .receitas-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

}
</style>
