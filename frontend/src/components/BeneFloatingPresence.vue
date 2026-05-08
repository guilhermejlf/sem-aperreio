<template>
  <div class="bene-presence">
    <!-- Insight bubble -->
    <Transition name="bene-insight-fade">
      <div
        v-if="hasInsight"
        class="bene-presence__insight-wrapper"
      >
        <BeneInsight
          :message="currentInsight.message"
          :variant="currentInsight.variant"
          :visible="true"
          dismissible
          @click="openChat"
          @dismiss="dismissInsight"
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
    dismissInsight() {
      this.store.dismiss()
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
  gap: 10px;
  pointer-events: none;
}

.bene-presence > * {
  pointer-events: auto;
}

.bene-presence__insight-wrapper {
  margin-bottom: 4px;
}

.bene-presence__avatar-wrapper {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.bene-presence__avatar-wrapper:hover {
  transform: scale(1.05);
}

.bene-presence__avatar-wrapper:active {
  transform: scale(0.97);
}

/* Transitions */
.bene-insight-fade-enter-active,
.bene-insight-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.bene-insight-fade-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.92);
}

.bene-insight-fade-leave-to {
  opacity: 0;
  transform: translateY(6px) scale(0.95);
}

@media (max-width: 768px) {
  .bene-presence {
    bottom: 16px;
    right: 16px;
  }
}
</style>
