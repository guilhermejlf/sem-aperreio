import { captureMessage, captureError } from '../config/sentry.js'

const PWA_METRICS = {
  installPromptShown: 0,
  installAccepted: 0,
  installDismissed: 0,
  offlineOpens: 0,
  onlineSwitches: 0,
  syncFailures: 0,
  swErrors: 0,
}

/**
 * Inicializa observabilidade do PWA e modo offline
 */
export function initPwaObservability() {
  // Monitorar mudanças de conectividade
  window.addEventListener('online', () => {
    PWA_METRICS.onlineSwitches++
    console.info('[PWA] Back online')
    captureMessage('Device back online', 'info')
  })

  window.addEventListener('offline', () => {
    PWA_METRICS.offlineOpens++
    console.info('[PWA] Went offline')
    captureMessage('Device went offline', 'info')
  })

  // Monitorar service worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('error', (event) => {
      PWA_METRICS.swErrors++
      console.error('[PWA] Service Worker error:', event.error)
      captureError(event.error, { context: 'service_worker' })
    })

    navigator.serviceWorker.addEventListener('controllerchange', () => {
      console.info('[PWA] Service Worker controller changed')
      captureMessage('Service Worker controller changed', 'info')
    })
  }

  // Monitorar beforeinstallprompt
  window.addEventListener('beforeinstallprompt', (e) => {
    PWA_METRICS.installPromptShown++
    console.info('[PWA] Install prompt shown')
    captureMessage('PWA install prompt shown', 'info')
  })

  // Monitorar appinstalled
  window.addEventListener('appinstalled', () => {
    PWA_METRICS.installAccepted++
    console.info('[PWA] App installed')
    captureMessage('PWA app installed', 'info')
  })

  // Monitorar IndexedDB errors
  window.addEventListener('error', (event) => {
    if (event.message?.includes('IndexedDB') || event.message?.includes('IDBDatabase')) {
      console.error('[PWA] IndexedDB error:', event.message)
      captureError(new Error(event.message), { context: 'indexeddb' })
    }
  })

  // Monitorar sync failures (se Background Sync API disponível)
  if ('sync' in navigator) {
    navigator.serviceWorker?.ready?.then((registration) => {
      // Background sync observability é tratada pelo service worker
      console.info('[PWA] Background Sync available')
    }).catch((err) => {
      console.warn('[PWA] Background Sync not available:', err)
    })
  }
}

/**
 * Registra que o usuário aceitou a instalação
 */
export function trackInstallAccepted() {
  PWA_METRICS.installAccepted++
}

/**
 * Registra que o usuário dispensou o prompt de instalação
 */
export function trackInstallDismissed() {
  PWA_METRICS.installDismissed++
}

/**
 * Registra falha de sync
 */
export function trackSyncFailure(error) {
  PWA_METRICS.syncFailures++
  captureError(error, { context: 'sync_failure' })
}

/**
 * Retorna métricas do PWA
 */
export function getPwaMetrics() {
  return {
    ...PWA_METRICS,
    isOnline: navigator.onLine,
    serviceWorkerSupported: 'serviceWorker' in navigator,
    syncSupported: 'sync' in navigator,
  }
}
