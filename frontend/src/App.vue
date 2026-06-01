<template>
  <ErrorBoundary>
    <div class="page">
    <ToastProvider />
    <OfflineFallback />
    <InstallPrompt />

    <!-- AUTH VIEWS -->
    <template v-if="currentPath === '/reset-password'">
      <PasswordResetView />
    </template>
    <template v-else-if="currentPath === '/verify-email'">
      <VerifyEmailView />
    </template>
    <template v-else-if="!isAuth">
      <AuthView @authenticated="handleLoginSuccess" />
    </template>

    <!-- WELCOME MODAL -->
    <WelcomeModal
      v-if="showWelcomeModal"
      @start="startOnboarding"
      @explore="dismissWelcome"
    />

    <!-- APP CONTENT -->
    <template v-else>
    <!-- HEADER -->
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <img :src="logo" class="logo" />
        </div>

        <nav class="nav-menu">
          <button
            :class="['nav-item', { active: activeTab === 'dashboard' }]"
            @click="activeTab = 'dashboard'"
          >
            <i class="pi pi-home"></i>
            <span>Painel</span>
          </button>
          <button
            :class="['nav-item', { active: activeTab === 'extrato' }]"
            @click="activeTab = 'extrato'"
          >
            <i class="pi pi-list"></i>
            <span>Extrato</span>
          </button>
          <button
            :class="['nav-item', { active: activeTab === 'gastos' }]"
            @click="activeTab = 'gastos'"
          >
            <i class="pi pi-arrow-up-right"></i>
            <span>Despesas</span>
          </button>
          <button
            :class="['nav-item', { active: activeTab === 'receitas' }]"
            @click="activeTab = 'receitas'"
          >
            <i class="pi pi-chart-line"></i>
            <span>Receitas</span>
          </button>
          <button
            :class="['nav-item', { active: activeTab === 'metas' }]"
            @click="activeTab = 'metas'"
          >
            <i class="pi pi-bullseye"></i>
            <span>Metas</span>
          </button>
          <button
            :class="['nav-item', { active: activeTab === 'grupo' }]"
            @click="activeTab = 'grupo'"
          >
            <i class="pi pi-users"></i>
            <span>Grupo</span>
          </button>
        </nav>

        <div class="header-actions">
          <div v-if="currentUser" class="user-menu-wrapper">
            <button class="user-name" @click="showUserMenu = !showUserMenu">
              <span class="user-avatar">{{ (currentUser.first_name || currentUser.username || '?').charAt(0).toUpperCase() }}</span>
              <span class="user-label">{{ currentUser.first_name || currentUser.username }}</span>
              <i class="pi pi-chevron-down" :class="{ rotated: showUserMenu }"></i>
            </button>
            <div v-if="showUserMenu" class="user-dropdown">
              <div class="dropdown-header">
                <span class="user-avatar dropdown-avatar">{{ (currentUser.first_name || currentUser.username || '?').charAt(0).toUpperCase() }}</span>
                <div class="dropdown-info">
                  <span class="dropdown-name">{{ currentUser.first_name || currentUser.username }}</span>
                  <span class="dropdown-email">{{ currentUser.email || '' }}</span>
                </div>
              </div>
              <div v-if="currentFamily" class="dropdown-group-info">
                <span class="group-label">Grupo</span>
                <span class="group-name">{{ currentFamily.name }}</span>
              </div>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item" @click="navigateTo('perfil')">
                <i class="pi pi-user"></i>
                <span>Meu Perfil</span>
              </button>
              <button class="dropdown-item" @click="navigateTo('configuracoes')">
                <i class="pi pi-cog"></i>
                <span>Configurações</span>
              </button>
              <div class="dropdown-divider"></div>
              <button @click="handleLogout" class="dropdown-item danger">
                <i class="pi pi-sign-out"></i>
                <span>Sair</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- LOADING -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="pi pi-spin pi-spinner"></i>
        <p>Carregando...</p>
      </div>
    </div>

    <!-- ERROR MESSAGE -->
    <div v-if="error" class="error-message">
      <i class="pi pi-exclamation-triangle"></i>
      <span>{{ error }}</span>
      <button @click="error = null" class="close-error">×</button>
    </div>

    <!-- MAIN CONTENT -->
    <main class="main-content">
      
      <!-- DASHBOARD TAB -->
      <div v-if="activeTab === 'dashboard'" class="tab-content">
        <div class="gastos-container">
          <OnboardingChecklist
            v-if="showOnboardingChecklist && !onboardingStatus.completed"
            :status="onboardingStatus"
            @dismiss="dismissChecklist"
            @navigate="handleNavigateFromChecklist"
          />
          <DashboardCharts />
        </div>
      </div>

      <!-- EXTRATO TAB -->
      <div v-if="activeTab === 'extrato'" class="tab-content">
        <div class="gastos-container">
          <ExtratoView />
        </div>
      </div>

      <!-- METAS TAB -->
      <div v-if="activeTab === 'metas'" class="tab-content">
        <div class="gastos-container">
          <BudgetView />
        </div>
      </div>

      <!-- DESPESAS TAB -->
      <div v-if="activeTab === 'gastos'" class="tab-content">
        <div class="gastos-container">
          <EmptyState
            v-if="gastos.length === 0"
            title="Ainda não tem despesas cadastradas 😄"
            description="Bora registrar tua primeira despesa?"
            icon="pi pi-receipt"
            action-label="Adicionar despesa"
            @action="showAddModal = true"
          />

          <div v-else>
            <div class="gastos-toolbar">
              <div v-if="currentFamily" class="gasto-filter-tabs">
                <button
                  :class="['filter-tab', { active: gastoFilter === 'todos' }]"
                  @click="gastoFilter = 'todos'"
                >
                  Todos ({{ gastos.length }})
                </button>
                <button
                  :class="['filter-tab', { active: gastoFilter === 'grupo' }]"
                  @click="gastoFilter = 'grupo'"
                >
                  Grupo ({{ gastosGrupo.length }})
                </button>
                <button
                  :class="['filter-tab', { active: gastoFilter === 'meus' }]"
                  @click="gastoFilter = 'meus'"
                >
                  Meus ({{ gastosMeus.length }})
                </button>
              </div>
              <div class="mobile-primary-action">
                <button @click="showAddModal = true" class="btn-primary btn-sm">
                  Nova Despesa
                </button>
              </div>
            </div>

            <div class="gastos-list">
              <EmptyState
                v-if="gastosFiltrados.length === 0"
                variant="no-results"
                title="Não encontrei nada com esse filtro 👀"
                description="Tenta outro filtro ou adiciona uma nova despesa."
                icon="pi pi-search"
              />
              <BaseCard
                v-for="g in gastosFiltrados"
                :key="g.id"
                :icon="getCategoriaIcon(g.categoria)"
                :title="getCategoriaLabel(g.categoria)"
                :subtitle="formatarData(g.data)"
                :value="formatarValor(g.valor)"
                :isGroup="g.is_group"
              >
                <template #header-badge>
                  <span v-if="g.is_group" class="group-badge">Grupo</span>
                </template>
                <template #extras>
                  <small v-if="g.data_competencia && g.data_competencia !== g.data" class="gasto-desc">
                    Mês da despesa: {{ formatarData(g.data_competencia) }}
                  </small>
                  <small v-if="g.data_pagamento" class="gasto-desc">
                    Quando foi pago: {{ formatarData(g.data_pagamento) }}
                  </small>
                  <small v-if="g.descricao" class="gasto-desc">{{ g.descricao }}</small>
                </template>
                <template #meta>
                  <small v-if="g.user_name" class="gasto-user">@{{ g.user_name }}</small>
                </template>
                <template #badges>
                  <span v-if="g.pago" class="pago-badge">Pago</span>
                  <span v-else class="pendente-badge">Pendente</span>
                </template>
                <template #actions>
                  <template v-if="podeEditarGasto(g)">
                    <button @click="abrirEdicao(g)" class="edit-btn" title="Editar">
                      <i class="pi pi-pencil"></i>
                    </button>
                    <button @click="excluirGasto(g.id)" class="delete-btn" title="Excluir">
                      <i class="pi pi-trash"></i>
                    </button>
                  </template>
                </template>
              </BaseCard>
            </div>

            <!-- Paginação -->
            <div v-if="gastosPagination.pages > 1" class="pagination-bar">
              <button
                :disabled="!gastosPagination.previous"
                @click="goToPageGastos(gastosPagination.page - 1)"
                class="btn-pagination"
              >
                <i class="pi pi-chevron-left"></i>
              </button>
              <span class="pagination-info">Página {{ gastosPagination.page }} de {{ gastosPagination.pages }}</span>
              <button
                :disabled="!gastosPagination.next"
                @click="goToPageGastos(gastosPagination.page + 1)"
                class="btn-pagination"
              >
                <i class="pi pi-chevron-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- GRUPO TAB -->
      <div v-if="activeTab === 'grupo'" class="tab-content">
        <div class="gastos-container">
          <FamilyView
            :family="currentFamily"
            :current-user="currentUser"
            @family-action="handleFamilyAction"
          />
        </div>
      </div>

      <!-- RECEITAS TAB -->
      <div v-if="activeTab === 'receitas'" class="tab-content">
        <div class="gastos-container">
          <ReceitasView :initial-edit-data="pendingIncomeEdit" />
        </div>
      </div>

      <!-- PERFIL TAB -->
      <div v-if="activeTab === 'perfil'" class="tab-content">
        <div class="gastos-container">
          <ProfileView />
        </div>
      </div>

      <!-- CONFIGURACOES TAB -->
      <div v-if="activeTab === 'configuracoes'" class="tab-content">
        <div class="gastos-container">
          <SettingsView @reset-onboarding="handleResetOnboarding" />
        </div>
      </div>

    </main>

    <!-- ADD/EDIT EXPENSE MODAL -->
    <ExpenseModal
      :visible="showAddModal"
      :editing-data="expenseEditingData"
      @close="fecharModal"
      @saved="onExpenseSaved"
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
    <AIAssistant
      ref="aiAssistant"
      :hide-fab="true"
      @saved="handleAIAssistantSaved"
      @edit-expense="handleEditExpense"
      @edit-income="handleEditIncome"
    />
    <BeneFloatingPresence
      @open-chat="openAIAssistant"
    />
    <BottomNav
      :active-tab="activeTab"
      @navigate="handleBottomNavNavigate"
    />
  </template>
