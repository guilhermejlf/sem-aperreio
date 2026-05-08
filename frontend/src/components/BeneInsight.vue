<template>
  <div
    v-if="visible"
    class="bene-tooltip"
    :class="[`bene-tooltip--${variant}`]"
    @click="handleClick"
  >
    <span class="bene-tooltip__text">{{ message }}</span>
  </div>
</template>

<script>
export default {
  name: 'BeneInsight',
  props: {
    message: { type: String, required: true },
    variant: {
      type: String,
      default: 'neutral',
      validator: (v) => ['info', 'success', 'warning', 'neutral'].includes(v),
    },
    visible: { type: Boolean, default: true },
  },
  emits: ['click'],
  methods: {
    handleClick() {
      this.$emit('click')
    },
  },
}
</script>

<style scoped>
.bene-tooltip {
  position: relative;
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  max-width: 220px;
  user-select: none;
  transition: all 0.25s ease;
}

.bene-tooltip:hover {
  background: rgba(15, 23, 42, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

.bene-tooltip__text {
  font-size: 12px;
  line-height: 1.35;
  color: #cbd5e1;
}

/* Arrow pointing down to avatar */
.bene-tooltip::after {
  content: '';
  position: absolute;
  bottom: -5px;
  right: 28px;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid rgba(15, 23, 42, 0.65);
  transition: border-top-color 0.25s ease;
}

.bene-tooltip:hover::after {
  border-top-color: rgba(15, 23, 42, 0.8);
}

/* Variant accents — very subtle */
.bene-tooltip--info {
  border-color: rgba(59, 130, 246, 0.12);
}

.bene-tooltip--success {
  border-color: rgba(34, 197, 94, 0.12);
}

.bene-tooltip--warning {
  border-color: rgba(245, 158, 11, 0.12);
}
</style>
