<template>
  <div class="checklist-card">
    <div class="checklist-header">
      <div>
        <h3 class="checklist-title">Configure teu Sem Aperreio</h3>
        <p class="checklist-subtitle">
          Complete os primeiros passos para desbloquear todo o potencial.
        </p>
      </div>
      <button v-if="allDone" class="btn-dismiss" @click="emit('dismiss')">
        <i class="pi pi-times"></i>
      </button>
    </div>

    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progress + '%' }"></div>
    </div>
    <div class="progress-text">{{ completedCount }}/4 concluídos</div>

    <div class="checklist-items">
      <div
        v-for="item in items"
        :key="item.key"
        :class="['checklist-item', { done: item.done }]"
      >
        <div class="check-circle">
          <i v-if="item.done" class="pi pi-check"></i>
        </div>
        <span class="check-label">{{ item.label }}</span>
      </div>
    </div>

    <div v-if="allDone" class="celebration">
      <div class="celebration-emoji">🎉</div>
      <p class="celebration-text">Tudo pronto! Teu Sem Aperreio já está configurado.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: Object,
    default: () => ({
      group_created: false,
      first_expense: false,
      first_revenue: false,
      first_goal: false,
      progress: 0,
    })
  }
})

const emit = defineEmits(['dismiss'])

const items = computed(() => [
  { key: 'group', label: 'Criar ou entrar em um grupo familiar', done: props.status.group_created },
  { key: 'expense', label: 'Registrar primeiro gasto', done: props.status.first_expense },
  { key: 'revenue', label: 'Registrar primeira receita', done: props.status.first_revenue },
  { key: 'goal', label: 'Criar primeira meta', done: props.status.first_goal },
])

const completedCount = computed(() =>
  items.value.filter(i => i.done).length
)

const progress = computed(() =>
  Math.round((completedCount.value / 4) * 100)
)

const allDone = computed(() => completedCount.value === 4)
</script>

<style scoped>
.checklist-card {
  background: rgba(11, 18, 32, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.checklist-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.checklist-title {
  font-size: 16px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px;
}

.checklist-subtitle {
  font-size: 13px;
  color: rgba(148, 163, 184, 0.7);
  margin: 0;
}

.btn-dismiss {
  background: none;
  border: none;
  color: rgba(148, 163, 184, 0.5);
  cursor: pointer;
  padding: 4px;
  font-size: 14px;
  transition: color 0.2s;
}

.btn-dismiss:hover {
  color: rgba(255, 255, 255, 0.7);
}

.progress-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 6px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #60A637, #7bc55a);
  border-radius: 3px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-text {
  font-size: 12px;
  color: rgba(148, 163, 184, 0.6);
  margin-bottom: 16px;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
}

.checklist-item.done {
  background: rgba(96, 166, 55, 0.06);
  border-color: rgba(96, 166, 55, 0.12);
}

.check-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 10px;
  color: #60A637;
  transition: all 0.2s ease;
}

.checklist-item.done .check-circle {
  border-color: #60A637;
  background: rgba(96, 166, 55, 0.15);
}

.check-label {
  font-size: 13px;
  color: rgba(226, 232, 240, 0.85);
  transition: color 0.2s;
}

.checklist-item.done .check-label {
  color: rgba(148, 163, 184, 0.6);
  text-decoration: line-through;
}

.celebration {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
  animation: fadeIn 0.5s ease;
}

.celebration-emoji {
  font-size: 28px;
  margin-bottom: 6px;
}

.celebration-text {
  font-size: 13px;
  color: rgba(148, 163, 184, 0.8);
  margin: 0;
}
</style>
