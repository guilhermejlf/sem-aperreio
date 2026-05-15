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
      :style="{ '--stagger-delay': `${idx * 60}ms` }"
    >
      <div class="insight-glow" />
      <div class="insight-content">
        <div class="insight-icon-wrap">
          <i :class="insight.icone" />
        </div>
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
  gap: 7px;
  margin-bottom: var(--space-lg);
}

.insight-card {
  position: relative;
  border-radius: var(--radius-md);
  padding: 11px 16px;
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
  opacity: 0.05;
  transition: opacity var(--motion-fast) var(--ease-soft);
}

.insight-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: var(--text-sm);
  line-height: 1.5;
}

.insight-icon-wrap {
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--color-surface-elevated);
}

.insight-icon-wrap i {
  font-size: 0.8rem;
}

.insight-text {
  color: var(--color-text-primary);
}

/* Tipos */
.insight-critical .insight-glow {
  background: var(--color-danger);
  opacity: 0.1;
}
.insight-critical {
  border-color: rgba(244, 63, 94, 0.18);
}
.insight-critical .insight-icon-wrap {
  background: rgba(244, 63, 94, 0.1);
}
.insight-critical .insight-icon-wrap i {
  color: var(--color-danger);
}

.insight-warning .insight-glow {
  background: var(--color-warning);
  opacity: 0.08;
}
.insight-warning {
  border-color: rgba(245, 158, 11, 0.15);
}
.insight-warning .insight-icon-wrap {
  background: rgba(245, 158, 11, 0.08);
}
.insight-warning .insight-icon-wrap i {
  color: var(--color-warning);
}

.insight-info .insight-glow {
  background: var(--color-info);
  opacity: 0.07;
}
.insight-info {
  border-color: rgba(59, 130, 246, 0.12);
}
.insight-info .insight-icon-wrap {
  background: rgba(59, 130, 246, 0.07);
}
.insight-info .insight-icon-wrap i {
  color: var(--color-info);
}

.insight-positive .insight-glow {
  background: var(--color-success);
  opacity: 0.07;
}
.insight-positive {
  border-color: rgba(16, 185, 129, 0.12);
}
.insight-positive .insight-icon-wrap {
  background: rgba(16, 185, 129, 0.07);
}
.insight-positive .insight-icon-wrap i {
  color: var(--color-success);
}

/* Hierarquia dinâmica futura — insight protagonista */
.insight-card.primary {
  padding: 13px 18px;
  border-left: 3px solid rgba(96, 166, 55, 0.35);
}

.insight-card.primary .insight-glow {
  opacity: 0.08;
}

/* Staggered reveal */
.insight-reveal-enter-active {
  transition: all var(--motion-base) var(--ease-smooth);
  transition-delay: var(--stagger-delay, 0ms);
}

.insight-reveal-leave-active {
  transition: all var(--motion-fast) var(--ease-standard);
}

.insight-reveal-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.insight-reveal-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* Mobile */
@media (max-width: 768px) {
  .dashboard-insights {
    gap: 6px;
    margin-bottom: var(--space-md);
  }
  .insight-card {
    padding: 9px 12px;
    border-radius: var(--radius-sm);
  }
  .insight-content {
    font-size: var(--text-xs);
    gap: 8px;
  }
  .insight-icon-wrap {
    width: 22px;
    height: 22px;
  }
  .insight-icon-wrap i {
    font-size: 0.7rem;
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
