<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <Transition
    enter-active-class="motion-fade-in"
    leave-active-class="motion-fade-out"
  >
    <div v-if="visible" class="offline-state" role="status" aria-live="polite">
      <div class="offline-state__icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M1 4l2 2m16-2l-2 2M4 11l2 2m10-2l-2 2M7 18l2 2m4-2l-2 2"/>
          <circle cx="12" cy="12" r="10" stroke-dasharray="4 4"/>
        </svg>
      </div>
      <p class="offline-state__title">Sem internet agora 😅</p>
      <p class="offline-state__message">
        Mas teus últimos dados continuam aqui.
      </p>
    </div>
  </Transition>
</template>

<style scoped>
.offline-state {
  background: linear-gradient(135deg, #1a1d23 0%, #23262d 100%);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 16px;
  padding: 2rem 1.5rem;
  text-align: center;
  max-width: 320px;
  margin: 2rem auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.offline-state__icon {
  width: 56px;
  height: 56px;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: #f59e0b;
}

.offline-state__icon svg {
  width: 28px;
  height: 28px;
}

.offline-state__title {
  margin: 0 0 0.5rem;
  font-size: 1.0625rem;
  font-weight: 600;
  color: #f0f2f5;
}

.offline-state__message {
  margin: 0;
  font-size: 0.875rem;
  color: #9ca3af;
  line-height: 1.5;
}
</style>
