<template>
  <Teleport to="body">
    <!-- Overlay backdrop -->
    <Transition name="fade">
      <div
        v-if="visible"
        class="ai-overlay"
        @click="close"
      />
    </Transition>

    <!-- Drawer -->
    <Transition name="slide">
      <div v-if="visible" class="ai-drawer" :class="{ 'ai-drawer--mobile': isMobile }">
        <ContextualTooltip
          v-if="showBeneTooltip"
          text="Posso registrar gastos e receitas por mensagem 😄"
          @dismiss="dismissBeneTooltip"
        />
        <!-- Header -->
        <div class="ai-header">
          <div class="ai-header-info">
            <div class="ai-avatar">
              <BeneAvatar size="small" :breathing="false" />
            </div>
            <div>
              <h3 class="ai-title">Seu Bené</h3>
              <span class="ai-subtitle">Copiloto financeiro</span>
            </div>
          </div>
          <button class="ai-close" @click="close">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <!-- Messages -->
        <div ref="messagesContainer" class="ai-messages">
          <div class="ai-welcome" v-if="messages.length === 0">
            <div class="ai-welcome-avatar">
              <BeneAvatar size="medium" :breathing="true" />
            </div>
            <p class="ai-welcome-text">
              Bora organizar essas contas? 😄<br>
              <span class="ai-welcome-examples">
                Pode falar naturalmente. Eu interpreto e organizo pra você.
              </span>
              <span class="ai-welcome-hint">
                Se faltar alguma informação eu te pergunto 😄
              </span>
            </p>
            <div class="ai-suggestions">
              <button
                v-for="s in quickSuggestions"
                :key="s"
                class="ai-suggestion-chip"
                @click="send(s)"
              >
                {{ s }}
              </button>
            </div>
          </div>

          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="ai-message"
            :class="{ 'ai-message--user': msg.role === 'user', 'ai-message--ai': msg.role === 'ai' }"
          >
            <div class="ai-bubble">
              <p v-if="msg.text">{{ msg.text }}</p>

              <!-- Suggestion chips -->
              <div v-if="msg.suggestions && msg.suggestions.length" class="ai-suggestions-inline">
                <button
                  v-for="s in msg.suggestions"
                  :key="s"
                  class="ai-suggestion-chip"
                  @click="send(s)"
                >
                  {{ s }}
                </button>
              </div>

              <!-- Confirmation card -->
              <div v-if="msg.confirmation" class="ai-confirm-card">
                <div class="ai-confirm-data">
                  <div class="ai-confirm-row">
                    <span class="ai-confirm-label">Tipo</span>
                    <span class="ai-confirm-value">{{ msg.confirmation.intent === 'add_expense' ? 'Despesa' : 'Receita' }}</span>
                  </div>
                  <div class="ai-confirm-row">
                    <span class="ai-confirm-label">Valor</span>
                    <span class="ai-confirm-value ai-confirm-value--highlight">{{ formatarValor(msg.confirmation.data.valor) }}</span>
                  </div>
                  <div v-if="msg.confirmation.data.categoria" class="ai-confirm-row">
                    <span class="ai-confirm-label">Categoria</span>
                    <span class="ai-confirm-value">{{ getCategoriaLabel(msg.confirmation.data.categoria) }}</span>
                  </div>
                  <div v-if="msg.confirmation.data.descricao" class="ai-confirm-row">
                    <span class="ai-confirm-label">Descrição</span>
                    <span class="ai-confirm-value">{{ msg.confirmation.data.descricao }}</span>
                  </div>
                </div>
                <div class="ai-confirm-actions">
                  <button
                    class="ai-btn ai-btn--cancel"
                    :disabled="msg.processing"
                    title="Cancelar"
                    @click="cancelAction(index)"
                  >
                    <i class="pi pi-times"></i>
                  </button>
                  <button
                    class="ai-btn ai-btn--edit"
                    :disabled="msg.processing"
                    title="Editar"
                    @click="editAction(msg, index)"
                  >
                    <i class="pi pi-pencil"></i>
                  </button>
                  <button
                    class="ai-btn ai-btn--confirm"
                    :disabled="msg.processing"
                    :title="msg.processing ? 'Salvando...' : 'Confirmar'"
                    @click="confirmAction(msg, index)"
                  >
                    <i class="pi pi-check"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="loading" class="ai-message ai-message--ai">
            <div class="ai-bubble ai-bubble--typing">
              <span class="ai-typing-dot"></span>
              <span class="ai-typing-dot"></span>
              <span class="ai-typing-dot"></span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="ai-input-area">
          <div class="ai-input-wrapper">
            <input
              ref="inputRef"
              v-model="input"
              type="text"
              placeholder="Digite uma mensagem..."
              class="ai-input"
              @keydown.enter.prevent="send"
              :disabled="loading"
            />
            <button
              class="ai-send"
              :disabled="!input.trim() || loading"
              @click="send"
            >
              <i class="pi pi-send"></i>
            </button>
          </div>
          <p class="ai-disclaimer">Só interpreto e sugiro. Nada é salvo sem você confirmar.</p>
        </div>
      </div>
    </Transition>

    <!-- FAB -->
    <Transition name="scale">
      <button
        v-if="!visible && !hideFab"
        class="ai-fab"
        @click="open"
        title="Assistente Financeiro"
      >
        <i class="pi pi-comments"></i>
      </button>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import ContextualTooltip from './onboarding/ContextualTooltip.vue'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'
