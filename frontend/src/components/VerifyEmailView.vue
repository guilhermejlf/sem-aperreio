<template>
  <div class="auth-page">
    <div class="auth-card">
      <div v-if="loading" class="state">
        <i class="pi pi-spin pi-spinner" style="font-size: 3rem; color: #60A637;"></i>
        <h2>Verificando seu email...</h2>
      </div>

      <div v-else-if="success" class="state">
        <i class="pi pi-check-circle" style="font-size: 3rem; color: #60A637;"></i>
        <h2 style="color: #60A637;">Email confirmado!</h2>
        <p>{{ success }}</p>
        <button class="btn-primary" @click="goToLogin">Fazer login</button>
      </div>

      <div v-else class="state">
        <i class="pi pi-times-circle" style="font-size: 3rem; color: #ef4444;"></i>
        <h2 style="color: #ef4444;">Erro</h2>
        <p>{{ error }}</p>
        <button class="btn-primary" @click="goToLogin">Voltar ao login</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { API_ENDPOINTS, apiRequest } from '../config/api.js'

const loading = ref(true)
const error = ref(null)
const success = ref(null)

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search)
  const token = urlParams.get('token')

  if (!token) {
    error.value = 'Token de verificação não encontrado na URL.'
    loading.value = false
    return
  }

  try {
    const data = await apiRequest(`${API_ENDPOINTS.AUTH_VERIFY_EMAIL}?token=${token}`)
    success.value = data.mensagem || 'Seu email foi confirmado com sucesso!'
  } catch (err) {
    error.value = err.message || 'Erro ao confirmar email. O link pode ter expirado.'
  } finally {
    loading.value = false
  }
})

function goToLogin() {
  window.location.href = '/'
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
  text-align: center;
}

.state {
  padding: 20px 0;
}

.state h2 {
  margin: 16px 0 8px;
}

.state p {
  color: #94a3b8;
  margin-bottom: 20px;
  font-size: 14px;
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
</style>
