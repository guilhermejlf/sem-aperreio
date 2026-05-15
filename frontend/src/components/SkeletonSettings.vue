<template>
  <div class="skeleton-settings">
    <div class="skeleton-section" v-for="s in 3" :key="s">
      <div class="skeleton-section-title" />
      <div class="skeleton-row" v-for="n in 3" :key="n">
        <div class="skeleton-text" style="width: 40%" />
        <div class="skeleton-toggle" />
      </div>
    </div>
  </div>
</template>

<script>
export default { name: 'SkeletonSettings' }
</script>

<style scoped>
.skeleton-settings {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  padding: var(--space-md);
}

.skeleton-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.skeleton-section-title {
  height: 16px;
  width: 100px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) 0;
}

.skeleton-text {
  height: 14px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-toggle {
  width: 40px;
  height: 22px;
  border-radius: 11px;
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}
</style>