import BeneAvatar from './BeneAvatar.vue'

const props = defineProps({
  hideFab: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['saved', 'edit-expense', 'edit-income'])

const visible = ref(false)
const showBeneTooltip = ref(false)

async function fetchOnboarding() {
  try {
    const data = await apiRequest(API_ENDPOINTS.ONBOARDING)
    showBeneTooltip.value = !data.seen_bene_tooltip
  } catch (err) {
    showBeneTooltip.value = false
  }
}

async function dismissBeneTooltip() {
  showBeneTooltip.value = false
  try {
    await apiRequest(API_ENDPOINTS.ONBOARDING, {
      method: 'POST',
      body: JSON.stringify({ action: 'dismiss_tooltip', tooltip: 'bene' })
    })
  } catch (e) {}
}
const input = ref('')
const loading = ref(false)
const messages = ref([])
const isMobile = ref(false)
const sessionContext = ref({
  awaiting_field: null,
  partial_data: {}
})
const quickSuggestions = ref([
  'Uber 25',
  'Feira 320',
  'Paguei internet 140',
  'Recebi salário 5 mil'
])
const inputRef = ref(null)
const messagesContainer = ref(null)

onMounted(() => {
  isMobile.value = window.innerWidth < 768
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

function handleResize() {
  isMobile.value = window.innerWidth < 768
}

function open() {
  visible.value = true
  fetchOnboarding()
  nextTick(() => {
    inputRef.value?.focus()
    scrollToBottom()
  })
}

function close() {
  visible.value = false
}

function scrollToBottom() {
  nextTick(() => {
    const container = messagesContainer.value
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  })
}

async function send(suggestionText = null) {
  const text = (typeof suggestionText === 'string' ? suggestionText : input.value).trim()
  if (!text || loading.value) return

  input.value = ''

  messages.value.push({ role: 'user', text })
  loading.value = true
  scrollToBottom()

  try {
    const history = messages.value
      .filter(m => m.role === 'user' || m.role === 'ai')
      .slice(-10)
      .map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.text || ''
      }))

    const payload = {
      message: text,
      context: sessionContext.value,
      conversation_history: history
    }

    const response = await apiRequest(API_ENDPOINTS.AI_CHAT, {
      method: 'POST',
      body: JSON.stringify(payload)
    })

    if (response.awaiting_field) {
      sessionContext.value = {
        awaiting_field: response.awaiting_field,
        partial_data: response.partial_data || {}
      }
    } else {
      sessionContext.value = {
        awaiting_field: null,
        partial_data: {}
      }
    }

    messages.value.push({
      role: 'ai',
      text: response.message,
      confirmation: response.confirmation_required ? response : null,
      processing: false
    })
  } catch (err) {
    messages.value.push({
      role: 'ai',
      text: 'Opa, deu um ruim aqui. Tenta de novo daqui a pouco?',
      confirmation: null
    })
    sessionContext.value = {
      awaiting_field: null,
      partial_data: {}
    }
  } finally {
    loading.value = false
    scrollToBottom()
    nextTick(() => {
      inputRef.value?.focus()
    })
  }
}

