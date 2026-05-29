<template>
  <ModalBase
    :visible="true"
    title="Redefinir"
    highlight="senha"
    subtitle="Informe seu email e enviaremos um link para redefinir sua senha."
    size="small"
    @close="emit('close')"
  >
    <div v-if="success" class="modal-success">
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="22" stroke="#60A637" stroke-width="2"/>
        <path d="M16 24L21 29L32 18" stroke="#60A637" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <p>{{ success }}</p>
    </div>

    <form v-else @submit.prevent="handleSubmit" class="modal-form">
      <div class="form-group">
        <label>Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="seu@email.com"
          class="form-input"
          :disabled="loading"
          required
        />
      </div>

      <div v-if="error" class="form-error">{{ error }}</div>
    </form>

    <template #footer>
      <button class="btn-secondary" @click="emit('close')">Cancelar</button>
      <button
        v-if="!success"
        class="btn-primary"
        :disabled="loading || !email"
        @click="handleSubmit"
      >
        {{ loading ? 'Enviando...' : 'Enviar link' }}
      </button>
    </template>
  </ModalBase>
</template>

<script setup>
import { ref } from 'vue'
import ModalBase from './ModalBase.vue'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'

const emit = defineEmits(['close'])

const email = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  success.value = null

  try {
    const data = await apiRequest(API_ENDPOINTS.AUTH_PASSWORD_RESET, {
      method: 'POST',
      body: JSON.stringify({ email: email.value })
    })
    success.value = data.mensagem || 'Se o email estiver cadastrado, você receberá um link de redefinição.'
  } catch (err) {
    error.value = err.message || 'Erro ao solicitar redefinição. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  display: block;
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

.form-error {
  color: #ef4444;
  font-size: 14px;
  text-align: center;
}

.modal-success {
  text-align: center;
  padding: 20px 0;
}

.modal-success p {
  color: #60A637;
  margin-top: 16px;
  font-size: 15px;
  font-weight: 500;
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
</style>
