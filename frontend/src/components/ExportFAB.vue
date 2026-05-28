<template>
  <div class="export-fab-wrapper">
    <button
      class="export-fab"
      @click="toggleDropdown"
      ref="exportBtn"
      title="Exportar"
    >
      <i class="pi pi-download"></i>
    </button>
    <Transition name="fade">
      <div v-if="showDropdown" class="export-menu" ref="exportDropdown">
        <button @click="emitExport('csv')">
          <i class="pi pi-file-export"></i> CSV
        </button>
        <button @click="emitExport('xlsx')">
          <i class="pi pi-file-excel"></i> Excel
        </button>
        <button @click="emitExport('pdf')">
          <i class="pi pi-file-pdf"></i> PDF
        </button>
      </div>
    </Transition>
  </div>
</template>

<script>
export default {
  name: 'ExportFAB',

  emits: ['export'],

  data() {
    return {
      showDropdown: false,
    }
  },

  mounted() {
    document.addEventListener('click', this.closeDropdown)
  },

  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdown)
  },

  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown
    },

    closeDropdown(e) {
      if (
        this.$refs.exportDropdown &&
        !this.$refs.exportDropdown.contains(e.target) &&
        !this.$refs.exportBtn.contains(e.target)
      ) {
        this.showDropdown = false
      }
    },

    emitExport(formato) {
      this.showDropdown = false
      this.$emit('export', formato)
    },
  },
}
</script>

<style scoped>
.export-fab-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}

.export-fab {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #94a3b8;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
}

.export-fab:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
  transform: translateY(-1px);
}

.export-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 6px;
  min-width: 160px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.export-menu button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #cbd5e1;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
}

.export-menu button:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #e5e7eb;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

@media (max-width: 768px) {
  .export-fab-wrapper {
    display: none;
  }
}
</style>
