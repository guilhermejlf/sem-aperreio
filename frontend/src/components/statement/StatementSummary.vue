<template>
  <div class="statement-summary" :class="{ 'statement-summary--mobile': isMobile }">
    <div class="summary-card summary-receitas">
      <div class="summary-card__icon">💰</div>
      <div class="summary-card__info">
        <span class="summary-card__label">Receitas</span>
        <span class="summary-card__value">{{ formatarValor(resumo.total_receitas) }}</span>
      </div>
    </div>

    <div class="summary-card summary-gastos">
      <div class="summary-card__icon">💳</div>
      <div class="summary-card__info">
        <span class="summary-card__label">Despesas</span>
        <span class="summary-card__value">{{ formatarValor(resumo.total_gastos) }}</span>
      </div>
    </div>

    <div class="summary-card summary-saldo" :class="saldoClasse">
      <div class="summary-card__icon">⚖️</div>
      <div class="summary-card__info">
        <span class="summary-card__label">Saldo</span>
        <span class="summary-card__value">{{ formatarValor(resumo.saldo) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatementSummary',

  props: {
    resumo: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      isMobile: window.innerWidth <= 768
    }
  },

  computed: {
    saldoClasse() {
      if (!this.resumo) return ''
      return this.resumo.saldo >= 0 ? 'saldo-positivo' : 'saldo-negativo'
    }
  },

  mounted() {
    window.addEventListener('resize', this.onResize)
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.onResize)
  },

  methods: {
    onResize() {
      this.isMobile = window.innerWidth <= 768
    },

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
.statement-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  padding: 16px;
  transition: all 0.2s ease;
}

.summary-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.08);
}

.summary-card__icon {
  font-size: 22px;
  flex-shrink: 0;
}

.summary-card__info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.summary-card__label {
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.summary-card__value {
  font-size: 17px;
  font-weight: 600;
  color: #e5e7eb;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-variant-numeric: tabular-nums;
}

.summary-receitas {
  border-left: 3px solid #60A637;
}

.summary-gastos {
  border-left: 3px solid #ef4444;
}

.summary-saldo {
  border-left: 3px solid #3b82f6;
}

.saldo-positivo .summary-card__value {
  color: #60A637;
}

.saldo-negativo .summary-card__value {
  color: #ef4444;
}

/* Mobile horizontal scroll */
.statement-summary--mobile {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 10px;
  padding-bottom: 8px;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.statement-summary--mobile::-webkit-scrollbar {
  display: none;
}

.statement-summary--mobile .summary-card {
  flex: 0 0 140px;
  scroll-snap-align: start;
  min-width: 140px;
}

@media (max-width: 768px) {
  .statement-summary {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 10px;
    padding-bottom: 8px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .statement-summary::-webkit-scrollbar {
    display: none;
  }

  .summary-card {
    flex: 0 0 140px;
    scroll-snap-align: start;
    min-width: 140px;
    padding: 14px;
  }

  .summary-card__value {
    font-size: 15px;
  }
}
</style>