</div>
  </ErrorBoundary>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { defineAsyncComponent } from 'vue'
import Button from 'primevue/button'
import AuthView from './components/AuthView.vue'
import PasswordResetView from './components/PasswordResetView.vue'
import VerifyEmailView from './components/VerifyEmailView.vue'
import BaseCard from './components/BaseCard.vue'
import BeneFloatingPresence from './components/BeneFloatingPresence.vue'
import ExpenseModal from './components/modals/ExpenseModal.vue'
import ConfirmModal from './components/modals/ConfirmModal.vue'
import BottomNav from './components/BottomNav.vue'
import EmptyState from './components/EmptyState.vue'
import ToastProvider from './components/ToastProvider.vue'
import AppLoading from './components/AppLoading.vue'
import SkeletonDashboard from './components/SkeletonDashboard.vue'
import SkeletonProfile from './components/SkeletonProfile.vue'
import SkeletonSettings from './components/SkeletonSettings.vue'
import SkeletonGeneric from './components/SkeletonGeneric.vue'
import OfflineFallback from './components/OfflineFallback.vue'
import InstallPrompt from './components/InstallPrompt.vue'
import ErrorBoundary from './components/ErrorBoundary.vue'
import WelcomeModal from './components/onboarding/WelcomeModal.vue'
import OnboardingChecklist from './components/onboarding/OnboardingChecklist.vue'

