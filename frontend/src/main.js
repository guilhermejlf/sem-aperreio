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

// brand design system
import './styles/brand.css'

const app = createApp(App)

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
})

app.use(ConfirmationService)

app.config.globalProperties.$toast = toastStore

app.mount('#app')