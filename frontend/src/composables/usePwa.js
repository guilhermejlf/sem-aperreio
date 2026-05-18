import { ref, onMounted, onUnmounted } from 'vue'

const isOnline = ref(navigator.onLine)
const isStandalone = ref(false)
const installPrompt = ref(null)
const showInstallCard = ref(false)

let deferredPrompt = null

export function usePwa() {
  const updateOnlineStatus = () => {
    isOnline.value = navigator.onLine
  }

  const handleBeforeInstallPrompt = (e) => {
    e.preventDefault()
    deferredPrompt = e
    installPrompt.value = e

    // Só mostra o card se o usuário já usou o app (localStorage flag)
    const hasUsed = localStorage.getItem('sa_has_used')
    const alreadyInstalled = localStorage.getItem('sa_installed')
    if (hasUsed && !alreadyInstalled && !isStandalone.value) {
      // Delay sutil para não interromper fluxo inicial
      setTimeout(() => {
        showInstallCard.value = true
      }, 3000)
    }
  }

  const installApp = async () => {
    if (!deferredPrompt) return
    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice
    if (outcome === 'accepted') {
      localStorage.setItem('sa_installed', 'true')
      showInstallCard.value = false
    }
    deferredPrompt = null
    installPrompt.value = null
  }

  const dismissInstall = () => {
    showInstallCard.value = false
    localStorage.setItem('sa_install_dismissed', Date.now().toString())
  }

  const markAsUsed = () => {
    localStorage.setItem('sa_has_used', 'true')
  }

  onMounted(() => {
    isStandalone.value =
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true

    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  })

  onUnmounted(() => {
    window.removeEventListener('online', updateOnlineStatus)
    window.removeEventListener('offline', updateOnlineStatus)
    window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  })

  return {
    isOnline,
    isStandalone,
    showInstallCard,
    installApp,
    dismissInstall,
    markAsUsed,
  }
}
