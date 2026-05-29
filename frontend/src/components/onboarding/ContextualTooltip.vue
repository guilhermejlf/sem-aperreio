<template>
  <div v-if="visible" class="tooltip-bubble" :class="position">
    <button class="tooltip-close" @click="dismiss">
      <i class="pi pi-times"></i>
    </button>
    <p class="tooltip-text">{{ text }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
  position: { type: String, default: 'bottom' }
})

const emit = defineEmits(['dismiss'])

const visible = ref(true)

function dismiss() {
  visible.value = false
  emit('dismiss')
}
</script>

<style scoped>
.tooltip-bubble {
  position: relative;
  background: rgba(11, 18, 32, 0.95);
  border: 1px solid rgba(96, 166, 55, 0.25);
  border-radius: 14px;
  padding: 14px 18px;
  max-width: 280px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(96, 166, 55, 0.08);
  animation: tooltipIn 0.3s ease;
  z-index: 100;
}

@keyframes tooltipIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

.tooltip-close {
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  color: rgba(148, 163, 184, 0.5);
  cursor: pointer;
  font-size: 10px;
  padding: 2px;
  line-height: 1;
}

.tooltip-close:hover {
  color: white;
}

.tooltip-text {
  font-size: 13px;
  color: rgba(226, 232, 240, 0.9);
  line-height: 1.5;
  margin: 0;
  padding-right: 14px;
}
</style>
