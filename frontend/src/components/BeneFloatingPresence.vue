<template>
  <div class="bene-presence">
    <!-- Micro tooltip -->
    <Transition name="bene-tooltip">
      <div
        v-if="hasInsight"
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

const INITIAL_DELAY = 8000
const CYCLE_INTERVAL = 45000

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
    // Primeiro insight após delay inicial
    setTimeout(() => {
      this.showRandomInsight()
      this.startCycle()
    }, INITIAL_DELAY)
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
      if (this.chatOpen) return
      const variants = ['neutral', 'info', 'success', 'warning']
      const weights = [0.35, 0.25, 0.25, 0.15]
      const variant = this.weightedPick(variants, weights)
      this.store.showInsight(variant)
    },
    startCycle() {
      this.cycleTimer = setInterval(() => {
        if (!this.chatOpen && !this.store.currentInsight) {
          this.showRandomInsight()
        }
      }, CYCLE_INTERVAL)
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
    bottom: 16px;
    right: 16px;
  }
}
</style>
