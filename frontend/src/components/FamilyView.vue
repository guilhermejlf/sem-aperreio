<template>
  <div class="family-page">
    <ContextualTooltip
      v-if="showFamilyTooltip"
      text="Convide familiares para compartilhar despesas e acompanhar o orçamento juntos."
      @dismiss="dismissFamilyTooltip"
    />
    <!-- Loading -->
    <div v-if="loading" class="family-loading">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      <p>Carregando...</p>
    </div>

    <!-- Sem Grupo -->
    <template v-else-if="pageState === 'no-group'">
      <div class="family-empty-state">
        <EmptyState
          title="Nenhum grupo criado"
          description="Compartilha despesas e acompanha o orçamento em família."
          icon="pi pi-users"
          action-label="Criar Grupo Familiar"
          @action="pageState = 'create-form'"
        />
        <div class="divider">
          <span>ou</span>
        </div>
        <button
          class="btn-primary-outlined"
          @click="pageState = 'join-form'"
        >
          Entrar com Código
        </button>
      </div>
    </template>

    <!-- Form Criar Grupo -->
    <div v-else-if="pageState === 'create-form'" class="family-form">
      <h3 class="family-title">Criar Grupo Familiar</h3>

      <div class="form-field">
        <label>Nome do Grupo <span class="required">*</span></label>
        <input
          v-model="newGroupName"
          type="text"
          class="native-input"
          placeholder="Ex: Família Silva"
          @keyup.enter="handleCreate"
        />
      </div>

      <button
        class="btn-primary"
        :disabled="actionLoading"
        @click="handleCreate"
      >
        {{ actionLoading ? 'Criando...' : 'Criar Grupo' }}
      </button>
      <button class="cancel-link" @click="pageState = 'no-group'">
        Cancelar
      </button>
    </div>

    <!-- Form Entrar com Código -->
    <div v-else-if="pageState === 'join-form'" class="family-form">
      <h3 class="family-title">Entrar em Grupo</h3>

      <div class="form-field">
        <label>Código de Convite <span class="required">*</span></label>
        <input
          v-model="joinCode"
          type="text"
          class="native-input code-input"
          placeholder="Ex: A3B7K9"
          maxlength="6"
          @input="joinCode = joinCode.toUpperCase()"
          @keyup.enter="handleJoin"
        />
      </div>

      <button
        class="btn-primary"
        :disabled="actionLoading"
        @click="handleJoin"
      >
        {{ actionLoading ? 'Entrando...' : 'Entrar no Grupo' }}
      </button>
      <button class="cancel-link" @click="pageState = 'no-group'">
        Cancelar
      </button>
    </div>

    <!-- Com Grupo -->
    <div v-else-if="pageState === 'has-group'" class="family-group">
      <h3 class="family-title">{{ familyData.name }}</h3>

      <!-- Código de Convite -->
      <div class="section">
        <label class="section-label">Código de Convite</label>
        <div class="code-box">
          <span class="code-text">{{ familyData.code }}</span>
          <button
            class="edit-btn"
            @click="copyCode"
            title="Copiar"
          >
            <i class="pi pi-copy"></i>
          </button>
        </div>
        <p class="expiration-text" :class="codeExpiringSoon ? 'expiring' : ''">
          {{ expirationText }}
        </p>
        <button
          v-if="isAdmin"
          class="btn-primary btn-sm mt-2"
          :disabled="actionLoading"
          @click="handleRegenerateCode"
        >
          {{ actionLoading ? 'Gerando...' : 'Gerar Novo Código' }}
        </button>
      </div>

      <!-- Membros -->
      <div class="section">
        <label class="section-label">Membros ({{ members.length }})</label>
        <div class="members-list">
          <BaseCard
            v-for="member in members"
            :key="member.id"
            :title="member.user.first_name || member.user.username"
            :subtitle="'@' + member.user.username"
          >
            <template #icon>
              <div class="member-avatar" :style="{ backgroundColor: getAvatarColor(member.user.username) }">
                {{ getInitials(member.user.first_name || member.user.username) }}
              </div>
            </template>
            <template #header-badge>
              <span v-if="isCurrentUser(member)" class="badge you">Você</span>
              <span v-if="member.role === 'admin'" class="badge admin">Admin</span>
            </template>
            <template #actions>
              <button
                v-if="isAdmin && !isCurrentUser(member)"
                class="delete-btn"
                title="Expulsar"
                @click="confirmExpel(member)"
              >
                <i class="pi pi-trash"></i>
              </button>
            </template>
          </BaseCard>
        </div>
      </div>

      <!-- Ações Admin -->
      <div v-if="isAdmin" class="section actions">
        <button
          class="btn-danger-outlined"
          @click="confirmDeleteGroup"
        >
          Excluir Grupo
        </button>
      </div>

      <!-- Sair do Grupo -->
      <div class="section actions">
        <button
          class="btn-danger-outlined"
          @click="confirmLeave"
        >
          Sair do Grupo
        </button>
      </div>
    </div>

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
import Toast from 'primevue/toast'
import BaseCard from './BaseCard.vue'
import EmptyState from './EmptyState.vue'
import ConfirmModal from './modals/ConfirmModal.vue'
import { toastMessages, toastTitles } from '../utils/toastMessages.js'
import { toastStore } from '../stores/toast.store.js'
import ContextualTooltip from './onboarding/ContextualTooltip.vue'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'
import {
  createFamily,
  joinFamily,
  leaveFamily,
  regenerateFamilyCode,
  removeFamilyMember,
  deleteFamily
} from '../config/api.js'