async function confirmAction(msg, index) {
  const confirmation = msg.confirmation
  if (!confirmation || !confirmation.data) return

  msg.processing = true

  try {
    if (confirmation.intent === 'add_expense') {
      await apiRequest(API_ENDPOINTS.GASTOS_LIST, {
        method: 'POST',
        body: JSON.stringify({
          valor: confirmation.data.valor,
          categoria: confirmation.data.categoria,
          descricao: confirmation.data.descricao,
          data: confirmation.data.data,
          data_competencia: confirmation.data.data,
          pago: false
        })
      })
    } else if (confirmation.intent === 'add_income') {
      await apiRequest(API_ENDPOINTS.RECEITAS_LIST, {
        method: 'POST',
        body: JSON.stringify({
          valor: confirmation.data.valor,
          descricao: confirmation.data.descricao,
          data: confirmation.data.data,
          data_competencia: confirmation.data.data
        })
      })
    }

    messages.value[index] = {
      role: 'ai',
      text: `${msg.text} \u2713 Pronto, salvo!`,
      confirmation: null,
      processing: false
    }

    sessionContext.value = {
      awaiting_field: null,
      partial_data: {}
    }

    messages.value.push({
      role: 'ai',
      text: 'Mais alguma coisa pra registrar? 😄',
      confirmation: null,
      suggestions: ['+ Mercado', '+ Transporte', '+ Restaurante', '+ Receita', 'Nenhum']
    })

    emit('saved')
  } catch (err) {
    messages.value[index] = {
      role: 'ai',
      text: `${msg.text} \u2717 Erro ao salvar. Tente novamente pelo formulário.`,
      confirmation: null,
      processing: false
    }
  } finally {
    scrollToBottom()
    nextTick(() => {
      inputRef.value?.focus()
    })
  }
}

function editAction(msg, index) {
  const confirmation = msg.confirmation
  if (!confirmation || !confirmation.data) return

  if (confirmation.intent === 'add_income') {
    emit('edit-income', {
      valor: confirmation.data.valor,
      descricao: confirmation.data.descricao,
      data: confirmation.data.data
    })
  } else {
    emit('edit-expense', {
      valor: confirmation.data.valor,
      categoria: confirmation.data.categoria,
      descricao: confirmation.data.descricao,
      data: confirmation.data.data
    })
  }

  close()

  messages.value[index] = {
    role: 'ai',
    text: 'Abri o formulário pra você revisar antes de salvar.',
    confirmation: null
  }
}

function cancelAction(index) {
  messages.value[index] = {
    role: 'ai',
    text: 'Beleza, cancelado. Manda outra quando quiser.',
    confirmation: null
  }
  sessionContext.value = {
    awaiting_field: null,
    partial_data: {}
  }
  scrollToBottom()
}

function formatarValor(valor) {
  return parseFloat(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function getCategoriaLabel(categoriaValue) {
  const categorias = {
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
  return categorias[categoriaValue] || categoriaValue
}

defineExpose({ open })
</script>

<style scoped>
.ai-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 1998;
}

.ai-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 420px;
  max-width: 100vw;
  background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
  border-left: 1px solid rgba(255, 255, 255, 0.08);
  z-index: 1999;
  display: flex;
  flex-direction: column;
  box-shadow: -20px 0 60px rgba(0, 0, 0, 0.5);
}

.ai-drawer--mobile {
  width: 100vw;
  border-left: none;
}

/* Header */
.ai-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
}

.ai-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(96, 166, 55, 0.08);
  transition: box-shadow 0.3s ease;
}

.ai-header-info:hover .ai-avatar {
  box-shadow: 0 0 28px rgba(96, 166, 55, 0.14);
}

.ai-title {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: white;
  letter-spacing: -0.2px;
}

.ai-subtitle {
  font-size: 11px;
  color: #64748b;
  font-weight: 400;
}

