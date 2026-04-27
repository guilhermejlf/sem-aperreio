<template>
  <form @submit.prevent="handleLogin" class="auth-form">
    <div class="form-group">
      <label class="form-label">Usuário</label>
      <input
        v-model="username" 
        placeholder="seu_usuario"
        class="form-input"
        :disabled="loading"
      />
    </div>

    <div class="form-group">
      <label class="form-label">Senha</label>
      <input
        v-model="password" 
        type="password"
        placeholder="••••••"
        class="form-input"
        :disabled="loading"
      />
    </div>

    <div v-if="error" class="form-error">{{ error }}</div>

    <Button 
      type="submit"
      :label="loading ? 'Entrando...' : 'Entrar'"
      class="btn-submit"
      :disabled="loading || !username || !password"
    />
  </form>
</template>

<script>
import Button from 'primevue/button'
import { API_ENDPOINTS, apiRequest, setTokens } from '../config/api.js'

export default {
  components: {
    Button
  },

  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null
    }
  },

  methods: {
    async handleLogin() {
      this.loading = true
      this.error = null

      try {
        const data = await apiRequest(API_ENDPOINTS.AUTH_LOGIN, {
          method: 'POST',
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })

        if (data.access && data.refresh) {
          setTokens(data.access, data.refresh)
          this.$emit('success')
        } else {
          this.error = 'Resposta inesperada do servidor'
        }
      } catch (error) {
        this.error = error.message || 'Erro ao fazer login. Verifique suas credenciais.'
        console.error('Login error:', error)
      } finally {
        this.loading = false
      }
    }
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
  gap: 6px;
}

.form-label {
  color: #e5e7eb;
  font-weight: 500;
  font-size: 13px;
}

.form-input {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: white !important;
  padding: 12px;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s ease;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: #22c55e !important;
  background: rgba(255, 255, 255, 0.05) !important;
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
  background: linear-gradient(135deg, #22c55e, #16a34a) !important;
  border: none !important;
  padding: 14px !important;
  border-radius: 8px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  color: white !important;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.btn-submit:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
