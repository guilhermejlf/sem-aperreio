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
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 20px;
  animation: emptyFadeIn 0.25s ease both;
}

.empty-state-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.empty-state-icon {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(96, 166, 55, 0.92);
  filter: drop-shadow(0 0 12px rgba(96, 166, 55, 0.12));
  font-size: 28px;
  margin-bottom: 4px;
}

.empty-state-title {
  font-size: 20px;
  font-weight: 700;
  color: #F8FAFC;
  margin: 0;
  letter-spacing: -0.3px;
  line-height: 1.3;
}

.empty-state-description {
  font-size: 14px;
  line-height: 1.6;
  color: rgba(248, 250, 252, 0.68);
  margin: 0;
  max-width: 320px;
}

.empty-state-action {
  margin-top: 8px;
  padding: 10px 20px;
  border-radius: 14px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 14px rgba(96, 166, 55, 0.15);
  font-family: inherit;
}

.empty-state-action:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.empty-state-bene {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 16px;
}

.empty-state-bene-text {
  font-size: 13px;
  color: rgba(248, 250, 252, 0.55);
  font-style: italic;
}

/* Variants */
.empty-state--no-results .empty-state-icon {
  color: rgba(148, 163, 184, 0.7);
  filter: none;
}

/* Responsive */
@media (max-width: 768px) {
  .empty-state {
    padding: 24px 18px;
    border-radius: 20px;
  }

  .empty-state-title {
    font-size: 17px;
  }

  .empty-state-description {
    font-size: 13px;
    max-width: 260px;
  }

  .empty-state-action {
    font-size: 13px;
    padding: 8px 16px;
  }
}

@keyframes emptyFadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
