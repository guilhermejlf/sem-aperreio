<template>
  <div class="empty-state" :class="variantClass">
    <div class="empty-state-content">
      <div class="empty-state-icon" v-if="icon">
        <i :class="icon"></i>
      </div>
      <h3 class="empty-state-title">{{ title }}</h3>
      <p v-if="description" class="empty-state-description">{{ description }}</p>
      <button
        v-if="actionLabel"
        class="empty-state-action"
        @click="$emit('action')"
      >
        {{ actionLabel }}
      </button>
    </div>
    <div v-if="showBene" class="empty-state-bene">
      <BeneAvatar size="small" :breathing="false" />
      <span class="empty-state-bene-text">{{ beneText }}</span>
    </div>
  </div>
</template>

<script>
import BeneAvatar from './BeneAvatar.vue'

export default {
  name: 'EmptyState',
  components: { BeneAvatar },
  emits: ['action'],
  props: {
    title: { type: String, required: true },
    description: { type: String, default: '' },
    icon: { type: String, default: '' },
    actionLabel: { type: String, default: '' },
    variant: { type: String, default: 'default' },
    showBene: { type: Boolean, default: false },
    beneText: { type: String, default: '' },
  },
  computed: {
    variantClass() {
      return this.variant ? `empty-state--${this.variant}` : ''
    },
  },
}
</script>

<style scoped>
.empty-state {
  background: var(--bg-surface);
  border: var(--glass-border);
  border-radius: var(--radius-xl);
  padding: var(--space-7) var(--space-6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: var(--space-5);
  animation: fadeInUp var(--motion-base) var(--ease-smooth) both;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.empty-state-icon {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  filter: drop-shadow(0 0 12px var(--color-primary-glow));
  font-size: var(--font-2xl);
  margin-bottom: var(--space-1);
}

.empty-state-title {
  font-size: var(--font-xl);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.3px;
  line-height: 1.3;
}

.empty-state-description {
  font-size: var(--font-sm);
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
  max-width: 320px;
}

.empty-state-action {
  margin-top: var(--space-2);
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  font-size: var(--font-sm);
  font-weight: var(--weight-semibold);
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-glow);
  font-family: inherit;
}

.empty-state-action:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.empty-state-bene {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-glass);
  border: var(--glass-border);
  border-radius: var(--radius-md);
}

.empty-state-bene-text {
  font-size: var(--font-sm);
  color: var(--text-muted);
  font-style: italic;
}

/* Variants */
.empty-state--no-results .empty-state-icon {
  color: var(--text-muted);
  filter: none;
}

/* Responsive */
@media (max-width: 768px) {
  .empty-state {
    padding: var(--space-6) 18px;
    border-radius: var(--radius-lg);
  }

  .empty-state-title {
    font-size: var(--font-lg);
  }

  .empty-state-description {
    font-size: var(--font-sm);
    max-width: 260px;
  }

  .empty-state-action {
    font-size: var(--font-sm);
    padding: var(--space-2) var(--space-4);
  }
}

</style>
