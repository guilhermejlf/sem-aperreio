import { reactive } from 'vue'

let idCounter = 0

export const toastStore = reactive({
  items: [],

  timers: {},

  add(message, opts = {}) {
    const {
      variant = 'info',
      title = null,
      duration = variant === 'error' ? 6000 : variant === 'warning' ? 5000 : 4000,
      dismissible = true,
    } = opts

    idCounter += 1
    const id = idCounter

    const toast = {
      id,
      message,
      variant,
      title,
      dismissible,
      duration,
    }

    this.items.push(toast)

    if (duration > 0) {
      this.timers[id] = setTimeout(() => {
        this.remove(id)
      }, duration)
    }

    // Limit visible toasts on mobile
    if (window.innerWidth < 768 && this.items.length > 2) {
      this.remove(this.items[0].id)
    }

    return id
  },

  pauseAll() {
    for (const id in this.timers) {
      clearTimeout(this.timers[id])
      delete this.timers[id]
    }
  },

  resumeAll() {
    for (const toast of this.items) {
      if (toast.duration > 0 && !this.timers[toast.id]) {
        this.timers[toast.id] = setTimeout(() => {
          this.remove(toast.id)
        }, toast.duration)
      }
    }
  },

  remove(id) {
    if (this.timers[id]) {
      clearTimeout(this.timers[id])
      delete this.timers[id]
    }
    const idx = this.items.findIndex(t => t.id === id)
    if (idx !== -1) {
      this.items.splice(idx, 1)
    }
  },

  success(message, opts) {
    return this.add(message, { ...opts, variant: 'success' })
  },

  error(message, opts) {
    return this.add(message, { ...opts, variant: 'error' })
  },

  warning(message, opts) {
    return this.add(message, { ...opts, variant: 'warning' })
  },

  info(message, opts) {
    return this.add(message, { ...opts, variant: 'info' })
  },
})
