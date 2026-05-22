<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <div class="error-icon">
        <i class="pi pi-exclamation-circle"></i>
      </div>
      <h2 class="error-title">Teu Bené teve um aperreio aqui 😅</h2>
      <p class="error-message">{{ displayMessage }}</p>
      <div class="error-actions">
        <button class="retry-btn" @click="handleRetry">
          <i class="pi pi-refresh"></i>
          Bora tentar novamente?
        </button>
        <button v-if="canGoHome" class="home-btn" @click="goHome">
          <i class="pi pi-home"></i>
          Voltar pro início
        </button>
      </div>
    </div>
  </div>
  <slot v-else></slot>
</template>

<script>
import { captureError } from '../config/sentry.js'

export default {
  name: 'ErrorBoundary',
  data() {
    return {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  },
  computed: {
    displayMessage() {
      if (this.error?.message?.includes('network') || this.error?.message?.includes('fetch')) {
        return 'Parece que a conexão deu uma vacilada. Verifica se tu tá online e tenta de novo.'
      }
      if (this.error?.message?.includes('timeout')) {
        return 'O servidor tá demorando mais que o normal. Bora esperar um pouquinho e tentar de novo?'
      }
      if (this.error?.message?.includes('chunk') || this.error?.message?.includes('loading')) {
        return 'Um pedacinho do app não carregou direito. Atualiza a página que resolve.'
      }
      return 'Algo inesperado aconteceu, mas já estamos cuidando disso.'
    },
    canGoHome() {
      return this.$route && this.$route.path !== '/'
    }
  },
  errorCaptured(err, instance, info) {
    this.hasError = true
    this.error = err
    this.errorInfo = info

    // Log to console
    console.error('[ErrorBoundary] Captured error:', err, info)

    // Send to Sentry
    captureError(err, {
      component: instance?.$options?.name || 'unknown',
      errorInfo: info,
      route: this.$route?.path,
    })

    return false
  },
  methods: {
    handleRetry() {
      const isChunkError = this.error?.message?.includes('chunk') || this.error?.message?.includes('loading')
      if (isChunkError) {
        // Chunk errors precisam de reload para baixar o novo chunk
        window.location.reload()
        return
      }
      this.hasError = false
      this.error = null
      this.errorInfo = null
      this.$emit('retry')
    },
    goHome() {
      this.hasError = false
      this.error = null
      this.errorInfo = null
      if (this.$router) {
        this.$router.push('/')
      } else {
        window.location.href = '/'
      }
    }
  }
}
</script>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;
  background: var(--surface-ground, #0f172a);
}

.error-content {
  text-align: center;
  max-width: 400px;
}

.error-icon {
  font-size: 64px;
  color: var(--primary-color, #f59e0b);
  margin-bottom: 24px;
  animation: pulse 2s ease-in-out infinite;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color, #f1f5f9);
  margin-bottom: 12px;
  line-height: 1.3;
}

.error-message {
  font-size: 1rem;
  color: var(--text-color-secondary, #94a3b8);
  margin-bottom: 32px;
  line-height: 1.5;
}

.error-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.retry-btn, .home-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.retry-btn {
  background: var(--primary-color, #f59e0b);
  color: var(--primary-color-text, #0f172a);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
}

.home-btn {
  background: transparent;
  color: var(--text-color-secondary, #94a3b8);
  border: 1px solid var(--surface-border, #334155);
}

.home-btn:hover {
  background: var(--surface-hover, #1e293b);
  color: var(--text-color, #f1f5f9);
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}

@media (min-width: 768px) {
  .error-actions {
    flex-direction: row;
    justify-content: center;
  }
}
</style>
