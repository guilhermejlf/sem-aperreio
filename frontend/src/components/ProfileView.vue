<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- Header -->
      <div class="profile-header">
        <div class="profile-avatar">
          {{ profileStore.avatarInitial }}
        </div>
        <h1 class="profile-name">{{ profileStore.displayName }}</h1>
        <p class="profile-email">{{ profileStore.data?.email }}</p>
        <p v-if="benePhrase" class="profile-bene">{{ benePhrase }}</p>
      </div>

      <!-- Card Principal -->
      <div class="profile-card">
        <h2 class="card-title">Dados Pessoais</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Nome completo</label>
            <input
              v-model="form.first_name"
              type="text"
              class="form-input"
              placeholder="Seu nome"
            />
          </div>
          <div class="form-group">
            <label>Username</label>
            <input
              v-model="form.username"
              type="text"
              class="form-input"
              placeholder="@usuario"
            />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input
              :value="profileStore.data?.email"
              type="email"
              class="form-input"
              disabled
            />
          </div>
          <div class="form-group">
            <label>Grupo Familiar</label>
            <input
              :value="familyName"
              type="text"
              class="form-input"
              disabled
            />
          </div>
        </div>
        <div class="card-actions">
          <button
            class="btn-primary"
            :disabled="saving || !changed"
            @click="saveProfile"
          >
            <span v-if="saving">Salvando...</span>
            <span v-else>Salvar Alterações</span>
          </button>
        </div>
      </div>

      <!-- Segurança -->
      <div class="profile-card">
        <h2 class="card-title">Segurança</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Senha atual</label>
            <input
              v-model="passwordForm.current_password"
              type="password"
              class="form-input"
              placeholder="••••••••"
            />
          </div>
          <div class="form-group">
            <label>Nova senha</label>
            <input
              v-model="passwordForm.new_password"
              type="password"
              class="form-input"
              placeholder="••••••••"
            />
          </div>
          <div class="form-group">
            <label>Confirmar nova senha</label>
            <input
              v-model="passwordForm.confirm_password"
              type="password"
              class="form-input"
              placeholder="••••••••"
            />
          </div>
        </div>
        <div class="card-actions">
          <button
            class="btn-secondary"
            :disabled="changingPassword"
            @click="savePassword"
          >
            <span v-if="changingPassword">Alterando...</span>
            <span v-else>Alterar Senha</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted, ref, watch } from 'vue'
import { profileStore } from '../stores/profile.store.js'
import { changePassword } from '../config/api.js'
import { toastStore } from '../stores/toast.store.js'

const form = reactive({
  first_name: '',
  username: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const saving = ref(false)
const changingPassword = ref(false)

const benePhrases = [
  'Qualquer coisa, Seu Bené tá por aqui 😄',
  'Cuidando do seu perfil com carinho! 🌱',
  'Tudo certo por aqui, patrão? 👍',
]
const benePhrase = computed(() => {
  const idx = (profileStore.data?.id || 0) % benePhrases.length
  return benePhrases[idx]
})

const familyName = computed(() => {
  return profileStore.data?.family?.name || 'Nenhum grupo'
})

const changed = computed(() => {
  return (
    form.first_name !== (profileStore.data?.first_name || '') ||
    form.username !== (profileStore.data?.username || '')
  )
})

onMounted(async () => {
  await profileStore.load()
  form.first_name = profileStore.data?.first_name || ''
  form.username = profileStore.data?.username || ''
})

watch(() => profileStore.data, (data) => {
  if (data) {
    form.first_name = data.first_name || ''
    form.username = data.username || ''
  }
})

async function saveProfile() {
  saving.value = true
  try {
    await profileStore.update({
      first_name: form.first_name,
      username: form.username,
    })
    toastStore.success('Perfil atualizado 😄')
  } catch (err) {
    toastStore.error(err.message || 'Erro ao atualizar perfil')
  } finally {
    saving.value = false
  }
}

async function savePassword() {
  changingPassword.value = true
  try {
    await changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password,
      confirm_password: passwordForm.confirm_password,
    })
    toastStore.success('Senha alterada com sucesso!')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (err) {
    toastStore.error(err.message || 'Erro ao alterar senha')
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
.profile-page {
  padding: 32px 20px;
  max-width: 820px;
  margin: 0 auto;
}

.profile-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header */
.profile-header {
  text-align: center;
  padding: 32px 20px;
  background: linear-gradient(180deg, rgba(30,41,59,0.88) 0%, rgba(15,23,42,0.92) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  backdrop-filter: blur(20px);
}

.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 999px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 20px rgba(96, 166, 55, 0.25);
}

.profile-name {
  font-size: 22px;
  font-weight: 700;
  color: #F8FAFC;
  margin: 0 0 6px;
}

.profile-email {
  font-size: 14px;
  color: rgba(148, 163, 184, 0.85);
  margin: 0 0 12px;
}

.profile-bene {
  font-size: 13px;
  color: rgba(96, 166, 55, 0.85);
  font-style: italic;
  margin: 0;
}

/* Card */
.profile-card {
  background: linear-gradient(180deg, rgba(30,41,59,0.88) 0%, rgba(15,23,42,0.92) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(20px);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #F8FAFC;
  margin: 0 0 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 500;
  color: rgba(148, 163, 184, 0.85);
}

.form-input {
  height: 48px;
  padding: 0 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: #F8FAFC;
  font-size: 15px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #60A637;
  box-shadow: 0 0 0 4px rgba(96, 166, 55, 0.12);
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.card-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* Buttons */
.btn-primary {
  height: 48px;
  padding: 0 28px;
  border-radius: 14px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: #fff;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 18px rgba(96, 166, 55, 0.12);
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.05);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  height: 48px;
  padding: 0 28px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: rgba(248, 250, 252, 0.9);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Messages */
.success-msg {
  margin-top: 12px;
  font-size: 14px;
  color: #60A637;
  text-align: right;
}

.error-msg {
  margin-top: 12px;
  font-size: 14px;
  color: #ef4444;
  text-align: right;
}

/* Responsive */
@media (max-width: 768px) {
  .profile-page {
    padding: 20px 16px;
  }

  .profile-header {
    padding: 24px 16px;
    border-radius: 20px;
  }

  .profile-avatar {
    width: 64px;
    height: 64px;
    font-size: 24px;
  }

  .profile-name {
    font-size: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    justify-content: stretch;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}
</style>
