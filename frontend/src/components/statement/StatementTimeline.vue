<template>
  <div class="statement-timeline">
    <StatementGroup
      v-for="(grupo, index) in grupos"
      :key="grupo.titulo"
      :titulo="grupo.titulo"
      :total="calcularTotal(grupo.itens)"
      :style="getStaggerDelay(index)"
    >
      <StatementItem
        v-for="item in grupo.itens"
        :key="`${item.tipo}-${item.id}`"
        :item="item"
        :categorias="categorias"
      />
    </StatementGroup>
  </div>
</template>

<script>
import StatementGroup from './StatementGroup.vue'
import StatementItem from './StatementItem.vue'
import { groupByTimeline } from '../../utils/timeline.js'

export default {
  name: 'StatementTimeline',

  components: { StatementGroup, StatementItem },

  props: {
    itens: {
      type: Array,
      required: true
    },
    categorias: {
      type: Array,
      default: () => []
    }
  },

  computed: {
    grupos() {
      return groupByTimeline(this.itens)
    }
  },

  methods: {
    calcularTotal(itens) {
      return itens.reduce((acc, item) => {
        const valor = parseFloat(item.valor || 0)
        return item.tipo === 'receita' ? acc + valor : acc - valor
      }, 0)
    },

    getStaggerDelay(index) {
      return { '--stagger-delay': `${index * 50}ms` }
    }
  }
}
</script>

<style scoped>
.statement-timeline {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.statement-timeline > * {
  animation: fadeInUp 0.4s ease var(--stagger-delay, 0ms) both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .statement-timeline > * {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
</style>
