<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <img src="../assets/logo-pdf.png" alt="Sem Aperreio" class="auth-logo" />
        <p class="auth-tagline">Seu Bené deixa sua vida financeira sem aperreio 😄</p>
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
        <a href="#" class="forgot-link" @click.prevent="showForgotModal = true">
          <i class="pi pi-lock forgot-icon"></i>
          Esqueci minha senha
        </a>
      </div>

      <div class="auth-bene">
        <img src="../assets/bene-avatar.png" alt="Seu Bené" class="bene-avatar" />
        <div class="bene-text">
          <span>Qualquer coisa,</span>
          <span><span class="bene-name">Seu Bené</span> tá por aqui 😄</span>
        </div>
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
  background: radial-gradient(circle at 50% 0%, #0f172a, #020617);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: rgba(11, 18, 32, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 32px;
  border-radius: 24px;
  box-shadow:
    0 8px 32px rgba(0,0,0,0.4),
    0 0 0 1px rgba(255,255,255,0.04),
    inset 0 1px 0 rgba(255,255,255,0.04);
  border: none;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-logo {
  width: 220px;
  height: 220px;
  object-fit: contain;
  display: block;
  margin: -16px auto 0;
}

.auth-tagline {
  margin: 10px 0 0;
  padding: 0;
  line-height: 1.4;
  font-size: 14px;
  color: rgba(148,163,184,0.7);
  letter-spacing: 0.2px;
}

.auth-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 28px;
  background: rgba(255,255,255,0.03);
  border-radius: 14px;
  padding: 5px;
  border: 1px solid rgba(255,255,255,0.04);
}

.auth-tab {
  flex: 1;
  padding: 10px 14px;
  border: none;
  border-radius: 10px;
  background: none;
  color: rgba(148,163,184,0.8);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-tab:hover {
  color: rgba(255,255,255,0.9);
}

.auth-tab.active {
  background: transparent;
  color: white;
  box-shadow: 0 0 0 2px rgba(34,197,94,0.05), 0 0 12px rgba(34,197,94,0.04);
}

.auth-form-container {
  animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}

.forgot-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: rgba(148,163,184,0.6);
  font-size: 13px;
  text-decoration: none;
  transition: all 0.25s ease;
}

.forgot-link:hover {
  color: rgba(34,197,94,0.8);
}

.forgot-icon {
  font-size: 12px;
}

.auth-bene {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 16px;
  margin-bottom: 16px;
  font-size: 13px;
  color: rgba(148,163,184,0.5);
}

.bene-text {
  display: flex;
  flex-direction: column;
  line-height: 1.4;
}

.bene-avatar {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  object-fit: cover;
}

.bene-name {
  color: #22c55e;
  font-weight: 500;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 20px;
  }
}
</style>