const asyncView = (loader, loading, delay = 200) => defineAsyncComponent({
  loader,
  loadingComponent: loading,
  delay,
})

const DashboardCharts = asyncView(() => import('./components/DashboardCharts.vue'), SkeletonDashboard)
const FamilyView = asyncView(() => import('./components/FamilyView.vue'), SkeletonGeneric)
const ReceitasView = asyncView(() => import('./components/ReceitasView.vue'), SkeletonGeneric)
const BudgetView = asyncView(() => import('./components/BudgetView.vue'), SkeletonGeneric)
const ExtratoView = asyncView(() => import('./components/ExtratoView.vue'), SkeletonGeneric)
const AIAssistant = asyncView(() => import('./components/AIAssistant.vue'), AppLoading)
const ProfileView = asyncView(() => import('./components/ProfileView.vue'), SkeletonProfile)
const SettingsView = asyncView(() => import('./components/SettingsView.vue'), SkeletonSettings)

import logo from './assets/logo.png'
import { toastMessages, toastTitles } from './utils/toastMessages.js'
import { toastStore } from './stores/toast.store.js'
import {
  API_ENDPOINTS,
  apiRequest,
  isAuthenticated,
  clearTokens,
  getFamily
} from './config/api.js'

const isAuth = ref(false)
const activeTab = ref('dashboard')
const currentFamily = ref(null)
const currentUser = ref(null)
const showFamilyDrawer = ref(false)
const showUserMenu = ref(false)
const gastos = ref([])
const gastoFilter = ref('todos')
const loading = ref(false)
const error = ref(null)
const gastosPagination = ref({
  page: 1,
  pages: 1,
  pageSize: 20,
  total: 0,
  next: null,
  previous: null,
})
const showAddModal = ref(false)
const expenseEditingData = ref(null)
const confirmVisible = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmDanger = ref(false)
const confirmAcceptLabel = ref('Confirmar')
const confirmRejectLabel = ref('Cancelar')
let confirmOnAccept = null
const pendingIncomeEdit = ref(null)
const aiAssistant = ref(null)

