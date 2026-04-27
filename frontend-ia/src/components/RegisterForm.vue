<template>
  <form @submit.prevent="handleRegister" class="auth-form">
    <div class="form-group">
      <label class="form-label">Nome</label>
      <input
        v-model="first_name" 
        placeholder="Seu nome"
        class="form-input"
        :disabled="loading"
      />
    </div>

    <div class="form-group">
      <label class="form-label">E-mail</label>
      <input
        v-model="email" 
        type="email"
        placeholder="seu@email.com"
        class="form-input"
        :disabled="loading"
      />
    </div>

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
        placeholder="Mínimo 6 caracteres"
        class="form-input"
        :disabled="loading"
      />
    </div>

    <div class="form-group">
      <label class="form-label">Confirmar senha</label>
      <input
        v-model="password_confirm" 
        type="password"
        placeholder="Repita a senha"
        class="form-input"
        :disabled="loading"
      />
    </div>

    <div v-if="error" class="form-error">{{ error }}</div>

    <Button 
      type="submit"
      :label="loading ? 'Criando conta...' : 'Criar Conta'"
      class="btn-submit"
      :disabled="loading || !formValido"
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
      first_name: '',
      email: '',
      username: '',
      password: '',
      password_confirm: '',
      loading: false,
      error: null
    }
  },

  computed: {
    formValido() {
      return this.first_name && 
             this.email && 
             this.username && 
             this.password && 
             this.password.length >= 6 &&
             this.password === this.password_confirm
    }
  },

  methods: {
    validarLocal() {
      if (!this.first_name) return 'Informe seu nome'
      if (!this.email) return 'Informe seu e-mail'
      if (!this.username) return 'Informe um nome de usuário'
      if (!this.password) return 'Informe uma senha'
      if (this.password.length < 6) return 'A senha deve ter pelo menos 6 caracteres'
      if (this.password !== this.password_confirm) return 'As senhas não coincidem'
      return null
    },

    async handleRegister() {
      this.loading = true
      this.error = null

      const erroValidacao = this.validarLocal()
      if (erroValidacao) {
        this.error = erroValidacao
        this.loading = false
        return
      }

      try {
        // Cadastro
        await apiRequest(API_ENDPOINTS.AUTH_REGISTER, {
          method: 'POST',
          body: JSON.stringify({
            first_name: this.first_name,
            email: this.email,
            username: this.username,
            password: this.password
          })
        })

        // Login automático após cadastro
        const loginData = await apiRequest(API_ENDPOINTS.AUTH_LOGIN, {
          method: 'POST',
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })

        if (loginData.access && loginData.refresh) {
          setTokens(loginData.access, loginData.refresh)
          this.$emit('auth-success')
        } else {
          this.error = 'Conta criada, mas erro ao fazer login automático'
        }
      } catch (error) {
        this.error = error.message || 'Erro ao criar conta. Tente novamente.'
        console.error('Register error:', error)
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
  gap: 14px;
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
  margin-top: 4px;
}

.btn-submit:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
