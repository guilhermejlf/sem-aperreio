<template>
  <form @submit.prevent="handleRegister" class="auth-form">
    <div class="form-group">
      <label class="form-label">Nome</label>
      <div class="input-wrapper">
        <i class="pi pi-user input-icon"></i>
        <input
          v-model="first_name"
          placeholder="Seu nome"
          class="form-input"
          :disabled="loading"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">E-mail</label>
      <div class="input-wrapper">
        <i class="pi pi-envelope input-icon"></i>
        <input
          v-model="email"
          type="email"
          placeholder="seu@email.com"
          class="form-input"
          :disabled="loading"
        />
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">Usuário</label>
      <div class="input-wrapper">
        <i class="pi pi-at input-icon"></i>
        <input
          v-model="username"
          placeholder="seu_usuario"
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
          placeholder="Mínimo 8 caracteres"
          class="form-input"
          :disabled="loading"
        />
        <button type="button" class="password-toggle" @click="showPassword = !showPassword" tabindex="-1">
          <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
        </button>
      </div>
      <!-- Password strength indicator -->
      <div class="password-strength" v-if="password">
        <div class="strength-bar">
          <div class="strength-fill" :style="{ width: strengthPercent + '%', background: strengthColor }"></div>
        </div>
        <span class="strength-text" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
      </div>
      <div class="password-rules">
        <div :class="['rule-item', { valid: hasMinLength }]">
          <i :class="hasMinLength ? 'pi pi-check' : 'pi pi-circle'" class="rule-icon"></i>
          <span>8 caracteres</span>
        </div>
        <div :class="['rule-item', { valid: hasUppercase }]">
          <i :class="hasUppercase ? 'pi pi-check' : 'pi pi-circle'" class="rule-icon"></i>
          <span>Letra maiúscula</span>
        </div>
        <div :class="['rule-item', { valid: hasLowercase }]">
          <i :class="hasLowercase ? 'pi pi-check' : 'pi pi-circle'" class="rule-icon"></i>
          <span>Letra minúscula</span>
        </div>
        <div :class="['rule-item', { valid: hasNumber }]">
          <i :class="hasNumber ? 'pi pi-check' : 'pi pi-circle'" class="rule-icon"></i>
          <span>Número</span>
        </div>
        <div :class="['rule-item', { valid: hasSpecial }]">
          <i :class="hasSpecial ? 'pi pi-check' : 'pi pi-circle'" class="rule-icon"></i>
          <span>Caractere especial</span>
        </div>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label">Confirmar senha</label>
      <div class="input-wrapper">
        <i class="pi pi-lock input-icon"></i>
        <input
          v-model="password_confirm"
          :type="showPasswordConfirm ? 'text' : 'password'"
          placeholder="Repita a senha"
          class="form-input"
          :disabled="loading"
        />
        <button type="button" class="password-toggle" @click="showPasswordConfirm = !showPasswordConfirm" tabindex="-1">
          <i :class="showPasswordConfirm ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
        </button>
      </div>
      <p v-if="password && password_confirm && password !== password_confirm" class="password-hint">Repita a senha para confirmar sua conta.</p>
      <p v-else-if="password && password_confirm && password === password_confirm" class="password-hint valid">Senhas combinam 👍</p>
    </div>

    <div v-if="error" class="form-error">{{ error }}</div>
    <div v-if="success" class="form-success">{{ success }}</div>

    <Button 
      type="submit"
      :label="loading ? 'Criando conta...' : 'Criar Conta'"
      class="btn-submit"
      :disabled="loading || !formValido"
    />
  </form>
</template>

<script setup>
import { ref, computed } from 'vue'
import Button from 'primevue/button'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'
import { toastStore } from '../stores/toast.store.js'

const emit = defineEmits(['registered'])

const first_name = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const password_confirm = ref('')
const showPassword = ref(false)
const showPasswordConfirm = ref(false)
const loading = ref(false)
const error = ref(null)
const success = ref(null)

const hasMinLength = computed(() => password.value.length >= 8)
const hasUppercase = computed(() => /[A-Z]/.test(password.value))
const hasLowercase = computed(() => /[a-z]/.test(password.value))
const hasNumber = computed(() => /[0-9]/.test(password.value))
const hasSpecial = computed(() => /[@!#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password.value))
const strengthScore = computed(() => {
  let score = 0
  if (hasMinLength.value) score++
  if (hasUppercase.value) score++
  if (hasLowercase.value) score++
  if (hasNumber.value) score++
  if (hasSpecial.value) score++
  return score
})
const strengthPercent = computed(() => (strengthScore.value / 5) * 100)
const strengthColor = computed(() => {
  const colors = ['#ef4444', '#f97316', '#eab308', '#60A637', '#60A637']
  return colors[strengthScore.value - 1] || '#ef4444'
})
const strengthLabel = computed(() => {
  const labels = ['Senha fraca 👀', 'Tá melhorando 🙂', 'Quase lá 😄', 'Agora ficou boa 😄', 'Agora ficou segura 😄']
  return labels[strengthScore.value - 1] || 'Senha fraca 👀'
})
const formValido = computed(() =>
  first_name.value &&
  email.value &&
  username.value &&
  password.value &&
  hasMinLength.value &&
  hasUppercase.value &&
  hasLowercase.value &&
  hasNumber.value &&
  hasSpecial.value &&
  password.value === password_confirm.value
)

function validarLocal() {
  if (!first_name.value) return 'Informe seu nome'
  if (!email.value) return 'Informe seu e-mail'
  if (!username.value) return 'Informe um nome de usuário'
  if (!password.value) return 'Informe uma senha'
  if (!hasMinLength.value) return 'A senha deve ter pelo menos 8 caracteres'
  if (!hasUppercase.value) return 'A senha deve conter uma letra maiúscula'
  if (!hasLowercase.value) return 'A senha deve conter uma letra minúscula'
  if (!hasNumber.value) return 'A senha deve conter um número'
  if (!hasSpecial.value) return 'A senha deve conter um caractere especial'
  if (password.value !== password_confirm.value) return 'As senhas não coincidem'
  return null
}

async function handleRegister() {
  loading.value = true
  error.value = null
  success.value = null

  const erroValidacao = validarLocal()
  if (erroValidacao) {
    toastStore.warning(erroValidacao)
    loading.value = false
    return
  }

  try {
    await apiRequest(API_ENDPOINTS.AUTH_REGISTER, {
      method: 'POST',
      body: JSON.stringify({
        first_name: first_name.value,
        email: email.value,
        username: username.value,
        password: password.value,
        password2: password_confirm.value
      })
    })

    emit('registered', { email: email.value })
  } catch (err) {
    toastStore.error(err.message || 'Erro ao criar conta. Tente novamente.')
    console.error('Register error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
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

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
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

.form-error {
  color: #ef4444;
  font-size: 14px;
  text-align: center;
}

.form-success {
  color: #60A637;
  font-size: 14px;
  text-align: center;
}

.password-strength {
  margin-top: 10px;
}

.strength-bar {
  height: 3px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.strength-text {
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
}

.password-rules {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 16px;
  margin: 10px 0 0 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.rule-item.valid {
  color: rgba(96, 166, 55, 0.75);
}

.rule-icon {
  font-size: 9px;
}

.password-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  margin: 6px 0 0;
}

.password-hint.valid {
  color: rgba(96, 166, 55, 0.7);
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
