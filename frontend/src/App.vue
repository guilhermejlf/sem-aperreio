<template>
  <div class="page">

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
              <button class="dropdown-item" @click="showUserMenu = false">
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

      <!-- GASTOS TAB -->
      <div v-if="activeTab === 'gastos'" class="tab-content">
        <div class="gastos-container">
          <div v-if="gastos.length === 0" class="empty-state">
            <i class="pi pi-inbox"></i>
            <h3>Nenhuma despesa cadastrada</h3>
            <p>Comece adicionando seu primeiro gasto para ver o painel completo!</p>
            <div class="mobile-primary-action">
              <button @click="showAddModal = true" class="btn-primary">
                Adicionar Primeira Despesa
              </button>
            </div>
          </div>

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
              <div v-if="gastosFiltrados.length === 0" class="empty-filter">
                <p>Nenhuma despesa nesta categoria.</p>
              </div>
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

    </main>

    <!-- ADD/EDIT EXPENSE MODAL -->
    <ModalBase
      :visible="showAddModal"
      :title="editingGasto ? 'Editar Despesa' : 'Adicionar Despesa'"
      :highlight="'Despesa'"
      size="medium"
      @close="fecharModal"
    >
      <form @submit.prevent="editingGasto ? salvarEdicao() : adicionarGasto()" class="gasto-form">
        <div class="form-group">
          <label class="form-label">Valor</label>
          <div class="input-wrapper">
            <span class="input-prefix">R$</span>
            <input
              v-model.number="novo.valor"
              type="number"
              step="0.01"
              min="0.01"
              class="form-input input-field"
              placeholder="0,00"
              ref="inputValor"
              autofocus
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Categoria</label>
          <select v-model="novo.categoria" class="form-select">
            <option value="">Selecione uma categoria</option>
            <option v-for="cat in categorias" :key="cat.value" :value="cat.value">
              {{ cat.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Descrição</label>
          <input
            v-model="novo.descricao"
            type="text"
            placeholder="Ex: Mercado, Uber, McDonald's..."
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Data da despesa</label>
          <input
            type="date"
            v-model="novo.data_competencia"
            class="form-input"
          />
        </div>

        <div class="form-group checkbox-group">
          <label class="form-checkbox">
            <input
              type="checkbox"
              v-model="novo.pago"
            />
            <span>Já paguei essa despesa</span>
          </label>
        </div>

        <div class="form-group" v-if="novo.pago">
          <label class="form-label">Data do pagamento</label>
          <input
            type="date"
            v-model="novo.data_pagamento"
            class="form-input"
          />
        </div>
      </form>

      <template #footer>
        <button class="btn-secondary" @click="fecharModal">Cancelar</button>
        <button
          class="btn-primary"
          :disabled="loading || !formValido"
          @click="editingGasto ? salvarEdicao() : adicionarGasto()"
        >
          {{ editingGasto ? 'Salvar alterações' : 'Salvar despesa' }}
        </button>
      </template>
    </ModalBase>

    <Toast position="top-right" />
    <ConfirmDialog />
    <AIAssistant
      ref="aiAssistant"
      :hide-fab="true"
      @saved="handleAIAssistantSaved"
      @edit-expense="handleEditExpense"
      @edit-income="handleEditIncome"
    />
    <BeneFloatingPresence
      :chat-open="beneStore?.visible || false"
      @open-chat="openAIAssistant"
    />
    <BottomNav
      :active-tab="activeTab"
      @navigate="activeTab = $event"
      class="bottom-nav-mobile"
    />
  </template>
</div>
</template>

<script>
import Button from 'primevue/button'
import DashboardCharts from './components/DashboardCharts.vue'
import AuthView from './components/AuthView.vue'
import FamilyView from './components/FamilyView.vue'
import ReceitasView from './components/ReceitasView.vue'
import BudgetView from './components/BudgetView.vue'
import ExtratoView from './components/ExtratoView.vue'
import BaseCard from './components/BaseCard.vue'
import AIAssistant from './components/AIAssistant.vue'
import PasswordResetView from './components/PasswordResetView.vue'
import VerifyEmailView from './components/VerifyEmailView.vue'
import BeneFloatingPresence from './components/BeneFloatingPresence.vue'
import ProfileView from './components/ProfileView.vue'
import ModalBase from './components/ModalBase.vue'
import BottomNav from './components/BottomNav.vue'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import logo from './assets/logo.png'
import {
  API_ENDPOINTS,
  API_BASE_URL,
  apiRequest,
  isAuthenticated,
  clearTokens,
  getFamily
} from './config/api.js'

export default {
  components: {
    Button,
    DashboardCharts,
    AuthView,
    FamilyView,
    ReceitasView,
    BudgetView,
    ExtratoView,
    BaseCard,
    AIAssistant,
    PasswordResetView,
    VerifyEmailView,
    BeneFloatingPresence,
    ProfileView,
    ModalBase,
    BottomNav,
    Toast,
    ConfirmDialog
  },

  data() {
    return {
      logo,
      isAuth: false,
      activeTab: 'dashboard',
      currentFamily: null,
      currentUser: null,
      showFamilyDrawer: false,
      showUserMenu: false,
      gastos: [],
      gastoFilter: 'todos', // 'todos' | 'grupo' | 'meus'
      novo: {
        valor: null,
        categoria: '',
        descricao: '',
        data: new Date().toISOString().split('T')[0],
        data_competencia: '',
        data_pagamento: '',
        pago: false
      },
      loading: false,
      error: null,
      showAddModal: false,
      editingGasto: null,
      pendingIncomeEdit: null,
      beneStore: null,
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
      ]
    }
  },

  computed: {
    currentPath() {
      return window.location.pathname
    },
    gastosDoMes() {
      const mesAtual = new Date().getMonth() + 1
      const anoAtual = new Date().getFullYear()
      
      return this.gastos.filter(g => {
        const dataGasto = new Date(g.data)
        return dataGasto.getMonth() + 1 === mesAtual && 
               dataGasto.getFullYear() === anoAtual
      })
    },

    totalMes() {
      return this.gastosDoMes
        .reduce((soma, g) => soma + parseFloat(g.valor), 0)
    },

    formValido() {
      return this.novo.valor && 
             this.novo.valor > 0 && 
             this.novo.categoria && 
             this.novo.data_competencia
    },

    gastosGrupo() {
      return this.gastos.filter(g => g.is_group)
    },
    gastosMeus() {
      // Todos os gastos que EU criei (grupo ou individual)
      const myId = this.currentUser?.id
      return this.gastos.filter(g => g.user === myId)
    },
    gastosFiltrados() {
      if (this.gastoFilter === 'grupo') return this.gastosGrupo
      if (this.gastoFilter === 'meus') return this.gastosMeus
      return this.gastos
    }
  },

  async mounted() {
    this.isAuth = isAuthenticated()
    if (this.isAuth) {
      await this.fetchUser()
      await this.fetchFamily()
      this.carregarGastos()
    }
    import('./stores/beneContext.store.js').then(m => {
      this.beneStore = m.beneStore || m.default
    })
  },

  methods: {
    async carregarGastos() {
      try {
        this.loading = true
        this.error = null
        const data = await apiRequest(API_ENDPOINTS.GASTOS_LIST)
        this.gastos = data.gastos || []
      } catch (error) {
        this.error = 'Erro ao carregar gastos: ' + error.message
        console.error('Erro ao carregar gastos:', error)
      } finally {
        this.loading = false
      }
    },

    abrirEdicao(gasto) {
      this.novo = {
        valor: parseFloat(gasto.valor),
        categoria: gasto.categoria,
        descricao: gasto.descricao || '',
        data: new Date().toISOString().split('T')[0],
        data_competencia: gasto.data_competencia || '',
        data_pagamento: gasto.data_pagamento || '',
        pago: gasto.pago || false
      }
      this.editingGasto = gasto.id
      this.showAddModal = true
    },

    fecharModal() {
      this.showAddModal = false
      this.editingGasto = null
      this.novo = {
        valor: null,
        categoria: '',
        descricao: '',
        data: new Date().toISOString().split('T')[0],
        data_competencia: '',
        data_pagamento: '',
        pago: false
      }
    },

    async adicionarGasto() {
      try {
        this.loading = true
        this.error = null
        
        // Validação básica
        if (!this.novo.valor || this.novo.valor <= 0) {
          this.error = 'Informe um valor válido'
          return
        }
        
        if (!this.novo.data_competencia) {
          this.error = 'Informe o mês do gasto'
          return
        }

        const payload = { ...this.novo, data: this.novo.data_competencia || this.novo.data }
        const response = await apiRequest(API_ENDPOINTS.GASTOS_LIST, {
          method: 'POST',
          body: JSON.stringify(payload)
        })

        this.$toast.add({
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Gasto adicionado!',
          life: 3000
        })

        if (response.alerta_meta) {
          this.$toast.add({
            severity: response.alerta_meta.status === 'critical' ? 'error' : 'warn',
            summary: 'Meta de Gastos',
            detail: response.alerta_meta.mensagem,
            life: 6000
          })
        }

        this.fecharModal()
        
        // Recarregar lista
        await this.carregarGastos()

      } catch (error) {
        this.error = 'Erro ao adicionar gasto: ' + error.message
        console.error('Erro ao adicionar gasto:', error)
      } finally {
        this.loading = false
      }
    },

    async salvarEdicao() {
      try {
        this.loading = true
        this.error = null

        if (!this.novo.valor || this.novo.valor <= 0) {
          this.error = 'Informe um valor válido'
          return
        }

        if (!this.novo.data_competencia) {
          this.error = 'Informe o mês do gasto'
          return
        }

        const payload = { ...this.novo, data: this.novo.data_competencia || this.novo.data }
        const response = await apiRequest(API_ENDPOINTS.GASTO_DETAIL(this.editingGasto), {
          method: 'PUT',
          body: JSON.stringify(payload)
        })

        this.$toast.add({
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Gasto atualizado!',
          life: 3000
        })

        if (response.alerta_meta) {
          this.$toast.add({
            severity: response.alerta_meta.status === 'critical' ? 'error' : 'warn',
            summary: 'Meta de Gastos',
            detail: response.alerta_meta.mensagem,
            life: 6000
          })
        }

        this.fecharModal()
        await this.carregarGastos()

      } catch (error) {
        this.error = 'Erro ao editar gasto: ' + error.message
        console.error('Erro ao editar gasto:', error)
      } finally {
        this.loading = false
      }
    },

    formatarData(dataStr) {
      try {
        let processedDate = dataStr
        
        // Tratar diferentes formatos de data
        if (typeof dataStr === 'string') {
          // Se for formato YYYY-MM-DD (ISO date)
          if (/^\d{4}-\d{2}-\d{2}$/.test(dataStr)) {
            processedDate = dataStr + 'T12:00:00' // Adiciona hora para evitar timezone issues
          }
          // Se for formato ISO completo
          else if (dataStr.includes('T')) {
            // Mantém como está
          }
          // Se for outro formato, tenta converter
          else {
            const partes = dataStr.split('/')
            if (partes.length === 3) {
              // Formato DD/MM/YYYY -> YYYY-MM-DD
              processedDate = `${partes[2]}-${partes[1]}-${partes[0]}T12:00:00`
            }
          }
        }
        
        const data = new Date(processedDate)
        
        // Verificar se a data é válida
        if (isNaN(data.getTime())) {
          return 'Data inválida'
        }
        
        // Formatar para brasileiro
        return data.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit', 
          year: 'numeric'
        })
      } catch (error) {
        console.error('Erro ao formatar data:', error, 'Input:', dataStr)
        return 'Data inválida'
      }
    },

    formatarValor(valor) {
      return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    getCategoriaLabel(categoriaValue) {
      const categoria = this.categorias.find(c => c.value === categoriaValue)
      return categoria ? categoria.label : categoriaValue
    },

    podeEditarGasto(gasto) {
      // Se não tem usuário logado, não pode editar
      if (!this.currentUser) return false
      
      // Se o gasto é do próprio usuário, pode editar
      if (Number(gasto.user) === Number(this.currentUser.id)) return true
      
      // Se é admin do grupo, pode editar qualquer gasto do grupo
      if (this.currentFamily && this.currentFamily.user_role === 'admin') return true
      
      return false
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
    },

    formatarTempo(dataStr) {
      try {
        const data = new Date(dataStr)
        
        // Verificar se a data é válida
        if (isNaN(data.getTime())) {
          return 'Data inválida'
        }
        
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
      } catch (error) {
        console.error('Erro ao formatar tempo:', error)
        return 'Data inválida'
      }
    },

    async excluirGasto(id) {
      this.$confirm.require({
        message: 'Tem certeza que deseja excluir este gasto?',
        header: 'Excluir Gasto',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Excluir',
        rejectLabel: 'Cancelar',
        acceptClass: 'p-button-danger',
        accept: async () => {
          try {
            this.loading = true
            this.error = null

            await apiRequest(API_ENDPOINTS.GASTO_DETAIL(id), {
              method: 'DELETE'
            })

            // Remove o gasto da lista localmente
            this.gastos = this.gastos.filter(g => g.id !== id)

            this.$toast.add({
              severity: 'success',
              summary: 'Sucesso',
              detail: 'Gasto excluído!',
              life: 3000
            })
          } catch (error) {
            this.error = 'Erro ao excluir gasto: ' + error.message
            console.error('Erro ao excluir gasto:', error)
          } finally {
            this.loading = false
          }
        }
      })
    },

    async handleLoginSuccess() {
      this.isAuth = true
      await this.fetchUser()
      await this.fetchFamily()
      this.carregarGastos()
    },

    async fetchUser() {
      try {
        const data = await apiRequest(API_ENDPOINTS.AUTH_USER)
        this.currentUser = data
      } catch (error) {
        console.warn('Não foi possível obter dados do usuário:', error)
      }
    },

    async fetchFamily() {
      try {
        this.currentFamily = await getFamily()
      } catch (error) {
        console.warn('Não foi possível obter dados da família:', error)
        this.currentFamily = null
      }
    },

    handleFamilyAction({ action }) {
      if (action === 'created' || action === 'joined') {
        this.fetchFamily()
        this.carregarGastos()
      } else if (action === 'left' || action === 'deleted') {
        this.currentFamily = null
        this.carregarGastos()
      } else if (action === 'code-regenerated' || action === 'member-removed') {
        this.fetchFamily()
      }
    },

    openAIAssistant() {
      this.$refs.aiAssistant?.open()
    },

    handleAIAssistantSaved() {
      this.carregarGastos()
    },

    handleEditExpense(data) {
      this.novo = {
        valor: parseFloat(data.valor),
        categoria: data.categoria || '',
        descricao: data.descricao || '',
        data: new Date().toISOString().split('T')[0],
        data_competencia: data.data || new Date().toISOString().split('T')[0],
        data_pagamento: '',
        pago: false
      }
      this.editingGasto = null
      this.showAddModal = true
    },

    navigateTo(tab) {
      this.activeTab = tab
      this.showUserMenu = false
    },

    handleEditIncome(data) {
      // Navegar para aba de receitas com dados pré-preenchidos
      this.activeTab = 'receitas'
      this.pendingIncomeEdit = {
        valor: parseFloat(data.valor),
        descricao: data.descricao || '',
        data: data.data || new Date().toISOString().split('T')[0]
      }
    },

    handleLogout() {
      clearTokens()
      this.isAuth = false
      this.activeTab = 'dashboard'
      this.gastos = []
      this.currentFamily = null
      this.currentUser = null
      this.showFamilyDrawer = false
      this.showUserMenu = false
    }
  }
}
</script>

