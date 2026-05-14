import { reactive, watch } from 'vue'

const STORAGE_KEY = 'sem_aperreio_settings_v1'

const DEFAULTS = {
  theme: 'dark',
  themeDark: true,
  notifications: {
    weeklyReminder: true,
    budgetAlerts: true,
    averageAlerts: true,
    beneInsights: true,
  },
  bene: {
    showInsights: true,
    showPresence: true,
    frequency: 'normal',
  },
  privacy: {
    exportData: false,
  },
  experience: {
    smoothAnimations: true,
    reduceMotion: false,
  },
}

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return { ...DEFAULTS, ...JSON.parse(raw) }
  } catch { /* ignore */ }
  return { ...DEFAULTS }
}

function saveToStorage(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch { /* ignore */ }
}

export const settingsStore = reactive(loadFromStorage())

watch(settingsStore, (val) => {
  saveToStorage(val)
}, { deep: true })

export function resetSettings() {
  Object.assign(settingsStore, DEFAULTS)
}