.ai-close {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
  transition: all 0.2s;
}

.ai-close:hover {
  color: white;
  background: rgba(255, 255, 255, 0.08);
}

/* Messages */
.ai-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ai-welcome {
  text-align: center;
  padding: 40px 20px;
  color: #94a3b8;
}

.ai-welcome-avatar {
  margin-bottom: 16px;
  opacity: 0.9;
}

.ai-welcome-hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #64748b;
}

.ai-welcome-text {
  font-size: 14px;
  line-height: 1.6;
}

.ai-welcome-examples {
  display: block;
  margin-top: 8px;
  font-size: 13px;
  color: #64748b;
}

.ai-welcome-examples em {
  color: #a78bfa;
  font-style: normal;
}

.ai-message {
  display: flex;
}

.ai-message--user {
  justify-content: flex-end;
}

.ai-message--ai {
  justify-content: flex-start;
}

.ai-bubble {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.ai-message--user .ai-bubble {
  background: linear-gradient(135deg, #60A637, #4C8932);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message--ai .ai-bubble {
  background: rgba(30, 41, 59, 0.8);
  color: #e2e8f0;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom-left-radius: 4px;
}

/* Typing indicator */
.ai-bubble--typing {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 12px 16px;
  min-width: 60px;
}

.ai-typing-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #a78bfa;
  animation: ai-typing-bounce 1.4s infinite ease-in-out both;
}

.ai-typing-dot:nth-child(1) { animation-delay: -0.32s; }
.ai-typing-dot:nth-child(2) { animation-delay: -0.16s; }
.ai-typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes ai-typing-bounce {
  0%, 80%, 100% { transform: scale(0.5); opacity: 0.3; }
  40% { transform: scale(1); opacity: 1; }
}

/* Suggestions */
.ai-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  justify-content: center;
}

.ai-suggestion-chip {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #94a3b8;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-suggestion-chip:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  border-color: rgba(255, 255, 255, 0.15);
}

/* Confirmation card */
.ai-confirm-card {
  margin-top: 10px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 14px;
}

.ai-confirm-data {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}

.ai-confirm-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.ai-confirm-label {
  color: #94a3b8;
}

.ai-confirm-value {
  color: white;
  font-weight: 500;
}

.ai-confirm-value--highlight {
  color: #60A637;
  font-size: 15px;
  font-weight: 600;
}

.ai-confirm-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.ai-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.03);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.ai-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ai-btn--confirm {
  color: #60A637;
}

.ai-btn--confirm:hover:not(:disabled) {
  background: rgba(96, 166, 55, 0.1);
  border-color: rgba(96, 166, 55, 0.25);
}

.ai-btn--edit {
  color: #3b82f6;
}

.ai-btn--edit:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.25);
}

.ai-btn--cancel {
  color: #ef4444;
}

.ai-btn--cancel:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.25);
}

/* Input area */
.ai-input-area {
  padding: 16px 20px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
}

.ai-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(2, 6, 23, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 4px 4px 4px 16px;
  transition: border-color 0.2s;
}

.ai-input-wrapper:focus-within {
  border-color: rgba(167, 139, 250, 0.4);
}

.ai-input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: white;
  font-size: 14px;
  padding: 10px 0;
}

.ai-input::placeholder {
  color: #64748b;
}

.ai-send {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #a78bfa, #60A637);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.ai-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ai-send:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(167, 139, 250, 0.3);
}

.ai-disclaimer {
  margin: 8px 0 0;
  font-size: 11px;
  color: #475569;
  text-align: center;
}

/* FAB */
.ai-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #a78bfa, #60A637);
  color: white;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1997;
  box-shadow: 0 8px 30px rgba(167, 139, 250, 0.35);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.ai-fab:hover {
  transform: scale(1.1) rotate(-4deg);
  box-shadow: 0 12px 40px rgba(167, 139, 250, 0.45);
}

.ai-fab:active {
  transform: scale(0.95);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.6);
}

/* Scrollbar */
.ai-messages::-webkit-scrollbar {
  width: 4px;
}

.ai-messages::-webkit-scrollbar-track {
  background: transparent;
}

.ai-messages::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.ai-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
