<template>
  <div
    class="statement-item"
    :class="{ 'statement-item--receita': isReceita }"
  >
    <div class="statement-item__icon">
      {{ icon }}
    </div>

    <div class="statement-item__content">
      <div class="statement-item__header">
        <span class="statement-item__title">
          {{ title }}
        </span>
        <span
          class="statement-item__value"
          :class="valueClass"
        >
          {{ valuePrefix }} {{ formatarValor(valor) }}
        </span>
      </div>

      <div class="statement-item__meta">
        <span v-if="dataContextual" class="statement-item__time">
          {{ dataContextual }}
        </span>
        <span v-if="categoriaLabel" class="statement-item__category">
          {{ categoriaLabel }}
        </span>
        <span
          v-if="statusLabel"
          class="statement-item__status"
          :class="statusClass"
        >
          {{ statusLabel }}
        </span>
        <span v-if="membroNome" class="statement-item__member">
          <i class="pi pi-user" style="font-size: 8px"></i>
          {{ membroNome }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatementItem',

  props: {
    item: {
      type: Object,
      required: true
    },
    categorias: {
      type: Array,
      default: () => []
    }
  },

  computed: {
    isReceita() {
      return this.item.tipo === 'receita'
    },

    icon() {
      if (this.isReceita) return '💰'
      const icons = {
        moradia: '🏠',
        mercado: '🛒',
        restaurantes: '🍔',
        transporte: '🚗',
        saude: '🏥',
        educacao: '📚',
        lazer: '🎮',
        contas: '💡',
        compras: '🛍️',
        outros: '📦'
      }
      return icons[this.item.categoria] || '💳'
    },

    title() {
      return this.item.descricao || this.categoriaLabel || 'Receita'
    },

    categoriaLabel() {
      const c = this.categorias.find(c => c.value === this.item.categoria)
      return c ? c.label : this.item.categoria
    },

    dataContextual() {
      if (!this.item.data) return ''
      try {
        const data = new Date(this.item.data + 'T12:00:00')
        if (isNaN(data.getTime())) return ''
        return data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      } catch {
        return ''
      }
    },

    valor() {
      return parseFloat(this.item.valor || 0)
    },

    valuePrefix() {
      return this.isReceita ? '+' : '-'
    },

    valueClass() {
      return this.isReceita ? 'value--receita' : 'value--gasto'
    },

    statusLabel() {
      if (this.isReceita) return null
      return this.item.pago ? 'Pago' : 'Pendente'
    },

    statusClass() {
      return this.item.pago ? 'status--pago' : 'status--pendente'
    },

    membroNome() {
      return this.item.membro_nome || this.item.user_name || null
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
.statement-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
  cursor: pointer;
}

.statement-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.statement-item__icon {
  font-size: 20px;
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  line-height: 1;
}

.statement-item__content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.statement-item__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.statement-item__title {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.statement-item__value {
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.value--receita {
  color: #60A637;
}

.value--gasto {
  color: #ef4444;
}

.statement-item__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
}

.statement-item__time {
  color: #64748b;
}

.statement-item__category {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 8px;
  border-radius: 4px;
  color: #94a3b8;
}

.statement-item__status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.status--pago {
  background: rgba(96, 166, 55, 0.1);
  color: #60A637;
}

.status--pendente {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.statement-item__member {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #64748b;
}

@media (max-width: 768px) {
  .statement-item {
    padding: 12px;
    gap: 10px;
  }

  .statement-item__icon {
    width: 32px;
    height: 32px;
    font-size: 18px;
  }

  .statement-item__title {
    font-size: 13px;
  }

  .statement-item__value {
    font-size: 13px;
  }
}
</style>
