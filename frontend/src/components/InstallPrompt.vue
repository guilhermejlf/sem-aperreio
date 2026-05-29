<template>
  <div v-if="showPrompt" class="install-prompt">
    <div class="install-content">
      <i class="pi pi-download install-icon"></i>
      <span class="install-text">Instale o Sem Aperreio no seu celular</span>
      <button class="install-btn" @click="install">
        <i class="pi pi-check"></i>
        Instalar
      </button>
      <button class="install-close" @click="dismiss">
        <i class="pi pi-times"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const showPrompt = ref(false)
const deferredPrompt = ref(null)

function handleBeforeInstall(e) {
  e.preventDefault()
  deferredPrompt.value = e
  showPrompt.value = true
}

async function install() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  const { outcome } = await deferredPrompt.value.userChoice
  if (outcome === 'accepted') {
    showPrompt.value = false
  }
  deferredPrompt.value = null
}

function dismiss() {
  showPrompt.value = false
  localStorage.setItem('install-prompt-dismissed', Date.now().toString())
}

onMounted(() => {
  const isInstalled = window.matchMedia('(display-mode: standalone)').matches
  const isDismissed = localStorage.getItem('install-prompt-dismissed')

  if (!isInstalled && !isDismissed) {
    window.addEventListener('beforeinstallprompt', handleBeforeInstall)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeinstallprompt', handleBeforeInstall)
})
</script>

<style scoped>
.install-prompt {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  z-index: 9998;
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.install-content {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.3);
  max-width: 480px;
  margin: 0 auto;
}

.install-icon {
  font-size: 1.25rem;
  color: #fff;
  flex-shrink: 0;
}

.install-text {
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  flex: 1;
  line-height: 1.4;
}

.install-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.install-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.install-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
  line-height: 1;
  flex-shrink: 0;
}

.install-close:hover {
  color: #fff;
}
</style>
