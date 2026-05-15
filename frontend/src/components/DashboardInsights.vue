<template>
  <TransitionGroup
    name="insight-reveal"
    tag="div"
    class="dashboard-insights"
    v-if="insights.length > 0"
  >
    <div
      v-for="(insight, idx) in insights"
      :key="idx"
      class="insight-card"
      :class="`insight-${insight.tipo}`"
    >
      <div class="insight-glow" />
      <div class="insight-content">
        <i :class="insight.icone" />
        <span class="insight-text">{{ insight.mensagem }}</span>
      </div>
    </div>
  </TransitionGroup>
</template>

<script>
import { gerarInsights } from '../utils/dashboardInsights.js'

export default {
  name: 'DashboardInsights',
  props: {
    data: { type: Object, default: null },
  },
  computed: {
    insights() {
      return gerarInsights(this.data)
    },
  },
}
</script>

<style scoped>
.dashboard-insights {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  margin-bottom: var(--space-md);
}

.insight-card {
  position: relative;
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  overflow: hidden;
  transition: var(--transition-fast);
}

.insight-card:hover {
  transform: var(--hover-lift);
  border-color: var(--color-border-hover);
}

.insight-glow {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  transition: opacity var(--motion-fast) var(--ease-soft);
}

.insight-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.insight-content i {
  font-size: 0.9rem;
  flex-shrink: 0;
}

.insight-text {
  color: var(--color-text-primary);
}

/* Tipos */
.insight-critical .insight-glow {
  background: var(--color-danger);
  opacity: 0.08;
}
.insight-critical {
  border-color: rgba(244, 63, 94, 0.2);
}
.insight-critical i {
  color: var(--color-danger);
}

.insight-warning .insight-glow {
  background: var(--color-warning);
  opacity: 0.06;
}
.insight-warning {
  border-color: rgba(245, 158, 11, 0.2);
}
.insight-warning i {
  color: var(--color-warning);
}

.insight-info .insight-glow {
  background: var(--color-info);
  opacity: 0.06;
}
.insight-info {
  border-color: rgba(59, 130, 246, 0.15);
}
.insight-info i {
  color: var(--color-info);
}

.insight-positive .insight-glow {
  background: var(--color-success);
  opacity: 0.06;
}
.insight-positive {
  border-color: rgba(16, 185, 129, 0.15);
}
.insight-positive i {
  color: var(--color-success);
}

/* Transitions */
.insight-reveal-enter-active,
.insight-reveal-leave-active {
  transition: all var(--motion-base) var(--ease-smooth);
}

.insight-reveal-enter-from {
  opacity: 0;
  transform: translateY(6px) scale(0.98);
}

.insight-reveal-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* Mobile */
@media (max-width: 768px) {
  .dashboard-insights {
    gap: var(--space-xs);
  }
  .insight-card {
    padding: var(--space-xs) var(--space-sm);
  }
  .insight-content {
    font-size: var(--text-xs);
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .insight-reveal-enter-active,
  .insight-reveal-leave-active {
    transition: none;
  }
}
</style>
