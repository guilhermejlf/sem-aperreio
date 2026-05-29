<template>
  <div class="skeleton-dashboard">
    <!-- Period selector -->
    <div class="skeleton-row" style="justify-content: center; gap: var(--space-sm)">
      <div class="skeleton-chip" style="width: 120px; height: 36px" />
      <div class="skeleton-chip" style="width: 80px; height: 36px" />
    </div>

    <!-- Financial block -->
    <div class="skeleton-block-title" />
    <div class="skeleton-cards-row">
      <div class="skeleton-card" v-for="n in 3" :key="n">
        <div class="skeleton-text-sm" style="width: 60%" />
        <div class="skeleton-text-lg" style="width: 80%" />
      </div>
    </div>

    <!-- Charts block -->
    <div class="skeleton-block-title" />
    <div class="skeleton-charts-row">
      <div class="skeleton-chart" />
      <div class="skeleton-chart" />
    </div>

    <!-- Evolution block -->
    <div class="skeleton-block-title" />
    <div class="skeleton-chart-wide" />
  </div>
</template>

<script setup>
</script>

<style scoped>
.skeleton-dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-md);
}

.skeleton-row {
  display: flex;
}

.skeleton-chip {
  border-radius: var(--radius-md);
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    var(--color-surface-elevated) 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
}

.skeleton-block-title {
  height: 18px;
  width: 140px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-cards-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-sm);
}

.skeleton-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-text-sm {
  height: 14px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-elevated);
  opacity: 0.6;
}

.skeleton-text-lg {
  height: 24px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-elevated);
  opacity: 0.8;
}

.skeleton-charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-sm);
}

.skeleton-chart {
  height: 200px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-chart-wide {
  height: 180px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

@media (max-width: 768px) {
  .skeleton-cards-row {
    grid-template-columns: 1fr;
  }
  .skeleton-charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
