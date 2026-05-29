<template>
  <div class="base-card" :class="{ 'base-card--group': isGroup }">
    <div class="base-card__body">
      <div class="base-card__info">
        <div class="base-card__header">
          <span v-if="icon && !slots.icon" class="base-card__icon">{{ icon }}</span>
          <slot name="icon"></slot>
          <h4 class="base-card__title">
            <slot name="title">{{ title }}</slot>
          </h4>
          <slot name="header-badge"></slot>
        </div>
        <p v-if="subtitle || slots.subtitle" class="base-card__subtitle">
          <slot name="subtitle">{{ subtitle }}</slot>
        </p>
        <div class="base-card__extras">
          <slot name="extras"></slot>
        </div>
        <div class="base-card__meta">
          <slot name="meta"></slot>
        </div>
      </div>
      <div class="base-card__summary">
        <div class="base-card__value" :style="valueStyle">
          <slot name="value">{{ value }}</slot>
        </div>
        <div class="base-card__badges">
          <slot name="badges"></slot>
        </div>
      </div>
    </div>
    <div v-if="slots.actions" class="base-card__actions-col">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  icon: { type: String, default: '' },
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  value: { type: String, default: '' },
  valueColor: { type: String, default: '#60A637' },
  isGroup: { type: Boolean, default: false }
})

const slots = useSlots()

const valueStyle = computed(() => props.valueColor ? { color: props.valueColor } : {})
</script>

<style scoped>
.base-card {
  background: var(--bg-hover);
  border-radius: var(--radius-sm);
  padding: var(--space-4);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all var(--transition-fast);
  border: var(--glass-border);
}

.base-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: var(--card-lift);
}

.base-card--group {
  border-left: 3px solid var(--color-primary);
}

.base-card__info {
  flex: 1;
  min-width: 0;
}

.base-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
  flex-wrap: wrap;
}

.base-card__icon {
  font-size: var(--font-lg);
  line-height: 1;
}

.base-card__title {
  margin: 0;
  color: var(--text-primary);
  font-size: 15px;
  font-weight: var(--weight-medium);
  line-height: 1.3;
}

.base-card__subtitle {
  margin: 0 0 var(--space-1) 0;
  color: var(--text-secondary);
  font-size: var(--font-sm);
  line-height: 1.4;
}

.base-card__extras {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.base-card__extras :deep(small),
.base-card__extras :deep(.base-card__extra-item) {
  color: var(--text-muted);
  font-style: italic;
  display: block;
  margin-bottom: var(--space-1);
  font-size: var(--font-xs);
  line-height: 1.4;
}

.base-card__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
}

.base-card__meta :deep(.base-card__meta-item) {
  color: var(--text-muted);
  font-size: 11px;
  display: block;
}

.base-card__body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
  min-width: 0;
}

.base-card__summary {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-2);
  flex-shrink: 0;
  margin-left: var(--space-4);
}

.base-card__actions-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-left: var(--space-4);
  padding-left: var(--space-3);
  border-left: var(--glass-border);
  flex-shrink: 0;
}

.base-card__value {
  font-size: var(--font-lg);
  font-weight: var(--weight-semibold);
  line-height: 1.2;
  white-space: nowrap;
}

.base-card__badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  justify-content: flex-end;
}

.base-card__actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.base-card__actions :deep(.edit-btn),
.base-card__actions :deep(.delete-btn) {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: var(--font-sm);
  cursor: pointer;
  transition: color var(--transition-fast);
  padding: var(--space-1);
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.base-card__actions :deep(.edit-btn:hover) {
  color: var(--color-info);
}

.base-card__actions :deep(.delete-btn:hover) {
  color: var(--color-error);
}

@media (max-width: 768px) {
  .base-card {
    gap: var(--space-3);
    padding: 14px;
    background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-surface) 100%);
    border: var(--glass-border);
    align-items: stretch;
  }

  .base-card__info {
    flex: 1;
    min-width: 0;
    text-align: left;
  }

  .base-card__header {
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .base-card__subtitle {
    color: var(--text-secondary);
    text-align: left;
  }

  .base-card__extras :deep(small),
  .base-card__extras :deep(.base-card__extra-item) {
    color: var(--text-secondary);
    text-align: left;
  }

  .base-card__meta :deep(.base-card__meta-item) {
    color: var(--text-secondary);
    font-size: 12px;
    text-align: left;
  }

  .base-card__body {
    flex-direction: column;
    align-items: stretch;
    gap: var(--space-3);
  }

  .base-card__summary {
    align-items: flex-start;
    margin-left: 0;
    gap: 6px;
  }

  .base-card__value {
    font-size: 16px;
  }

  .base-card__badges {
    justify-content: flex-start;
  }

  .base-card__actions-col {
    margin-left: var(--space-2);
    padding-left: var(--space-3);
    border-left: var(--glass-border);
    justify-content: center;
  }

  .base-card__actions-col :deep(.edit-btn),
  .base-card__actions-col :deep(.delete-btn) {
    min-width: 40px;
    min-height: 40px;
    font-size: 18px;
    color: var(--text-muted);
    padding: 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.2s ease;
  }

  .base-card__actions-col :deep(.edit-btn:hover) {
    color: var(--text-secondary);
  }

  .base-card__actions-col :deep(.delete-btn:hover) {
    color: #ef4444;
  }
}
</style>
