<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h3>Redefinir senha</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div v-if="success" class="modal-success">
        <i class="pi pi-check-circle" style="font-size: 2rem; color: #60A637;"></i>
        <p>{{ success }}</p>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="modal-form">
        <p class="modal-text">Informe seu email e enviaremos um link para redefinir sua senha.</p>

        <div class="form-group">
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

        <Button
          type="submit"
          :label="loading ? 'Enviando...' : 'Enviar link'"
          class="btn-submit"
          :disabled="loading || !email"
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
      email: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async handleSubmit() {
      this.loading = true
      this.error = null
      this.success = null

      try {
        const data = await apiRequest(API_ENDPOINTS.AUTH_PASSWORD_RESET, {
          method: 'POST',
          body: JSON.stringify({ email: this.email })
        })
        this.success = data.mensagem || 'Se o email estiver cadastrado, você receberá um link de redefinição.'
      } catch (error) {
        this.error = error.message || 'Erro ao solicitar redefinição. Tente novamente.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-card {
  background: #0b1220;
  border-radius: 16px;
  padding: 28px;
  width: 100%;
  max-width: 380px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  color: #e2e8f0;
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: white;
}

.modal-text {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 16px;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
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

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
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
  margin-top: 12px;
  font-size: 14px;
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
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
