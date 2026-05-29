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

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { formatarValor } from '../../utils/formatCurrency.js'

const props = defineProps({
  resumo: {
    type: Object,
    required: true
  }
})

const isMobile = ref(false)

const saldoClasse = computed(() => {
  if (!props.resumo) return ''
  return props.resumo.saldo >= 0 ? 'saldo-positivo' : 'saldo-negativo'
})

function onResize() {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  isMobile.value = window.innerWidth <= 768
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
})
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

@media (max-width: 768px) {
  .statement-summary {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    padding: 0 4px;
    margin-bottom: 28px;
    width: 100%;
  }

  .statement-summary::-webkit-scrollbar {
    display: none;
  }

  .summary-card {
    padding: 8px 10px;
    gap: 6px;
    border-radius: 12px;
    border-color: rgba(255, 255, 255, 0.04);
    background: rgba(255, 255, 255, 0.02);
    min-width: 0;
    overflow: hidden;
    box-sizing: border-box;
  }

  .summary-card__icon {
    font-size: 16px;
  }

  .summary-card__label {
    font-size: 8px;
    letter-spacing: 0.5px;
    opacity: 0.5;
    white-space: nowrap;
  }

  .summary-card__value {
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .summary-saldo {
    grid-column: 1 / -1;
    padding: 12px 16px;
    gap: 8px;
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.06);
  }

  .summary-saldo .summary-card__icon {
    font-size: 20px;
  }

  .summary-saldo .summary-card__value {
    font-size: 18px;
    font-weight: 700;
  }
}
</style>