// Onboarding state
const onboardingStatus = ref({
  group_created: false,
  first_expense: false,
  first_revenue: false,
  first_goal: false,
  progress: 0,
  completed: false,
})
const showWelcomeModal = ref(false)
const showOnboardingChecklist = ref(true)

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

const currentPath = computed(() => window.location.pathname)
const gastosDoMes = computed(() => {
  const mesAtual = new Date().getMonth() + 1
  const anoAtual = new Date().getFullYear()
  return gastos.value.filter(g => {
    const dataGasto = new Date(g.data)
    return dataGasto.getMonth() + 1 === mesAtual &&
           dataGasto.getFullYear() === anoAtual
  })
})
const totalMes = computed(() => gastosDoMes.value.reduce((soma, g) => soma + parseFloat(g.valor), 0))
const gastosGrupo = computed(() => gastos.value.filter(g => g.is_group))
const gastosMeus = computed(() => {
  const myId = currentUser.value?.id
  return gastos.value.filter(g => g.user === myId)
})
const gastosFiltrados = computed(() => {
  if (gastoFilter.value === 'grupo') return gastosGrupo.value
  if (gastoFilter.value === 'meus') return gastosMeus.value
  return gastos.value
})

onMounted(async () => {
  isAuth.value = isAuthenticated()
  if (isAuth.value) {
    await fetchUser()
    await fetchFamily()
    carregarGastos()
  }
})

async function carregarGastos(page = 1) {
  try {
    loading.value = true
    error.value = null
    const url = `${API_ENDPOINTS.GASTOS_LIST}?page=${page}&page_size=${gastosPagination.value.pageSize}`
    const data = await apiRequest(url)
    gastos.value = data.gastos || []
    gastosPagination.value.page = data.page || 1
    gastosPagination.value.pages = data.pages || 1
    gastosPagination.value.total = data.total || 0
    gastosPagination.value.next = data.next || null
    gastosPagination.value.previous = data.previous || null
  } catch (err) {
    error.value = 'Erro ao carregar despesas: ' + err.message
    console.error('Erro ao carregar despesas:', err)
  } finally {
    loading.value = false
  }
}

function goToPageGastos(page) {
  if (page >= 1 && page <= gastosPagination.value.pages) {
    carregarGastos(page)
  }
}

function abrirEdicao(gasto) {
  expenseEditingData.value = gasto
  showAddModal.value = true
}

function fecharModal() {
  showAddModal.value = false
  expenseEditingData.value = null
}

async function onExpenseSaved() {
  await carregarGastos()
}

function formatarData(dataStr) {
  try {
    let processedDate = dataStr
    if (typeof dataStr === 'string') {
      if (/^\d{4}-\d{2}-\d{2}$/.test(dataStr)) {
        processedDate = dataStr + 'T12:00:00'
      } else if (!dataStr.includes('T')) {
        const partes = dataStr.split('/')
        if (partes.length === 3) {
          processedDate = `${partes[2]}-${partes[1]}-${partes[0]}T12:00:00`
        }
      }
    }
    const data = new Date(processedDate)
    if (isNaN(data.getTime())) return 'Data inválida'
    return data.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  } catch (err) {
    console.error('Erro ao formatar data:', err, 'Input:', dataStr)
    return 'Data inválida'
  }
}

