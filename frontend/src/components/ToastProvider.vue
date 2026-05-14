<template>
  <TransitionGroup
    name="toast"
    tag="div"
    class="toast-provider"
    :class="{ mobile: isMobile }"
    @mouseenter="toastStore.pauseAll()"
    @mouseleave="toastStore.resumeAll()"
  >
    <div
      v-for="toast in toastStore.items"
      :key="toast.id"
      :class="['toast-item', toast.variant]"
      @click="dismiss(toast)"
    >
      <span class="toast-icon">{{ iconFor(toast.variant) }}</span>
      <div class="toast-content">
        <span v-if="toast.title" class="toast-title">{{ toast.title }}</span>
        <span class="toast-message">{{ toast.message }}</span>
      </div>
      <button
        v-if="toast.dismissible"
        class="toast-close"
        @click.stop="dismiss(toast)"
        aria-label="Fechar"
      >
        <i class="pi pi-times"></i>
      </button>
    </div>
  </TransitionGroup>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { toastStore } from '../stores/toast.store.js'

const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})

function dismiss(toast) {
  toastStore.remove(toast.id)
}

function iconFor(variant) {
  const icons = {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ℹ',
  }
  return icons[variant] || 'ℹ'
}
</script>

<style scoped>
.toast-provider {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 100%;
  pointer-events: none;
  padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
}

/* Mobile positioning */
.toast-provider.mobile {
  top: 16px;
  right: 50%;
  transform: translateX(50%);
  left: auto;
  width: calc(100vw - 32px);
  align-items: center;
}

/* Toast item */
.toast-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 300px;
  max-width: 420px;
  padding: 14px 16px;
  background: rgba(15, 23, 42, 0.92);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.28);
  cursor: pointer;
  pointer-events: auto;
  transition: all 0.2s ease;
}

/* Mobile sizing */
.toast-provider.mobile .toast-item {
  min-width: 0;
  max-width: 380px;
  width: 100%;
}

/* Variant colors */
.toast-item.success { border-left: 3px solid #60A637; }
.toast-item.error { border-left: 3px solid #EF4444; }
.toast-item.warning { border-left: 3px solid #F59E0B; }
.toast-item.info { border-left: 3px solid #38BDF8; }

.toast-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 1px;
}

.toast-item.success .toast-icon { color: #60A637; }
.toast-item.error .toast-icon { color: #EF4444; }
.toast-item.warning .toast-icon { color: #F59E0B; }
.toast-item.info .toast-icon { color: #38BDF8; }

.toast-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 13px;
  font-weight: 600;
  color: rgba(248, 250, 252, 0.85);
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
  color: #F8FAFC;
  line-height: 1.4;
  word-break: break-word;
}

.toast-close {
  appearance: none;
  border: none;
  background: none;
  padding: 4px;
  margin: -4px -4px 0 0;
  cursor: pointer;
  color: rgba(148, 163, 184, 0.6);
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.toast-close:hover {
  color: rgba(248, 250, 252, 0.8);
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Mobile transitions */
.toast-provider.mobile .toast-enter-from {
  opacity: 0;
  transform: translateY(-12px) translateX(50%);
}

.toast-provider.mobile .toast-leave-to {
  opacity: 0;
  transform: translateY(-8px) translateX(50%);
}
</style>
