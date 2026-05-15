import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks(id) {
          // PrimeVue e PrimeIcons em chunk separado
          if (id.includes('primevue') || id.includes('primeicons')) {
            return 'prime'
          }
          // Chart.js em chunk separado
          if (id.includes('chart.js')) {
            return 'charts'
          }
          // Vendor libraries
          if (id.includes('node_modules')) {
            return 'vendor'
          }
        }
      }
    }
  }
})
