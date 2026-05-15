<template>
  <ModalBase
    :visible="visible"
    :title="title"
    :subtitle="message"
    size="small"
    @close="onReject"
  >
    <template #footer>
      <button class="btn-secondary" @click="onReject">{{ rejectLabel }}</button>
      <button
        :class="['btn-primary', danger && 'btn-danger']"
        @click="onAccept"
      >
        {{ acceptLabel }}
      </button>
    </template>
  </ModalBase>
</template>

<script>
import ModalBase from '../ModalBase.vue'

export default {
  name: 'ConfirmModal',
  components: { ModalBase },
  props: {
    visible: { type: Boolean, default: false },
    title: { type: String, default: 'Confirmar' },
    message: { type: String, default: '' },
    acceptLabel: { type: String, default: 'Confirmar' },
    rejectLabel: { type: String, default: 'Cancelar' },
    danger: { type: Boolean, default: false }
  },
  emits: ['accept', 'reject'],
  methods: {
    onAccept() {
      this.$emit('accept')
    },
    onReject() {
      this.$emit('reject')
    }
  }
}
</script>

<style scoped>
.btn-secondary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.06);
}

.btn-primary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-glow);
}

.btn-primary:hover {
  filter: brightness(1.05);
}

.btn-danger {
  background: linear-gradient(180deg, var(--color-error) 0%, #DC2626 100%) !important;
  box-shadow: 0 0 18px rgba(239, 68, 68, 0.12);
}

.btn-danger:hover {
  filter: brightness(1.05);
}
</style>
