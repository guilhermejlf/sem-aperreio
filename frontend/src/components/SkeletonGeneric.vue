<template>
  <div class="skeleton-generic">
    <div class="skeleton-card" v-for="n in count" :key="n">
      <div class="skeleton-header">
        <div class="skeleton-avatar-sm" />
        <div class="skeleton-lines">
          <div class="skeleton-line" style="width: 60%" />
          <div class="skeleton-line-sm" style="width: 40%" />
        </div>
      </div>
      <div class="skeleton-body">
        <div class="skeleton-line" style="width: 90%" />
        <div class="skeleton-line" style="width: 70%" />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  count: { type: Number, default: 3 },
})
</script>

<style scoped>
.skeleton-generic {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-sm);
}

.skeleton-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  animation: shimmer var(--shimmer-duration) ease-in-out infinite;
  background-image: linear-gradient(90deg, var(--color-surface) 25%, var(--color-surface-elevated) 50%, var(--color-surface) 75%);
  background-size: 200% 100%;
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.skeleton-avatar-sm {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-surface-elevated);
  opacity: 0.5;
  flex-shrink: 0;
}

.skeleton-lines {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  flex: 1;
}

.skeleton-line {
  height: 14px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-elevated);
  opacity: 0.6;
}

.skeleton-line-sm {
  height: 12px;
  border-radius: var(--radius-sm);
  background: var(--color-surface-elevated);
  opacity: 0.4;
}

.skeleton-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding-top: var(--space-xs);
}
</style>