function formatarValor(valor) {
  return parseFloat(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function getCategoriaLabel(categoriaValue) {
  const categoria = categorias.value.find(c => c.value === categoriaValue)
  return categoria ? categoria.label : categoriaValue
}

function podeEditarGasto(gasto) {
  if (!currentUser.value) return false
  if (Number(gasto.user) === Number(currentUser.value.id)) return true
  if (currentFamily.value && currentFamily.value.user_role === 'admin') return true
  return false
}

function getCategoriaIcon(categoria) {
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

function formatarTempo(dataStr) {
  try {
    const data = new Date(dataStr)
    if (isNaN(data.getTime())) return 'Data inválida'
    const agora = new Date()
    const diffMs = agora - data
    const diffMin = Math.floor(diffMs / 60000)
    const diffHoras = Math.floor(diffMs / 3600000)
    const diffDias = Math.floor(diffMs / 86400000)
    if (diffMin < 1) return 'agora'
    if (diffMin < 60) return `${diffMin} min atrás`
    if (diffHoras < 24) return `${diffHoras}h atrás`
    if (diffDias < 7) return `${diffDias} dias atrás`
    return data.toLocaleDateString('pt-BR')
  } catch (err) {
    console.error('Erro ao formatar tempo:', err)
    return 'Data inválida'
  }
}

function excluirGasto(id) {
  confirmTitle.value = 'Excluir Despesa'
  confirmMessage.value = 'Tem certeza que deseja excluir esta despesa?'
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Excluir'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = async () => {
    try {
      loading.value = true
      error.value = null
      await apiRequest(API_ENDPOINTS.GASTO_DETAIL(id), { method: 'DELETE' })
      gastos.value = gastos.value.filter(g => g.id !== id)
      toastStore.success(toastMessages.expense.deleted, { title: toastTitles.success })
    } catch (err) {
      if (err.message?.includes('404') || err.message?.includes('não encontrado')) {
        gastos.value = gastos.value.filter(g => g.id !== id)
        toastStore.success(toastMessages.expense.deleted, { title: toastTitles.success })
      } else {
        error.value = 'Erro ao excluir despesa: ' + err.message
        console.error('Erro ao excluir despesa:', err)
        toastStore.error(toastMessages.expense.deleteError, { title: toastTitles.error })
      }
    } finally {
      loading.value = false
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

async function handleLoginSuccess() {
  isAuth.value = true
  await fetchUser()
  await fetchFamily()
  carregarGastos()
  await fetchOnboardingStatus()
  if (!onboardingStatus.value.completed) {
    showWelcomeModal.value = true
  }
}

async function fetchOnboardingStatus() {
  try {
    const data = await apiRequest(API_ENDPOINTS.ONBOARDING)
    onboardingStatus.value = data
    const manuallyClosed = localStorage.getItem('onboarding-checklist-closed')
    showOnboardingChecklist.value = !data.completed && manuallyClosed !== 'true'
  } catch (err) {
    console.warn('Erro ao buscar onboarding:', err)
  }
}

function dismissWelcome() {
  showWelcomeModal.value = false
}

function startOnboarding() {
  showWelcomeModal.value = false
  activeTab.value = 'dashboard'
}

async function dismissChecklist() {
  showOnboardingChecklist.value = false
  if (onboardingStatus.value.completed) {
    return
  }
  localStorage.setItem('onboarding-checklist-closed', 'true')
  try {
    await apiRequest(API_ENDPOINTS.ONBOARDING, {
      method: 'POST',
      body: JSON.stringify({ action: 'complete' })
    })
    onboardingStatus.value.completed = true
  } catch (err) {
    console.warn('Erro ao completar onboarding:', err)
  }
}

async function handleResetOnboarding() {
  try {
    await apiRequest(API_ENDPOINTS.ONBOARDING, {
      method: 'POST',
      body: JSON.stringify({ action: 'reset' })
    })
    localStorage.removeItem('onboarding-checklist-closed')
    onboardingStatus.value.completed = false
    showOnboardingChecklist.value = true
    showWelcomeModal.value = true
    activeTab.value = 'dashboard'
    toastStore.success('Onboarding reiniciado! 😄')
  } catch (err) {
    console.warn('Erro ao resetar onboarding:', err)
  }
}

function handleNavigateFromChecklist(key) {
  switch (key) {
    case 'group':
      activeTab.value = 'grupo'
      break
    case 'expense':
      activeTab.value = 'gastos'
      break
    case 'revenue':
      activeTab.value = 'receitas'
      break
    case 'goal':
      activeTab.value = 'metas'
      break
  }
}

async function fetchUser() {
  try {
    const data = await apiRequest(API_ENDPOINTS.AUTH_USER)
    currentUser.value = data
  } catch (err) {
    console.warn('Não foi possível obter dados do usuário:', err)
  }
}

async function fetchFamily() {
  try {
    currentFamily.value = await getFamily()
  } catch (err) {
    console.warn('Não foi possível obter dados da família:', err)
    currentFamily.value = null
  }
}

function handleBottomNavNavigate(tab) {
  activeTab.value = tab
}

function handleFamilyAction({ action }) {
  if (action === 'created' || action === 'joined') {
    fetchFamily()
    carregarGastos()
  } else if (action === 'left' || action === 'deleted') {
    currentFamily.value = null
    carregarGastos()
  } else if (action === 'code-regenerated' || action === 'member-removed') {
    fetchFamily()
  }
}

function openAIAssistant() {
  aiAssistant.value?.open()
}

function handleAIAssistantSaved() {
  carregarGastos()
}

function handleEditExpense(data) {
  expenseEditingData.value = {
    id: null,
    valor: parseFloat(data.valor),
    categoria: data.categoria || '',
    descricao: data.descricao || '',
    data_competencia: data.data || new Date().toISOString().split('T')[0],
    data_pagamento: '',
    pago: false
  }
  showAddModal.value = true
}

function navigateTo(tab) {
  activeTab.value = tab
  showUserMenu.value = false
}

function handleEditIncome(data) {
  activeTab.value = 'receitas'
  pendingIncomeEdit.value = {
    valor: parseFloat(data.valor),
    descricao: data.descricao || '',
    data: data.data || new Date().toISOString().split('T')[0]
  }
}

function handleLogout() {
  clearTokens()
  isAuth.value = false
  activeTab.value = 'dashboard'
  gastos.value = []
  currentFamily.value = null
  currentUser.value = null
  showFamilyDrawer.value = false
  showUserMenu.value = false
}
</script>

<style>
.page {
  min-height: 100vh;
  background: radial-gradient(circle at top, #0f172a, var(--bg-app));
  color: white;
  padding: var(--space-8) var(--space-5);
}

/* LOGO */
.logo-container {
  text-align: center;
  margin-bottom: 30px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 160px;
}

.logo {
  width: 120px;
  height: 120px;
  border-radius: 10px;
  object-fit: contain;
}

/* HEADER */
.header {
  position: sticky;
  top: 0;
  z-index: var(--z-header);
  background: rgba(11, 18, 32, 0.75);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.header-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 6px 20px;
}

/* CARD */
.card {
  max-width: 420px;
  margin: auto;
  background: #0b1220;
  padding: 25px;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

/* NAV MENU */
.nav-menu {
  display: flex;
  gap: var(--space-2);
  align-items: center;
  justify-self: center;
}

.nav-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: none;
  border: none;
  color: var(--text-muted);
  border-radius: var(--space-2);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 13px;
  font-weight: var(--weight-medium);
}

.nav-item i {
  font-size: 14px;
}

.nav-item:hover {
  color: var(--text-secondary);
  background: var(--bg-hover);
}

.nav-item.active {
  color: var(--color-primary);
  background: var(--color-primary-glow);
}

/* GASTOS CONTAINER */
.gastos-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gastos-container {
  max-width: 1200px;
  margin: var(--space-5) auto 0;
  background: rgba(30, 41, 59, 0.3);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: var(--space-7);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.gastos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.gastos-header h2 {
  font-size: 28px;
  margin: 0;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gastos-stats {
  display: flex;
  gap: 10px;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.stat-badge.primary {
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: var(--radius-md);
  font-size: var(--font-md);
  font-weight: var(--weight-bold);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-soft);
}

.btn-primary:hover {
  filter: brightness(1.1);
}

.btn-primary.btn-sm {
  padding: 10px 20px;
  font-size: var(--font-md);
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.gastos-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.gastos-toolbar .mobile-primary-action {
  margin-left: auto;
}

.gastos-toolbar .btn-sm {
  margin-left: auto;
}

.gasto-desc {
  color: var(--text-secondary);
  font-style: italic;
  display: block;
  margin-bottom: var(--space-1);
  font-size: var(--font-xs);
}

.gasto-time {
  color: var(--text-secondary);
  font-size: var(--font-xs);
}

.delete-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: var(--font-md);
  cursor: pointer;
  transition: color var(--transition-fast);
  padding: var(--space-1);
  line-height: 1;
  min-width: 40px;
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.delete-btn:hover {
  color: var(--color-error);
}

.edit-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: var(--font-md);
  cursor: pointer;
  transition: color var(--transition-fast);
  padding: var(--space-1);
  line-height: 1;
  min-width: 40px;
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.edit-btn:hover {
  color: var(--color-info);
}

/* GASTO FILTER TABS */
.gasto-filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.user-menu-wrapper {
  position: relative;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px 6px 6px;
  border-radius: 24px;
  transition: background 0.2s ease;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  color: inherit;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

.user-name:hover {
  background: rgba(255, 255, 255, 0.06);
}

.user-name i {
  font-size: 11px;
  transition: transform 0.2s ease;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  background: #60A637;
  color: #ffffff;
  flex-shrink: 0;
}

.user-label {
  color: #d1d5db;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  min-width: 220px;
  background: rgba(31, 41, 55, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-sm);
  padding: 6px;
  box-shadow: var(--shadow-card);
  z-index: var(--z-header);
  animation: slideIn 0.15s ease;
  backdrop-filter: blur(20px);
}

/* ANIMATIONS */
@keyframes slideIn {
  from {
    transform: translateY(var(--motion-distance));
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Motion tokens: use transform/opacity only for performance */

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.dropdown-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.dropdown-name {
  color: #f3f4f6;
  font-size: 14px;
  font-weight: 500;
}

.dropdown-email {
  color: #6b7280;
  font-size: 12px;
}

.dropdown-divider {
  height: 1px;
  background: #374151;
  margin: 4px 0;
}

.dropdown-group-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
}

.group-label {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.group-name {
  font-size: 13px;
  color: #60A637;
  font-weight: 600;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  width: 100%;
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 13px;
  font-weight: 400;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
  border-radius: 6px;
  white-space: nowrap;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.04);
  color: #e5e7eb;
}

.dropdown-item.danger {
  color: #9ca3af;
}

.dropdown-item.danger:hover {
  background: rgba(239, 68, 68, 0.08);
  color: #ef4444;
}

.filter-tab {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--space-2);
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: var(--bg-hover);
  color: var(--text-muted);
  font-size: 13px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
}

.filter-tab.active {
  background: var(--color-primary-glow);
  border-color: rgba(96, 166, 55, 0.3);
  color: var(--color-primary);
}

.group-badge {
  font-size: 10px;
  padding: 2px var(--space-2);
  border-radius: 4px;
  background: rgba(96, 166, 55, 0.15);
  color: var(--color-primary);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.gasto-user {
  display: block;
  margin-top: var(--space-1);
  color: var(--text-secondary);
  font-size: var(--font-xs);
}

.pago-badge {
  display: inline-block;
  margin-top: var(--space-1);
  padding: var(--space-1) 10px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  font-size: var(--font-xs);
  font-weight: var(--weight-semibold);
  border-radius: var(--radius-full);
}

.pendente-badge {
  display: inline-block;
  margin-top: var(--space-1);
  padding: var(--space-1) 10px;
  background: linear-gradient(90deg, var(--color-error), #f87171);
  color: #ffffff;
  font-size: var(--font-xs);
  font-weight: var(--weight-semibold);
  border-radius: var(--radius-full);
}

/* FORM CONTAINER */
.form-container {
  max-width: 400px;
  margin: 0 auto;
}

.form-card {
  background: rgba(30, 41, 59, 0.2);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-md);
  padding: var(--space-7);
  border: var(--glass-border);
}

.form-card h2 {
  text-align: center;
  margin: 0 0 var(--space-6) 0;
  font-size: 22px;
  color: white;
  font-weight: var(--weight-semibold);
}

.gasto-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 13px;
  font-weight: var(--weight-semibold);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: var(--space-3);
}

.form-input,
.form-select {
  width: 100%;
  height: 56px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: var(--font-md);
  font-weight: var(--weight-medium);
  color: var(--text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input::placeholder {
  color: var(--text-muted);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px var(--color-primary-glow);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: var(--space-4);
  color: var(--text-muted);
  font-weight: var(--weight-medium);
  font-size: 15px;
  pointer-events: none;
  z-index: 1;
}

.input-field {
  padding-left: 44px;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='rgba(248,250,252,0.45)' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.form-select option {
  background: #1e293b;
  color: white;
}

/* Checkbox */
.form-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 400;
}

.form-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  accent-color: var(--color-primary);
  cursor: pointer;
}

/* Buttons */
.btn-secondary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: var(--hover-lift);
}

.btn-secondary:active {
  transform: var(--active-press);
}

.btn-primary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-glow);
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.05);
  transform: var(--hover-lift);
}

.btn-primary:active:not(:disabled) {
  transform: var(--active-press);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.4);
}

/* HEADER RIGHT */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: var(--color-error);
  border-radius: var(--space-2);
  font-size: 13px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.25);
}

.logout-btn i {
  font-size: 14px;
}

/* FAMILY BUTTON */
.family-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-muted);
  border-radius: var(--space-2);
  font-size: 13px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.family-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
}

.family-btn.has-family {
  background: var(--color-primary-glow);
  border-color: rgba(96, 166, 55, 0.3);
  color: var(--color-primary);
}

.family-btn.has-family:hover {
  background: rgba(96, 166, 55, 0.15);
}

.family-badge {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  background: rgba(96, 166, 55, 0.15);
  border: 1px solid rgba(96, 166, 55, 0.3);
  color: var(--color-primary);
  padding: 2px var(--space-2);
  border-radius: 6px;
  font-size: var(--font-xs);
  font-weight: var(--weight-semibold);
}

.family-dot {
  color: var(--color-primary);
  font-size: 10px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-self: end;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 12px;
    grid-template-columns: none;
  }

  .logo {
    width: 96px;
    height: 96px;
  }

  .brand {
    font-size: 20px;
  }

  .header-right {
    flex-wrap: wrap;
    justify-content: flex-end;
  }

  .nav-menu {
    display: none;
  }

  .logout-btn {
    padding: 6px 10px;
    font-size: 12px;
  }

  .main-content {
    padding: var(--space-4) 15px calc(var(--space-4) + var(--mobile-header-height) + var(--safe-bottom));
  }

  .gastos-container,
  .form-card {
    padding: 20px;
    background: linear-gradient(180deg, rgba(30,41,59,0.88) 0%, rgba(15,23,42,0.92) 100%);
  }

  .gastos-header {
    flex-direction: column;
    text-align: center;
  }

  .gastos-toolbar {
    flex-direction: column;
    align-items: center;
    gap: 8px;
    text-align: center;
  }

  .gasto-filter-tabs {
    justify-content: center;
  }

  .gastos-toolbar .mobile-primary-action {
    display: block;
    text-align: center;
    margin: 12px 0 16px;
  }

  /* Header minimalista: só avatar, sem texto */
  .user-name {
    padding: 4px;
    gap: 0;
    background: none;
    border: none;
  }

  .user-name .user-label,
  .user-name .pi-chevron-down {
    display: none;
  }

  .user-name .user-avatar {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }

  /* Mobile Primary Action Wrapper */
  .mobile-primary-action {
    display: flex;
    justify-content: center;
    margin: 20px 0 24px;
    width: 100%;
  }

  .mobile-primary-action .btn-primary,
  .mobile-primary-action .btn-primary.btn-sm {
    width: fit-content;
    min-width: 200px;
    max-width: 240px;
    height: 52px;
    padding: 0 24px;
    border-radius: 16px;
    background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
    box-shadow: 0 0 18px rgba(96,166,55,0.12);
    font-size: 17px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  .mobile-primary-action .btn-primary i {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .nav-tabs {
    flex-direction: column;
    width: 100%;
  }

  .tab-btn {
    width: 100%;
    justify-content: center;
  }

  .logo-section {
    flex-direction: column;
  }

  .brand-section .brand {
    font-size: 20px;
  }
}

/* Modal styles are now handled by ModalBase.vue */
</style>