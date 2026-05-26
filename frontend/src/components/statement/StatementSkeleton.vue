<template>
  <div class="statement-skeleton">
    <!-- Summary skeleton -->
    <div class="skeleton-summary">
      <div v-for="i in 3" :key="i" class="skeleton-card">
        <div class="skeleton-icon shimmer"></div>
        <div class="skeleton-text">
          <div class="skeleton-label shimmer"></div>
          <div class="skeleton-value shimmer"></div>
        </div>
      </div>
    </div>

    <!-- Timeline groups skeleton -->
    <div class="skeleton-groups">
      <div v-for="g in 3" :key="g" class="skeleton-group">
        <div class="skeleton-group-header shimmer"></div>
        <div class="skeleton-items">
          <div v-for="i in 3" :key="i" class="skeleton-item">
            <div class="skeleton-item-icon shimmer"></div>
            <div class="skeleton-item-content">
              <div class="skeleton-item-title shimmer"></div>
              <div class="skeleton-item-meta shimmer"></div>
            </div>
            <div class="skeleton-item-value shimmer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatementSkeleton'
}
</script>

<style scoped>
.statement-skeleton {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Summary */
.skeleton-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.skeleton-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.skeleton-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
}

.skeleton-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.skeleton-label {
  width: 60px;
  height: 10px;
  border-radius: 4px;
}

.skeleton-value {
  width: 100px;
  height: 18px;
  border-radius: 4px;
}

/* Groups */
.skeleton-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-group-header {
  width: 100px;
  height: 14px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.skeleton-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.skeleton-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.skeleton-item-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  flex-shrink: 0;
}

.skeleton-item-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.skeleton-item-title {
  width: 60%;
  height: 14px;
  border-radius: 4px;
}

.skeleton-item-meta {
  width: 40%;
  height: 10px;
  border-radius: 4px;
}

.skeleton-item-value {
  width: 70px;
  height: 14px;
  border-radius: 4px;
  flex-shrink: 0;
}

/* Shimmer effect */
.shimmer {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.03) 0%,
    rgba(255, 255, 255, 0.07) 50%,
    rgba(255, 255, 255, 0.03) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite ease-in-out;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .shimmer {
    animation: none;
    background: rgba(255, 255, 255, 0.03);
  }
}

@media (max-width: 768px) {
  .skeleton-summary {
    display: flex;
    overflow-x: auto;
    gap: 10px;
  }

  .skeleton-card {
    flex: 0 0 140px;
    min-width: 140px;
  }
}
</style>
