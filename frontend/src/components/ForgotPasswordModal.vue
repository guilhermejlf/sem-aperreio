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
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 28px;
  width: min(480px, 90vw);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5);
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 22px;
  background: linear-gradient(90deg, #60A637, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #94a3b8;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
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
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  padding: 12px 14px;
  color: #e5e7eb;
  font-size: 15px;
  width: 100%;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #60A637;
  box-shadow: 0 0 0 3px rgba(96, 166, 55, 0.15);
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
  border-radius: 14px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  color: white !important;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(96, 166, 55, 0.18);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-submit:hover:not(:disabled) {
  filter: brightness(1.1);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
