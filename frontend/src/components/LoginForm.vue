<template>
  <form @submit.prevent="handleLogin" class="auth-form">
    <div class="form-group">
      <label class="form-label">Usuário ou Email</label>
      <div class="input-wrapper">
        <i class="pi pi-user input-icon"></i>
        <input
          v-model="identifier"
          placeholder="seu_usuario ou email@exemplo.com"
          class="form-input"
          :disabled="loading"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">Senha</label>
      <div class="input-wrapper">
        <i class="pi pi-lock input-icon"></i>
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="••••••"
          class="form-input"
          :disabled="loading"
        />
        <button
          type="button"
          class="password-toggle"
          @click="showPassword = !showPassword"
          tabindex="-1"
        >
          <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
        </button>
      </div>
    </div>

    <div v-if="error" class="form-error">{{ error }}</div>

    <Button 
      type="submit"
      :label="loading ? 'Entrando...' : 'Entrar'"
      class="btn-submit"
      :disabled="loading || !identifier || !password"
    />
  </form>
</template>

<script setup>
import { ref } from 'vue'
import Button from 'primevue/button'
import { API_ENDPOINTS, apiRequest, setTokens } from '../config/api.js'
import { toastStore } from '../stores/toast.store.js'

const emit = defineEmits(['success'])

const identifier = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref(null)
async function handleLogin() {
  loading.value = true
  error.value = null

  try {
    const data = await apiRequest(API_ENDPOINTS.AUTH_LOGIN, {
      method: 'POST',
      body: JSON.stringify({
        identifier: identifier.value,
        password: password.value
      })
    })

    if (data.access && data.refresh) {
      setTokens(data.access, data.refresh)
      toastStore.success('Bem-vindo de volta! 😄')
      emit('success')
    } else {
      toastStore.error('Resposta inesperada do servidor')
    }
  } catch (err) {
    const msg = err.message || ''
    if (msg.includes('Credenciais inválidas')) {
      error.value = 'Usuário/email ou senha incorretos.'
    } else {
      error.value = msg || 'Erro ao fazer login. Tente novamente.'
    }
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-label {
  color: #e5e7eb;
  font-weight: 500;
  font-size: 13px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: rgba(255,255,255,0.35);
  font-size: 14px;
  pointer-events: none;
  z-index: 1;
}

.form-input {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: white !important;
  padding: 12px 44px;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.25s ease;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: rgba(96,166,55,0.4) !important;
  background: rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 0 0 2px rgba(96,166,55,0.06), 0 0 12px rgba(96,166,55,0.04);
}

.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: rgba(255,255,255,0.35);
  cursor: pointer;
  font-size: 14px;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: rgba(255,255,255,0.7);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-error {
  color: #ef4444;
  font-size: 14px;
  text-align: center;
}

.btn-submit {
  width: 100%;
  background: linear-gradient(135deg, #60A637, #4C8932) !important;
  border: none !important;
  padding: 14px !important;
  border-radius: 14px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 8px;
  box-shadow: 0 4px 14px rgba(96,166,55,0.18);
}

.btn-submit:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

</style>
