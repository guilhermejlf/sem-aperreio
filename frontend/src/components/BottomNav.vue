<template>
  <nav class="bottom-nav">
    <button
      v-for="item in items"
      :key="item.tab"
      :class="['bottom-nav-item', { active: activeTab === item.tab }]"
      @click="$emit('navigate', item.tab)"
    >
      <i :class="item.icon"></i>
      <span>{{ item.label }}</span>
    </button>
  </nav>
</template>

<script>
export default {
  name: 'BottomNav',
  props: {
    activeTab: {
      type: String,
      required: true
    }
  },
  emits: ['navigate'],
  data() {
    return {
      items: [
        { tab: 'dashboard', label: 'Painel', icon: 'pi pi-home' },
        { tab: 'extrato', label: 'Extrato', icon: 'pi pi-list' },
        { tab: 'gastos', label: 'Despesas', icon: 'pi pi-arrow-up-right' },
        { tab: 'receitas', label: 'Receitas', icon: 'pi pi-chart-line' },
        { tab: 'metas', label: 'Metas', icon: 'pi pi-bullseye' },
        { tab: 'grupo', label: 'Grupo', icon: 'pi pi-users' },
      ]
    }
  }
}
</script>

<style scoped>
.bottom-nav {
  display: none;
}

@media (max-width: 768px) {
  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: var(--z-bottom-nav);
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: var(--mobile-header-height);
    background: var(--bg-surface);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-top: var(--glass-border);
    padding-bottom: var(--safe-bottom);
  }
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 6px 2px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: var(--font-xs);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-base);
}

.bottom-nav-item i {
  font-size: 22px;
  transition: all var(--transition-base);
}

.bottom-nav-item.active {
  color: var(--color-primary);
}

.bottom-nav-item.active i {
  filter: drop-shadow(0 0 4px var(--color-primary-glow));
}
</style>
