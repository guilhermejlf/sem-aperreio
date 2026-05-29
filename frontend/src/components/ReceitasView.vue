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

        <!-- Paginação -->
        <div v-if="pagination.pages > 1" class="pagination-bar">
          <button
            :disabled="!pagination.previous"
            @click="goToPageReceitas(pagination.page - 1)"
            class="btn-pagination"
          >
            <i class="pi pi-chevron-left"></i>
          </button>
          <span class="pagination-info">Página {{ pagination.page }} de {{ pagination.pages }}</span>
          <button
            :disabled="!pagination.next"
            @click="goToPageReceitas(pagination.page + 1)"
            class="btn-pagination"
          >
            <i class="pi pi-chevron-right"></i>
          </button>
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

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import BaseCard from './BaseCard.vue'
import RevenueModal from './modals/RevenueModal.vue'
import ConfirmModal from './modals/ConfirmModal.vue'
import EmptyState from './EmptyState.vue'
import { fetchReceitas, deleteReceita } from '../config/api.js'
import { toastMessages, toastTitles } from '../utils/toastMessages.js'
import { toastStore } from '../stores/toast.store.js'

const props = defineProps({
  initialEditData: {
    type: Object,
    default: null
  }
})

const receitas = ref([])
const loading = ref(false)
const showModal = ref(false)
const revenueEditingData = ref(null)
const pagination = ref({
  page: 1,
  pages: 1,
  pageSize: 20,
  total: 0,
  next: null,
  previous: null,
})
const confirmVisible = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmDanger = ref(false)
const confirmAcceptLabel = ref('Confirmar')
const confirmRejectLabel = ref('Cancelar')
let confirmOnAccept = null

watch(() => props.initialEditData, (newVal) => {
  if (newVal) {
    revenueEditingData.value = { id: null, ...newVal }
    showModal.value = true
  }
})

const totalReceitas = computed(() => receitas.value.reduce((soma, r) => soma + parseFloat(r.valor || 0), 0))

onMounted(() => {
  carregarReceitas()
})

async function carregarReceitas(page = 1) {
  try {
    loading.value = true
    const res = await fetchReceitas(page, pagination.value.pageSize)
    receitas.value = res.receitas || []
    pagination.value.page = res.page || 1
    pagination.value.pages = res.pages || 1
    pagination.value.total = res.total || 0
    pagination.value.next = res.next || null
    pagination.value.previous = res.previous || null
  } catch (err) {
    console.error('Erro ao carregar receitas:', err)
  } finally {
    loading.value = false
  }
}

function goToPageReceitas(page) {
  if (page >= 1 && page <= pagination.value.pages) {
    carregarReceitas(page)
  }
}

function abrirModal() {
  revenueEditingData.value = null
  showModal.value = true
}

function abrirEdicao(receita) {
  revenueEditingData.value = receita
  showModal.value = true
}

function fecharModal() {
  showModal.value = false
  revenueEditingData.value = null
}

async function onRevenueSaved() {
  await carregarReceitas()
}

function podeEditarReceita(receita) {
  return true
}

function excluirReceita(id) {
  confirmTitle.value = 'Excluir Receita'
  confirmMessage.value = 'Tem certeza que deseja excluir esta receita?'
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Sim, excluir'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = async () => {
    try {
      await deleteReceita(id)
      receitas.value = receitas.value.filter(r => r.id !== id)
      toastStore.success(toastMessages.revenue.deleted, { title: toastTitles.success })
    } catch (err) {
      if (err.message?.includes('404') || err.message?.includes('não encontrada')) {
        receitas.value = receitas.value.filter(r => r.id !== id)
        toastStore.success(toastMessages.revenue.deleted, { title: toastTitles.success })
      } else {
        console.error('Erro ao excluir receita:', err)
        toastStore.error(toastMessages.generic.actionError, { title: toastTitles.error })
      }
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

function formatarValor(valor) {
  return parseFloat(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function formatarData(dataStr) {
  if (!dataStr) return ''
  const data = new Date(dataStr + 'T00:00:00')
  return data.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
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
