<template>
  <div class="statement-group">
    <div class="statement-group__header">
      <span class="statement-group__title">{{ titulo }}</span>
      <span v-if="total" class="statement-group__total">
        {{ formatarValor(total) }}
      </span>
    </div>
    <div class="statement-group__items">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatementGroup',

  props: {
    titulo: {
      type: String,
      required: true
    },
    total: {
      type: Number,
      default: null
    }
  },

  methods: {
    formatarValor(valor) {
      return parseFloat(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    }
  }
}
</script>

<style scoped>
.statement-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.statement-group__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 4px 12px;
}

.statement-group__title {
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.statement-group__total {
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  font-variant-numeric: tabular-nums;
}

.statement-group__items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
