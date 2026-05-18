<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['install', 'dismiss'])
</script>

<template>
  <Transition
    enter-active-class="motion-fade-in motion-slide-up"
    leave-active-class="motion-fade-out motion-slide-down"
  >
    <div
      v-if="visible"
      class="install-prompt"
      role="dialog"
      aria-label="Instalar aplicativo"
    >
      <div class="install-prompt__content">
        <div class="install-prompt__icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <div class="install-prompt__text">
          <p class="install-prompt__title">Instala o Sem Aperreio no celular</p>
          <p class="install-prompt__subtitle">pra acessar mais rápido 😄</p>
        </div>
        <button
          class="install-prompt__cta"
          @click="emit('install')"
        >
          Instalar
        </button>
        <button
          class="install-prompt__close"
          aria-label="Fechar"
          @click="emit('dismiss')"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.install-prompt {
  position: fixed;
  bottom: calc(1rem + env(safe-area-inset-bottom, 0px));
  left: 1rem;
  right: 1rem;
  z-index: 100;
  pointer-events: none;
}

.install-prompt__content {
  background: linear-gradient(135deg, #1a1d23 0%, #23262d 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(16, 185, 129, 0.1);
  pointer-events: auto;
  max-width: 420px;
  margin: 0 auto;
}

.install-prompt__icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #10b981;
}

.install-prompt__icon svg {
  width: 20px;
  height: 20px;
}

.install-prompt__text {
  flex: 1;
  min-width: 0;
}

.install-prompt__title {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #f0f2f5;
  line-height: 1.3;
}

.install-prompt__subtitle {
  margin: 0.125rem 0 0;
  font-size: 0.8125rem;
  color: #9ca3af;
  line-height: 1.3;
}

.install-prompt__cta {
  flex-shrink: 0;
  background: #10b981;
  color: #0a0c0f;
  font-weight: 600;
  font-size: 0.8125rem;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: transform 0.15s ease, background 0.15s ease;
}

.install-prompt__cta:hover {
  background: #34d399;
  transform: scale(1.03);
}

.install-prompt__close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.install-prompt__close:hover {
  color: #f0f2f5;
}

.install-prompt__close svg {
  width: 18px;
  height: 18px;
}

@media (min-width: 640px) {
  .install-prompt {
    display: none;
  }
}
</style>
