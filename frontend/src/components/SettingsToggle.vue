<template>
  <button
    :class="['settings-toggle', { active: modelValue }]"
    :aria-checked="modelValue"
    role="switch"
    @click="toggle"
  >
    <span class="toggle-track">
      <span class="toggle-thumb" />
    </span>
  </button>
</template>

<script setup>
const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

function toggle() {
  emit('update:modelValue', !props.modelValue)
}
</script>

<style scoped>
.settings-toggle {
  appearance: none;
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.toggle-track {
  width: 44px;
  height: 26px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  transition: background 0.25s ease, border-color 0.25s ease;
}

.toggle-thumb {
  width: 20px;
  height: 20px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.45);
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), background 0.25s ease;
}

.settings-toggle.active .toggle-track {
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  border-color: transparent;
  box-shadow: 0 0 12px rgba(96, 166, 55, 0.12);
}

.settings-toggle.active .toggle-thumb {
  transform: translateX(18px);
  background: #fff;
}
</style>
