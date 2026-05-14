<template>
  <div class="settings-page">
    <div class="settings-container">
      <!-- Header -->
      <div class="settings-header">
        <h1 class="settings-title">Configurações</h1>
        <p class="settings-subtitle">Se oriente do teu jeito 😄</p>
      </div>

      <!-- Card: Aparência -->
      <div class="settings-card">
        <h2 class="card-title">
          <i class="pi pi-palette card-icon"></i>
          Aparência
        </h2>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Tema escuro</span>
            <span class="setting-desc">Experiência visual atual</span>
          </div>
          <SettingsToggle v-model="settings.themeDark" />
        </div>
      </div>

      <!-- Card: Notificações -->
      <div class="settings-card">
        <h2 class="card-title">
          <i class="pi pi-bell card-icon"></i>
          Notificações
        </h2>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Lembrete semanal</span>
            <span class="setting-desc">Receba um resumo toda segunda-feira</span>
          </div>
          <SettingsToggle v-model="settings.notifications.weeklyReminder" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Alertas de orçamento</span>
            <span class="setting-desc">Aviso quando atingir limites definidos</span>
          </div>
          <SettingsToggle v-model="settings.notifications.budgetAlerts" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Alertas de média histórica</span>
            <span class="setting-desc">Comparativo com meses anteriores</span>
          </div>
          <SettingsToggle v-model="settings.notifications.averageAlerts" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Notificações do Seu Bené</span>
            <span class="setting-desc">Dicas e insights contextuais</span>
          </div>
          <SettingsToggle v-model="settings.notifications.beneInsights" />
        </div>
      </div>

      <!-- Card: Seu Bené -->
      <div class="settings-card">
        <h2 class="card-title">
          <i class="pi pi-sparkles card-icon"></i>
          Seu Bené
        </h2>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Mostrar insights contextuais</span>
            <span class="setting-desc">Frases inteligentes conforme sua rotina</span>
          </div>
          <SettingsToggle v-model="settings.bene.showInsights" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Mostrar presença flutuante</span>
            <span class="setting-desc">Avatar animado no canto da tela</span>
          </div>
          <SettingsToggle v-model="settings.bene.showPresence" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Frequência dos insights</span>
            <span class="setting-desc">Quanto o Bené aparece</span>
          </div>
          <div class="frequency-select">
            <button
              v-for="opt in frequencies"
              :key="opt.value"
              :class="['freq-btn', { active: settings.bene.frequency === opt.value }]"
              @click="settings.bene.frequency = opt.value"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Card: Privacidade -->
      <div class="settings-card">
        <h2 class="card-title">
          <i class="pi pi-shield card-icon"></i>
          Privacidade
        </h2>
        <div class="setting-row placeholder">
          <div class="setting-info">
            <span class="setting-label">Exportar meus dados</span>
            <span class="setting-desc">Em breve</span>
          </div>
          <span class="soon-badge">Em breve</span>
        </div>
        <div class="setting-row placeholder">
          <div class="setting-info">
            <span class="setting-label">Remover minha conta</span>
            <span class="setting-desc">Em breve</span>
          </div>
          <span class="soon-badge">Em breve</span>
        </div>
      </div>

      <!-- Card: Experiência -->
      <div class="settings-card">
        <h2 class="card-title">
          <i class="pi pi-desktop card-icon"></i>
          Experiência
        </h2>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Animações suaves</span>
            <span class="setting-desc">Transições mais fluidas pelo app</span>
          </div>
          <SettingsToggle v-model="settings.experience.smoothAnimations" />
        </div>
        <div class="setting-row">
          <div class="setting-info">
            <span class="setting-label">Reduzir movimento</span>
            <span class="setting-desc">Menos animações para acessibilidade</span>
          </div>
          <SettingsToggle v-model="settings.experience.reduceMotion" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { settingsStore } from '../stores/settings.store.js'
import { toastStore } from '../stores/toast.store.js'
import SettingsToggle from './SettingsToggle.vue'

const settings = settingsStore

const frequencies = [
  { value: 'low', label: 'Baixa' },
  { value: 'normal', label: 'Normal' },
  { value: 'high', label: 'Alta' },
]

watch(settings, () => {
  toastStore.success('Configurações salvas automaticamente 😄')
}, { deep: true })
</script>

<style scoped>
.settings-page {
  padding: 32px 20px;
  max-width: 920px;
  margin: 0 auto;
}

.settings-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header */
.settings-header {
  padding: 0 4px;
}

.settings-title {
  font-size: 22px;
  font-weight: 700;
  color: #F8FAFC;
  margin: 0 0 6px;
}

.settings-subtitle {
  font-size: 14px;
  color: rgba(148, 163, 184, 0.8);
  margin: 0;
}

/* Card */
.settings-card {
  background: linear-gradient(180deg, rgba(30,41,59,0.88) 0%, rgba(15,23,42,0.92) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(20px);
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #F8FAFC;
  margin: 0 0 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-icon {
  font-size: 15px;
  color: #60A637;
  opacity: 0.85;
}

/* Setting Row */
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.setting-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.setting-row:first-of-type {
  padding-top: 0;
}

.setting-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}

.setting-label {
  font-size: 14px;
  font-weight: 500;
  color: rgba(248, 250, 252, 0.92);
}

.setting-desc {
  font-size: 12px;
  color: rgba(148, 163, 184, 0.7);
}

/* Frequency */
.frequency-select {
  display: flex;
  gap: 6px;
}

.freq-btn {
  height: 32px;
  padding: 0 14px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(148, 163, 184, 0.8);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.freq-btn:hover {
  background: rgba(255, 255, 255, 0.07);
}

.freq-btn.active {
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  border-color: transparent;
  color: #fff;
  box-shadow: 0 0 12px rgba(96, 166, 55, 0.12);
}

/* Placeholder */
.placeholder .setting-label,
.placeholder .setting-desc {
  opacity: 0.45;
}

.soon-badge {
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(148, 163, 184, 0.5);
}

/* Save toast */
.save-toast {
  text-align: center;
  font-size: 14px;
  color: #60A637;
  margin: 4px 0 0;
}

/* Responsive */
@media (max-width: 768px) {
  .settings-page {
    padding: 20px 16px;
  }

  .settings-card {
    padding: 20px 18px;
    border-radius: 18px;
  }

  .setting-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .frequency-select {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