<style>
.page {
  min-height: 100vh;
  background: radial-gradient(circle at top, #0f172a, #020617);
  color: white;
  padding: 40px 20px;
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
  z-index: 1000;
  background: rgba(11, 18, 32, 0.75);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
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
  gap: 4px;
  align-items: center;
  justify-self: center;
}

.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: none;
  border: none;
  color: #9ca3af;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  font-weight: 500;
}

.nav-item i {
  font-size: 14px;
}

.nav-item:hover {
  color: #e5e7eb;
  background: rgba(255, 255, 255, 0.03);
}

.nav-item.active {
  color: #60A637;
  background: rgba(96, 166, 55, 0.08);
}

/* GASTOS CONTAINER */
.gastos-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gastos-container {
  max-width: 1200px;
  margin: 20px auto 0;
  background: rgba(30, 41, 59, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
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
  background: linear-gradient(90deg, #60A637, #3b82f6);
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
  background: linear-gradient(90deg, #60A637, #3b82f6);
}

/* EMPTY STATE */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  margin: 20px 0 10px;
  color: #e5e7eb;
}

.empty-state p {
  margin: 0 0 30px;
  font-size: 16px;
  line-height: 1.6;
}

.btn-primary {
  background: linear-gradient(135deg, #60A637, #4C8932);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
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
  color: rgba(148, 163, 184, 0.92);
  font-style: italic;
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
}

.gasto-time {
  color: rgba(148, 163, 184, 0.92);
  font-size: 12px;
}

.delete-btn {
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

.delete-btn:hover {
  color: #ef4444;
}

.edit-btn {
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

.edit-btn:hover {
  color: #3b82f6;
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
  top: calc(100% + 8px);
  right: 0;
  min-width: 220px;
  background: rgba(31, 41, 55, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 6px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  z-index: 1000;
  animation: dropdownIn 0.15s ease;
  backdrop-filter: blur(20px);
}

@keyframes dropdownIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

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
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.03);
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #e5e7eb;
}

.filter-tab.active {
  background: rgba(96, 166, 55, 0.1);
  border-color: rgba(96, 166, 55, 0.3);
  color: #60A637;
}

.group-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(96, 166, 55, 0.15);
  color: #60A637;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.gasto-user {
  display: block;
  margin-top: 4px;
  color: rgba(148, 163, 184, 0.88);
  font-size: 12px;
}

.pago-badge {
  display: inline-block;
  margin-top: 4px;
  padding: 4px 10px;
  background: linear-gradient(90deg, #60A637, #4C8932);
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
}

.pendente-badge {
  display: inline-block;
  margin-top: 4px;
  padding: 4px 10px;
  background: linear-gradient(90deg, #ef4444, #f87171);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
}

.empty-filter {
  text-align: center;
  padding: 32px;
  color: #94a3b8;
  font-size: 14px;
}

/* FORM CONTAINER */
.form-container {
  max-width: 400px;
  margin: 0 auto;
}

.form-card {
  background: rgba(30, 41, 59, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 32px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.form-card h2 {
  text-align: center;
  margin: 0 0 24px 0;
  font-size: 22px;
  color: white;
  font-weight: 600;
}

/* Modal form styles - Design System v2.0 */
.gasto-form {
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

.form-input,
.form-select {
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

.form-input:focus,
.form-select:focus {
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
  gap: 10px;
  cursor: pointer;
  color: rgba(248, 250, 252, 0.82);
  font-size: 15px;
  font-weight: 400;
}

.form-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  accent-color: #60A637;
  cursor: pointer;
}

/* Buttons */
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

/* ANIMATIONS */
@keyframes slideIn {
  from {
    transform: translateY(-20px);
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
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  color: #ef4444;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
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
  color: #9ca3af;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.family-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #d1d5db;
}

.family-btn.has-family {
  background: rgba(96, 166, 55, 0.1);
  border-color: rgba(96, 166, 55, 0.3);
  color: #60A637;
}

.family-btn.has-family:hover {
  background: rgba(96, 166, 55, 0.15);
}

.family-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(96, 166, 55, 0.15);
  border: 1px solid rgba(96, 166, 55, 0.3);
  color: #60A637;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.family-dot {
  color: #60A637;
  font-size: 10px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-self: end;
}

/* BOTTOM NAV — desktop hidden */
.bottom-nav-mobile {
  display: none;
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
    padding: 16px 15px calc(16px + 64px + env(safe-area-inset-bottom));
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

  .bottom-nav-mobile {
    display: flex;
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