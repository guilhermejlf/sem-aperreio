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
    z-index: 1000;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background: rgba(15, 23, 42, 0.92);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: env(safe-area-inset-bottom);
  }
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 4px;
  background: none;
  border: none;
  color: rgba(248, 250, 252, 0.58);
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  min-height: 56px;
}

.bottom-nav-item i {
  font-size: 20px;
  transition: all 0.25s ease;
}

.bottom-nav-item.active {
  color: #60A637;
}

.bottom-nav-item.active i {
  filter: drop-shadow(0 0 6px rgba(96, 166, 55, 0.25));
}
</style>
