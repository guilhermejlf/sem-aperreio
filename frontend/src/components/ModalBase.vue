<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click.self="onClose">
        <div class="modal-card" :class="[`modal-${size}`]">
          <!-- Header -->
          <div class="modal-header">
            <div class="modal-title-group">
              <h2 v-if="title" class="modal-title">
                <template v-if="highlight">
                  {{ titleBefore }}<span class="modal-highlight">{{ highlight }}</span>{{ titleAfter }}
                </template>
                <template v-else>{{ title }}</template>
              </h2>
              <p v-if="subtitle" class="modal-subtitle">{{ subtitle }}</p>
            </div>
            <button class="modal-close" @click="onClose" aria-label="Fechar">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 3L13 13M3 13L13 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: 'ModalBase',
  props: {
    visible: { type: Boolean, default: false },
    title: { type: String, default: '' },
    highlight: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    size: { type: String, default: 'medium', validator: v => ['small', 'medium', 'large'].includes(v) }
  },
  emits: ['close'],
  computed: {
    titleBefore() {
      if (!this.highlight) return this.title
      const idx = this.title.indexOf(this.highlight)
      if (idx === -1) return this.title
      return this.title.slice(0, idx)
    },
    titleAfter() {
      if (!this.highlight) return ''
      const idx = this.title.indexOf(this.highlight)
      if (idx === -1) return ''
      return this.title.slice(idx + this.highlight.length)
    }
  },
  methods: {
    onClose() {
      this.$emit('close')
    }
  },
  mounted() {
    document.addEventListener('keydown', this.handleEsc)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEsc)
  },
  methods: {
    handleEsc(e) {
      if (e.key === 'Escape' && this.visible) {
        this.onClose()
      }
    },
    onClose() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
/* Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: var(--bg-glass);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  padding: var(--space-5);
}

/* Card */
.modal-card {
  background: var(--bg-surface);
  backdrop-filter: var(--glass-blur);
  border: var(--glass-border);
  border-radius: var(--radius-xl);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.03),
    var(--shadow-card);
  padding: var(--space-7);
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.modal-small {
  max-width: 420px;
}

.modal-medium {
  max-width: 540px;
}

.modal-large {
  max-width: 720px;
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
  gap: var(--space-4);
}

.modal-title-group {
  flex: 1;
  min-width: 0;
}

.modal-title {
  margin: 0;
  font-size: 32px;
  font-weight: var(--weight-bold);
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  word-break: break-word;
}

.modal-highlight {
  color: var(--color-primary);
}

.modal-subtitle {
  margin: 6px 0 0;
  font-size: var(--font-sm);
  font-weight: 400;
  line-height: 1.5;
  color: var(--text-secondary);
}

/* Close Button */
.modal-close {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(8px);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.07);
}

/* Body */
.modal-body {
  flex: 1;
  min-height: 0;
}

/* Footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-7);
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: all var(--transition-base);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-card,
.modal-leave-to .modal-card {
  transform: scale(0.95);
  opacity: 0;
}

/* Mobile */
@media (max-width: 640px) {
  .modal-card {
    padding: var(--space-6);
    border-radius: var(--radius-lg);
  }

  .modal-title {
    font-size: 26px;
  }

  .modal-overlay {
    padding: var(--space-4);
  }
}
</style>
