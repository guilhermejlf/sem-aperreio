<template>
  <div v-if="settingsStore.bene.showPresence" class="bene-presence">
    <!-- Micro tooltip -->
    <Transition name="bene-tooltip">
      <div
        v-if="hasInsight && settingsStore.bene.showInsights"
        class="bene-presence__tooltip-wrapper"
      >
        <BeneInsight
          :message="currentInsight.message"
          :variant="currentInsight.variant"
          :visible="true"
          @click="openChat"
        />
      </div>
    </Transition>

    <!-- Avatar button -->
    <div
      class="bene-presence__avatar-wrapper"
      @click="openChat"
      title="Falar com Seu Bené"
    >
      <BeneAvatar
        size="floating"
        :breathing="!chatOpen"
      />
    </div>
  </div>
</template>

<script>
import { toRaw } from 'vue'
import BeneAvatar from './BeneAvatar.vue'
import BeneInsight from './BeneInsight.vue'
import beneStore from '../stores/beneContext.store.js'
import { settingsStore } from '../stores/settings.store.js'

const FREQ_DELAYS = { low: 18000, normal: 8000, high: 4000 }
const FREQ_CYCLES = { low: 75000, normal: 45000, high: 25000 }

export default {
  name: 'BeneFloatingPresence',
  components: { BeneAvatar, BeneInsight },
  props: {
    chatOpen: { type: Boolean, default: false },
  },
  emits: ['open-chat'],
  data() {
    return {
      store: beneStore,
      cycleTimer: null,
    }
  },
  computed: {
    hasInsight() {
      return !!this.store.currentInsight
    },
    currentInsight() {
      return this.store.currentInsight
    },
  },
  mounted() {
    if (!settingsStore.bene.showPresence) return
    const delay = FREQ_DELAYS[settingsStore.bene.frequency] || FREQ_DELAYS.normal
    setTimeout(() => {
      this.showRandomInsight()
      this.startCycle()
    }, delay)
  },
  beforeUnmount() {
    clearInterval(this.cycleTimer)
    this.store.dismiss()
  },
  methods: {
    openChat() {
      this.store.openChat()
      this.$emit('open-chat')
    },
    showRandomInsight() {
      if (this.chatOpen || !settingsStore.bene.showInsights) return
      const variants = ['neutral', 'info', 'success', 'warning']
      const weights = [0.35, 0.25, 0.25, 0.15]
      const variant = this.weightedPick(variants, weights)
      this.store.showInsight(variant)
    },
    startCycle() {
      const cycle = FREQ_CYCLES[settingsStore.bene.frequency] || FREQ_CYCLES.normal
      this.cycleTimer = setInterval(() => {
        if (!this.chatOpen && !this.store.currentInsight) {
          this.showRandomInsight()
        }
      }, cycle)
    },
    weightedPick(items, weights) {
      const total = weights.reduce((a, b) => a + b, 0)
      let random = Math.random() * total
      for (let i = 0; i < items.length; i++) {
        random -= weights[i]
        if (random <= 0) return items[i]
      }
      return items[items.length - 1]
    },
  },
}
</script>

<style scoped>
.bene-presence {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1996;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  pointer-events: none;
}

.bene-presence > * {
  pointer-events: auto;
}

.bene-presence__tooltip-wrapper {
  margin-bottom: 2px;
}

.bene-presence__avatar-wrapper {
  cursor: pointer;
}

/* Transitions */
.bene-tooltip-enter-active,
.bene-tooltip-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.bene-tooltip-enter-from {
  opacity: 0;
  transform: translateY(6px) scale(0.96);
}

.bene-tooltip-leave-to {
  opacity: 0;
  transform: translateY(4px) scale(0.98);
}

@media (max-width: 768px) {
  .bene-presence {
    bottom: calc(72px + env(safe-area-inset-bottom));
    right: 16px;
  }
}
</style>
