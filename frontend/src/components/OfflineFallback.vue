<template>
  <div v-if="isOffline" class="offline-fallback">
    <div class="offline-content">
      <i class="pi pi-wifi-off offline-icon"></i>
      <h2>Você está offline</h2>
      <p>Os dados do último acesso estão disponíveis para consulta.</p>
      <p class="offline-hint">Novos registros serão sincronizados quando a conexão voltar.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const isOffline = ref(!navigator.onLine)

function handleOnline() {
  isOffline.value = false
}

function handleOffline() {
  isOffline.value = true
}

onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onBeforeUnmount(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>

<style scoped>
.offline-fallback {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-primary, #1a1d23);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.offline-content {
  text-align: center;
  padding: 2rem;
  max-width: 400px;
}

.offline-icon {
  font-size: 4rem;
  color: var(--text-secondary, #8b9aab);
  margin-bottom: 1.5rem;
  display: block;
}

.offline-content h2 {
  color: var(--text-primary, #f0f2f5);
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}

.offline-content p {
  color: var(--text-secondary, #8b9aab);
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.offline-hint {
  font-size: 0.875rem;
  opacity: 0.7;
}
</style>
