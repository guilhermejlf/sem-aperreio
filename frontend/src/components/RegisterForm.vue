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
        placeholder="Mínimo 8 caracteres"
        class="form-input"
        :disabled="loading"
      />
      <!-- Password strength indicator -->
      <div class="password-strength" v-if="password">
        <div class="strength-bar">
          <div class="strength-fill" :style="{ width: strengthPercent + '%', background: strengthColor }"></div>
        </div>
        <span class="strength-text" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
      </div>
      <ul class="password-rules">
        <li :class="{ valid: hasMinLength }">Mínimo 8 caracteres</li>
        <li :class="{ valid: hasUppercase }">1 letra maiúscula</li>
        <li :class="{ valid: hasLowercase }">1 letra minúscula</li>
        <li :class="{ valid: hasNumber }">1 número</li>
        <li :class="{ valid: hasSpecial }">1 caractere especial</li>
      </ul>
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
    <div v-if="success" class="form-success">{{ success }}</div>

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
      error: null,
      success: null
    }
  },

  computed: {
    hasMinLength() {
      return this.password.length >= 8
    },
    hasUppercase() {
      return /[A-Z]/.test(this.password)
    },
    hasLowercase() {
      return /[a-z]/.test(this.password)
    },
    hasNumber() {
      return /[0-9]/.test(this.password)
    },
    hasSpecial() {
      return /[@!#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(this.password)
    },
    strengthScore() {
      let score = 0
      if (this.hasMinLength) score++
      if (this.hasUppercase) score++
      if (this.hasLowercase) score++
      if (this.hasNumber) score++
      if (this.hasSpecial) score++
      return score
    },
    strengthPercent() {
      return (this.strengthScore / 5) * 100
    },
    strengthColor() {
      const colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e']
      return colors[this.strengthScore - 1] || '#ef4444'
    },
    strengthLabel() {
      const labels = ['Muito fraca', 'Fraca', 'Média', 'Boa', 'Forte']
      return labels[this.strengthScore - 1] || 'Muito fraca'
    },
    formValido() {
      return this.first_name && 
             this.email && 
             this.username && 
             this.password && 
             this.hasMinLength &&
             this.hasUppercase &&
             this.hasLowercase &&
             this.hasNumber &&
             this.hasSpecial &&
             this.password === this.password_confirm
    }
  },

  methods: {
    validarLocal() {
      if (!this.first_name) return 'Informe seu nome'
      if (!this.email) return 'Informe seu e-mail'
      if (!this.username) return 'Informe um nome de usuário'
      if (!this.password) return 'Informe uma senha'
      if (!this.hasMinLength) return 'A senha deve ter pelo menos 8 caracteres'
      if (!this.hasUppercase) return 'A senha deve conter uma letra maiúscula'
      if (!this.hasLowercase) return 'A senha deve conter uma letra minúscula'
      if (!this.hasNumber) return 'A senha deve conter um número'
      if (!this.hasSpecial) return 'A senha deve conter um caractere especial'
      if (this.password !== this.password_confirm) return 'As senhas não coincidem'
      return null
    },

    async handleRegister() {
      this.loading = true
      this.error = null
      this.success = null

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
            password: this.password,
            password2: this.password_confirm
          })
        })

        this.success = 'Conta criada! Verifique seu email para ativar sua conta antes de fazer login.'
        // Não faz login automático — usuário precisa verificar email
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

.form-success {
  color: #22c55e;
  font-size: 14px;
  text-align: center;
}

.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.strength-text {
  font-size: 12px;
  margin-top: 4px;
  display: block;
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
  transition: color 0.2s ease;
}

.password-rules li.valid {
  color: #22c55e;
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
