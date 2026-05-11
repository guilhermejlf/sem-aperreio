<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <i class="pi pi-wallet auth-icon"></i>
        <h1 class="auth-title">Sem Aperreio</h1>
        <p class="auth-subtitle">Controle seus gastos domésticos</p>
      </div>

      <div class="auth-tabs">
        <button :class="['auth-tab', { active: activeTab === 'login' }]" @click="activeTab = 'login'">Entrar</button>
        <button :class="['auth-tab', { active: activeTab === 'register' }]" @click="activeTab = 'register'">Criar Conta</button>
      </div>

      <div class="auth-form-container">
        <LoginForm v-if="activeTab === 'login'" @success="handleAuth" />
        <RegisterForm v-else @auth-success="handleAuth" />
      </div>

      <div v-if="activeTab === 'login'" class="auth-footer">
        <a href="#" class="forgot-link" @click.prevent="showForgotModal = true">Esqueci minha senha</a>
      </div>

      <ForgotPasswordModal v-if="showForgotModal" @close="showForgotModal = false" />
    </div>
  </div>
</template>

<script>
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
import ForgotPasswordModal from './ForgotPasswordModal.vue'

export default {
  components: { LoginForm, RegisterForm, ForgotPasswordModal },
  data() {
    return {
      activeTab: 'login',
      showForgotModal: false
    }
  },
  methods: {
    handleAuth() {
      this.$emit('authenticated')
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
  color: #22c55e;
  margin-bottom: 12px;
}

.auth-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 6px 0;
  background: linear-gradient(90deg, #a78bfa, #22c55e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.auth-subtitle {
  color: #94a3b8;
  font-size: 14px;
  margin: 0;
}

.auth-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  background: rgba(255,255,255,0.03);
  border-radius: 10px;
  padding: 4px;
}

.auth-tab {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: none;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.auth-tab:hover {
  color: white;
}

.auth-tab.active {
  background: #22c55e;
  color: white;
}

.auth-form-container {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
}

.forgot-link {
  color: #94a3b8;
  font-size: 13px;
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #22c55e;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 24px 20px;
  }
}
</style>
