import { createApp } from 'vue'
import App from './App.vue'

import PrimeVue from 'primevue/config'
import ConfirmationService from 'primevue/confirmationservice'
import Aura from '@primevue/themes/aura'
import { toastStore } from './stores/toast.store.js'

// ícones
import 'primeicons/primeicons.css'

// design tokens (foundation)
import './styles/tokens.css'

// motion system
import './styles/motion.css'

// brand design system
import './styles/brand.css'

// Registrar Service Worker gerado pelo VitePWA
if ('serviceWorker' in navigator) {
  // Limpar caches antigos uma vez (migração de SW residual)
  if ('caches' in window && !sessionStorage.getItem('sw-cache-cleared')) {
    caches.keys().then(names => {
      for (const name of names) {
        caches.delete(name)
        console.log('[SW] Cache antigo deletado:', name)
      }
      sessionStorage.setItem('sw-cache-cleared', '1')
    })
  }
  // O VitePWA injeta o registrador automaticamente no build de produção.
  // Em dev, usamos o devOptions.enabled para testar.
}

const app = createApp(App)

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
})

app.use(ConfirmationService)

app.config.globalProperties.$toast = toastStore

app.mount('#app')