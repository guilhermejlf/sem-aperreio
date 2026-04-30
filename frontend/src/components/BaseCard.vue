<template>
  <div class="base-card" :class="{ 'base-card--group': isGroup }">
    <div class="base-card__info">
      <div class="base-card__header">
        <span v-if="icon && !$slots.icon" class="base-card__icon">{{ icon }}</span>
        <slot name="icon"></slot>
        <h4 class="base-card__title">
          <slot name="title">{{ title }}</slot>
        </h4>
        <slot name="header-badge"></slot>
      </div>
      <p v-if="subtitle || $slots.subtitle" class="base-card__subtitle">
        <slot name="subtitle">{{ subtitle }}</slot>
      </p>
      <div class="base-card__extras">
        <slot name="extras"></slot>
      </div>
      <div class="base-card__meta">
        <slot name="meta"></slot>
      </div>
    </div>
    <div class="base-card__right">
      <div class="base-card__value" :style="valueStyle">
        <slot name="value">{{ value }}</slot>
      </div>
      <div class="base-card__badges">
        <slot name="badges"></slot>
      </div>
      <div v-if="$slots.actions" class="base-card__actions">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseCard',
  props: {
    icon: { type: String, default: '' },
    title: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    value: { type: String, default: '' },
    valueColor: { type: String, default: '#22c55e' },
    isGroup: { type: Boolean, default: false }
  },
  computed: {
    valueStyle() {
      return this.valueColor ? { color: this.valueColor } : {}
    }
  }
}
</script>

<style scoped>
.base-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.base-card:hover {
  background: rgba(255, 255, 255, 0.05);
}

.base-card--group {
  border-left: 3px solid #22c55e;
}

.base-card__info {
  flex: 1;
  min-width: 0;
}

.base-card__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  flex-wrap: wrap;
}

.base-card__icon {
  font-size: 18px;
  line-height: 1;
}

.base-card__title {
  margin: 0;
  color: #e5e7eb;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.3;
}

.base-card__subtitle {
  margin: 0 0 4px 0;
  color: #94a3b8;
  font-size: 13px;
  line-height: 1.4;
}

.base-card__extras {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.base-card__extras :deep(small),
.base-card__extras :deep(.base-card__extra-item) {
  color: #64748b;
  font-style: italic;
  display: block;
  margin-bottom: 4px;
  font-size: 12px;
  line-height: 1.4;
}

.base-card__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
}

.base-card__meta :deep(.base-card__meta-item) {
  color: #64748b;
  font-size: 11px;
  display: block;
}

.base-card__right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  flex-shrink: 0;
  margin-left: 16px;
}

.base-card__value {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.2;
  white-space: nowrap;
}

.base-card__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
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
  color: #64748b;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s ease;
  padding: 4px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.base-card__actions :deep(.edit-btn:hover) {
  color: #3b82f6;
}

.base-card__actions :deep(.delete-btn:hover) {
  color: #ef4444;
}

@media (max-width: 768px) {
  .base-card {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .base-card__header {
    justify-content: center;
  }

  .base-card__right {
    align-items: center;
    margin-left: 0;
  }

  .base-card__badges {
    justify-content: center;
  }
}
</style>
