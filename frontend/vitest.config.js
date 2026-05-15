import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.test.js'],
    coverage: {
      reporter: ['text', 'html'],
      include: ['src/**/*.vue', 'src/**/*.js'],
      exclude: ['src/**/*.test.js', 'node_modules/'],
    },
  },
})
