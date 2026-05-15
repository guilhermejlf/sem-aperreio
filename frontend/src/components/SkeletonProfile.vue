<template>
  <div class="skeleton-profile">
    <div class="skeleton-avatar" />
    <div class="skeleton-text" style="width: 50%; height: 20px; margin: 0 auto" />
    <div class="skeleton-text" style="width: 70%; height: 14px; margin: 0 auto" />
    <div class="skeleton-divider" />
    <div class="skeleton-field" v-for="n in 4" :key="n">
      <div class="skeleton-text-sm" style="width: 30%" />
      <div class="skeleton-text" style="width: 60%" />
    </div>
  </div>
</template>

<script>
export default { name: 'SkeletonProfile' }
</script>

<style scoped>
.skeleton-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-lg);
}

.skeleton-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-text {
  height: 16px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-text-sm {
  height: 12px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-elevated);
  opacity: 0.5;
}

.skeleton-divider {
  width: 100%;
  height: 1px;
  background: var(--color-border);
  margin: var(--space-sm) 0;
}

.skeleton-field {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-sm) 0;
}
</style>