const props = defineProps({
  family: {
    type: Object,
    default: null
  },
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['family-action'])

const pageState = ref('no-group')
const newGroupName = ref('')
const joinCode = ref('')
const loading = ref(false)
const actionLoading = ref(false)
const confirmVisible = ref(false)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmDanger = ref(false)
const confirmAcceptLabel = ref('Confirmar')
const confirmRejectLabel = ref('Cancelar')
let confirmOnAccept = null
const showFamilyTooltip = ref(false)

async function fetchOnboarding() {
  try {
    const data = await apiRequest(API_ENDPOINTS.ONBOARDING)
    showFamilyTooltip.value = !data.seen_family_tooltip
  } catch (err) {
    showFamilyTooltip.value = false
  }
}

async function dismissFamilyTooltip() {
  showFamilyTooltip.value = false
  try {
    await apiRequest(API_ENDPOINTS.ONBOARDING, {
      method: 'POST',
      body: JSON.stringify({ action: 'dismiss_tooltip', tooltip: 'family' })
    })
  } catch (e) {}
}

const familyData = computed(() => props.family || null)
const members = computed(() => familyData.value?.members || [])
const isAdmin = computed(() => {
  if (!familyData.value || !props.currentUser) return false
  const me = members.value.find(m => m.user.id === props.currentUser.id)
  return me?.role === 'admin'
})
const codeExpiringSoon = computed(() => {
  if (!familyData.value?.code_expires_at) return false
  const expires = new Date(familyData.value.code_expires_at)
  const now = new Date()
  const diffHours = (expires - now) / (1000 * 60 * 60)
  return diffHours < 24
})
const expirationText = computed(() => {
  if (!familyData.value?.code_expires_at) return ''
  const expires = new Date(familyData.value.code_expires_at)
  const now = new Date()
  if (now > expires) return 'Código expirado'
  const diffDays = Math.ceil((expires - now) / (1000 * 60 * 60 * 24))
  return diffDays <= 1 ? 'Expira em menos de 24h' : `Expira em ${diffDays} dias`
})

onMounted(() => {
  fetchOnboarding()
})

watch(() => props.family, (newVal) => {
  updateState(newVal)
}, { immediate: true })

function updateState(family) {
  if (family) {
    pageState.value = 'has-group'
  } else {
    pageState.value = 'no-group'
  }
  newGroupName.value = ''
  joinCode.value = ''
}

function isCurrentUser(member) {
  return member.user.id === props.currentUser?.id
}

function getInitials(name) {
  return name.charAt(0).toUpperCase()
}

function getAvatarColor(str) {
  const colors = ['#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#06b6d4', '#ec4899', '#10b981', '#f97316']
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

async function handleCreate() {
  const name = newGroupName.value.trim()
  if (!name) {
    toastStore.error(toastMessages.family.nameRequired, { title: toastTitles.error })
    return
  }
  actionLoading.value = true
  try {
    const data = await createFamily(name)
    emit('family-action', { action: 'created', data })
    toastStore.success(toastMessages.family.created, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

async function handleJoin() {
  const code = joinCode.value.trim().toUpperCase()
  if (code.length !== 6) {
    toastStore.error(toastMessages.family.codeLength, { title: toastTitles.error })
    return
  }
  actionLoading.value = true
  try {
    const data = await joinFamily(code)
    emit('family-action', { action: 'joined', data })
    toastStore.success(toastMessages.family.joined, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

async function handleRegenerateCode() {
  actionLoading.value = true
  try {
    const data = await regenerateFamilyCode()
    emit('family-action', { action: 'code-regenerated', data })
    toastStore.success(toastMessages.family.codeRegenerated, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

async function handleLeave() {
  actionLoading.value = true
  try {
    await leaveFamily()
    emit('family-action', { action: 'left' })
    toastStore.success(toastMessages.family.left, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

async function handleExpel(member) {
  actionLoading.value = true
  try {
    await removeFamilyMember(member.user.id)
    emit('family-action', { action: 'member-removed', data: member })
    toastStore.success(toastMessages.family.memberRemoved, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

async function handleDeleteGroup() {
  actionLoading.value = true
  try {
    await deleteFamily()
    emit('family-action', { action: 'deleted' })
    toastStore.success(toastMessages.family.groupDeleted, { title: toastTitles.success })
  } catch (err) {
    toastStore.error(toastMessages.family.saveError, { title: toastTitles.error })
  } finally {
    actionLoading.value = false
  }
}

function copyCode() {
  navigator.clipboard.writeText(familyData.value.code)
  toastStore.success(toastMessages.family.codeCopied, { title: toastTitles.success })
}

function confirmLeave() {
  confirmTitle.value = 'Sair do Grupo'
  confirmMessage.value = 'Tem certeza que deseja sair do grupo? Se for o único membro, o grupo será excluído.'
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Sair'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = handleLeave
  confirmVisible.value = true
}

function confirmDeleteGroup() {
  confirmTitle.value = 'Excluir Grupo?'
  confirmMessage.value = 'Todos os membros serão removidos e as despesas permanecerão vinculadas apenas aos criadores.'
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Excluir'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = handleDeleteGroup
  confirmVisible.value = true
}

function confirmExpel(member) {
  confirmTitle.value = 'Expulsar Membro'
  confirmMessage.value = `Remover ${member.user.first_name || member.user.username} do grupo?`
  confirmDanger.value = true
  confirmAcceptLabel.value = 'Remover'
  confirmRejectLabel.value = 'Cancelar'
  confirmOnAccept = () => handleExpel(member)
  confirmVisible.value = true
}

async function onConfirmAccept() {
  confirmVisible.value = false
  if (confirmOnAccept) {
    await confirmOnAccept()
    confirmOnAccept = null
  }
}
</script>

<style scoped>
.family-page {
  max-width: 1200px;
  margin: 0 auto;
}

.family-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
  color: #9ca3af;
}

.family-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 16px 0;
}

.divider {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 300px;
  gap: 0.75rem;
  color: #6b7280;
  font-size: 0.875rem;
  margin: 8px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #374151;
}

.family-form,
.family-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.family-title {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-field label {
  color: #9ca3af;
  font-size: 0.875rem;
  font-weight: 500;
}

.required {
  color: #ef4444;
}

.native-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.5rem;
  color: #ffffff;
  font-size: 0.9375rem;
  outline: none;
  transition: border-color 0.2s;
}

.native-input:focus {
  border-color: #60A637;
}

.native-input::placeholder {
  color: #6b7280;
}

.code-input {
  font-family: monospace;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 1.125rem;
}

.cancel-link {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.5rem;
  align-self: center;
}

.cancel-link:hover {
  color: #d1d5db;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-label {
  color: #9ca3af;
  font-size: 0.875rem;
  font-weight: 500;
}

.code-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 0.5rem;
}

.code-text {
  font-family: monospace;
  font-size: 1.25rem;
  letter-spacing: 0.15em;
  color: #60A637;
  font-weight: 600;
}

.expiration-text {
  color: #6b7280;
  font-size: 0.75rem;
  margin: 0.25rem 0 0 0;
}

.expiration-text.expiring {
  color: #f59e0b;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.badge {
  font-size: 0.625rem;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.admin {
  background: #60A637;
  color: #ffffff;
}

.badge.you {
  background: #374151;
  color: #9ca3af;
}

.actions {
  padding-top: 0.5rem;
  border-top: 1px solid #374151;
}

.mt-2 {
  margin-top: 0.5rem;
}

.w-full {
  width: 100%;
}

/* Primary buttons matching 'Adicionar Primeiro Gasto' pattern */
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
  align-self: center;
}

.btn-primary:hover {
  filter: brightness(1.1);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-primary-outlined {
  background: transparent;
  color: white;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  align-self: center;
}

.btn-primary-outlined::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 12px;
  padding: 1.5px;
  background: linear-gradient(180deg, #60A637, #4C8932);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.btn-primary-outlined:hover {
  background: rgba(96, 166, 55, 0.08);
  transform: translateY(-2px);
}

.btn-sm {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 10px;
}

.btn-danger-outlined {
  background: transparent;
  color: #ef4444;
  border: 2px solid #ef4444;
  border-radius: 12px;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
}

.btn-danger-outlined:hover {
  background: rgba(239, 68, 68, 0.1);
  transform: translateY(-2px);
}

</style>
