<template>
  <div class="statement-empty">
    <div class="statement-empty__icon">📊</div>
    <h3 class="statement-empty__title">
      Teu extrato ainda tá vazio
    </h3>
    <p class="statement-empty__description">
      Bora registrar tua primeira despesa ou receita pra começar a acompanhar teu histórico financeiro?
    </p>
    <button
      v-if="showAction"
      class="statement-empty__action"
      @click="$emit('action')"
    >
      <i class="pi pi-plus"></i>
      Adicionar lançamento
    </button>
  </div>
</template>

<script>
export default {
  name: 'StatementEmptyState',

  props: {
    showAction: {
      type: Boolean,
      default: true
    }
  },

  emits: ['action']
}
</script>

<style scoped>
.statement-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
  gap: 16px;
}

.statement-empty__icon {
  font-size: 48px;
  opacity: 0.6;
  margin-bottom: 8px;
}

.statement-empty__title {
  font-size: 18px;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.statement-empty__description {
  font-size: 14px;
  color: #64748b;
  max-width: 320px;
  line-height: 1.6;
  margin: 0;
}

.statement-empty__action {
  margin-top: 8px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  background: #3b82f6;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.statement-empty__action:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

@media (max-width: 768px) {
  .statement-empty {
    padding: 40px 20px;
  }

  .statement-empty__title {
    font-size: 16px;
  }

  .statement-empty__description {
    font-size: 13px;
  }
}
</style>
