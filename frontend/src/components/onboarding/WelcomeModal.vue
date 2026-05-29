<template>
  <div class="welcome-overlay" @click.self="handleExplore">
    <div class="welcome-card">
      <div class="welcome-emoji">👋</div>
      <h2 class="welcome-title">Bem-vindo ao Sem Aperreio</h2>
      <p class="welcome-text">
        Vamos te ajudar a configurar tua vida financeira em poucos minutos.
      </p>
      <div class="welcome-actions">
        <button class="btn-primary" @click="handleStart">
          <i class="pi pi-play"></i>
          Começar
        </button>
        <button class="btn-ghost" @click="handleExplore">
          <i class="pi pi-compass"></i>
          Explorar sozinho
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['start', 'explore'])

function handleStart() {
  emit('start')
}

function handleExplore() {
  emit('explore')
}
</script>

<style scoped>
.welcome-overlay {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.welcome-card {
  background: rgba(11, 18, 32, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  padding: 40px 36px;
  max-width: 380px;
  width: 90%;
  text-align: center;
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.04);
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.welcome-emoji {
  font-size: 48px;
  line-height: 1;
  margin-bottom: 16px;
}

.welcome-title {
  font-size: 22px;
  font-weight: 600;
  color: white;
  margin: 0 0 12px;
}

.welcome-text {
  color: rgba(148, 163, 184, 0.85);
  font-size: 15px;
  line-height: 1.5;
  margin: 0 0 28px;
}

.welcome-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-primary,
.btn-ghost {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 13px 20px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #60A637, #4C8932);
  color: white;
  box-shadow: 0 4px 14px rgba(96, 166, 55, 0.2);
}

.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.btn-ghost {
  background: transparent;
  color: rgba(148, 163, 184, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.8);
}
</style>
