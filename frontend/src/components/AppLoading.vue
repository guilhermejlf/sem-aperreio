<template>
  <div class="app-loading" :class="{ inline, fullscreen }">
    <div v-if="inline" class="app-loading--inline">
      <i class="pi pi-spin pi-spinner" />
    </div>
    <div v-else class="app-loading--center">
      <i class="pi pi-spin pi-spinner" />
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppLoading',
  props: {
    inline: { type: Boolean, default: false },
    fullscreen: { type: Boolean, default: false },
    message: { type: String, default: '' },
  },
}
</script>

<style scoped>
.app-loading {
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-loading--inline {
  display: inline-flex;
}

.app-loading--center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  padding: var(--space-lg);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.app-loading--center i {
  font-size: 1.5rem;
  color: var(--color-brand);
}

.fullscreen {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  background: var(--color-bg-base);
}

.app-loading--inline i {
  font-size: 1rem;
  color: var(--color-text-secondary);
}
</style>
