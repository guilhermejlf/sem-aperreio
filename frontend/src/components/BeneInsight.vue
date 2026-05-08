<template>
  <Transition name="bene-insight">
    <div
      v-if="visible"
      class="bene-insight"
      :class="[`bene-insight--${variant}`]"
      @click="handleClick"
    >
      <BeneAvatar size="small" :breathing="false" />
      <span class="bene-insight__text">{{ message }}</span>
      <button
        v-if="dismissible"
        class="bene-insight__dismiss"
        @click.stop="dismiss"
      >
        <i class="pi pi-times"></i>
      </button>
    </div>
  </Transition>
</template>

<script>
import BeneAvatar from './BeneAvatar.vue'

export default {
  name: 'BeneInsight',
  components: { BeneAvatar },
  props: {
    message: { type: String, required: true },
    variant: {
      type: String,
      default: 'neutral',
      validator: (v) => ['info', 'success', 'warning', 'neutral'].includes(v),
    },
    dismissible: { type: Boolean, default: true },
    visible: { type: Boolean, default: true },
  },
  emits: ['click', 'dismiss'],
  methods: {
    handleClick() {
      this.$emit('click')
    },
    dismiss() {
      this.$emit('dismiss')
    },
  },
}
</script>

<style scoped>
.bene-insight {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 260px;
  user-select: none;
}

.bene-insight:hover {
  background: rgba(15, 23, 42, 0.85);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
}

.bene-insight__text {
  font-size: 13px;
  line-height: 1.4;
  color: #e2e8f0;
  flex: 1;
}

.bene-insight__dismiss {
  background: none;
  border: none;
  color: #64748b;
  font-size: 11px;
  cursor: pointer;
  padding: 2px;
  line-height: 1;
  border-radius: 4px;
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.bene-insight__dismiss:hover {
  color: #ef4444;
}

.bene-insight--info {
  border-left: 3px solid #3b82f6;
}

.bene-insight--success {
  border-left: 3px solid #22c55e;
}

.bene-insight--warning {
  border-left: 3px solid #f59e0b;
}

.bene-insight--neutral {
  border-left: 3px solid #64748b;
}

/* Transitions */
.bene-insight-enter-active,
.bene-insight-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.bene-insight-enter-from {
  opacity: 0;
  transform: translateY(8px) scale(0.95);
}

.bene-insight-leave-to {
  opacity: 0;
  transform: translateY(4px) scale(0.97);
}
</style>
