<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <i class="pi pi-lock auth-icon"></i>
        <h1 class="auth-title">Redefinir senha</h1>
      </div>

      <div v-if="loading" class="loading-state">
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem; color: #60A637;"></i>
        <p>Processando...</p>
      </div>

      <div v-else-if="success" class="success-state">
        <i class="pi pi-check-circle" style="font-size: 3rem; color: #60A637;"></i>
        <h2>Senha redefinida!</h2>
        <p>{{ success }}</p>
        <button class="btn-primary" @click="goToLogin">Ir para login</button>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label class="form-label">Nova senha</label>
          <input
            v-model="password"
            type="password"
            placeholder="Nova senha forte"
            class="form-input"
            :disabled="loading"
          />
          <ul class="password-rules">
            <li :class="{ valid: hasMinLength }">Mínimo 8 caracteres</li>
            <li :class="{ valid: hasUppercase }">1 letra maiúscula</li>
            <li :class="{ valid: hasLowercase }">1 letra minúscula</li>
            <li :class="{ valid: hasNumber }">1 número</li>
            <li :class="{ valid: hasSpecial }">1 caractere especial</li>
          </ul>
        </div>

        <div class="form-group">
          <label class="form-label">Confirmar nova senha</label>
          <input
            v-model="password_confirm"
            type="password"
            placeholder="Repita a nova senha"
            class="form-input"
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="form-error">{{ error }}</div>

        <Button
          type="submit"
          :label="loading ? 'Redefinindo...' : 'Redefinir senha'"
          class="btn-submit"
          :disabled="loading || !formValido"
        />
      </form>
    </div>
  </div>
</template>

<script>
import Button from 'primevue/button'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'

export default {
  components: { Button },
  data() {
    return {
      password: '',
      password_confirm: '',
      loading: false,
      error: null,
      success: null,
      token: null
    }
  },
  computed: {
    hasMinLength() { return this.password.length >= 8 },
    hasUppercase() { return /[A-Z]/.test(this.password) },
    hasLowercase() { return /[a-z]/.test(this.password) },
    hasNumber() { return /[0-9]/.test(this.password) },
    hasSpecial() { return /[@!#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(this.password) },
    formValido() {
      return this.hasMinLength && this.hasUppercase && this.hasLowercase &&
             this.hasNumber && this.hasSpecial && this.password === this.password_confirm
    }
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search)
    this.token = urlParams.get('token')
    if (!this.token) {
      this.error = 'Link inválido. Solicite uma nova redefinição de senha.'
    }
  },
  methods: {
    async handleSubmit() {
      if (!this.token) return
      this.loading = true
      this.error = null

      try {
        const data = await apiRequest(API_ENDPOINTS.AUTH_PASSWORD_RESET_CONFIRM, {
          method: 'POST',
          body: JSON.stringify({
            token: this.token,
            new_password: this.password
          })
        })
        this.success = data.mensagem || 'Senha redefinida com sucesso!'
      } catch (error) {
        this.error = error.message || 'Erro ao redefinir senha. O link pode ter expirado.'
      } finally {
        this.loading = false
      }
    },
    goToLogin() {
      window.location.href = '/'
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at top, #0f172a, #020617);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: #0b1220;
  padding: 32px 28px;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.05);
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-icon {
  font-size: 2.5rem;
  color: #60A637;
  margin-bottom: 12px;
}

.auth-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(90deg, #a78bfa, #60A637);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.loading-state,
.success-state {
  text-align: center;
  padding: 20px 0;
}

.success-state h2 {
  color: #60A637;
  margin: 16px 0 8px;
}

.success-state p {
  color: #94a3b8;
  margin-bottom: 20px;
}

.btn-primary {
  background: linear-gradient(135deg, #60A637, #4C8932);
  border: none;
  padding: 14px 28px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  cursor: pointer;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  color: #e5e7eb;
  font-weight: 500;
  font-size: 13px;
}

.form-input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: white;
  padding: 12px;
  border-radius: 8px;
  font-size: 15px;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: #60A637;
  background: rgba(255, 255, 255, 0.05);
}

.password-rules {
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
}

.password-rules li {
  padding: 2px 0;
}

.password-rules li.valid {
  color: #60A637;
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
  border-radius: 8px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: white !important;
  cursor: pointer;
  margin-top: 8px;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
