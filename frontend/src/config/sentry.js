import * as Sentry from '@sentry/vue'
import { browserTracingIntegration } from '@sentry/vue'

const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || ''
const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT || 'development'
const RELEASE = import.meta.env.VITE_RELEASE || 'sem-aperreio@v2.1.0'

// Filtros de ruido conhecidos
const NOISE_PATTERNS = [
  'ResizeObserver loop limit exceeded',
  'ResizeObserver loop completed with undelivered notifications',
  'Non-Error promise rejection captured',
  'Cannot redefine property: googletag',
  'window.__REACT_DEVTOOLS_GLOBAL_HOOK__',
  'Extension context invalidated',
  'The fetching process for the media resource',
  'NetworkError when attempting to fetch resource',
  'The operation was aborted',
  'The user aborted a request',
]

function isNoiseEvent(event) {
  try {
    const values = event.exception?.values || []
    for (const value of values) {
      const excValue = value.value || ''
      const excType = value.type || ''

      for (const pattern of NOISE_PATTERNS) {
        if (excValue.includes(pattern)) return true
      }

      // Ignorar AbortError benigno (usuario cancelou request)
      if (excType === 'AbortError') return true

      // Ignorar erros de extensoes
      const frames = value.stacktrace?.frames || []
      for (const frame of frames) {
        const filename = frame.filename || ''
        if (filename.includes('chrome-extension://') || filename.includes('moz-extension://')) {
          return true
        }
        if (filename.includes('google-analytics') || filename.includes('googletagmanager')) {
          return true
        }
      }
    }
  } catch (e) {
    // Nunca quebrar o Sentry por causa do filtro
  }
  return false
}

export function initSentry(app) {
  if (!SENTRY_DSN) {
    console.info('[Sentry] DSN nao configurado — skipping initialization')
    return
  }

  Sentry.init({
    app,
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    release: RELEASE,
    integrations: [
      browserTracingIntegration({
        tracePropagationTargets: [
          /^https:\/\/campo-valor-production\.up\.railway\.app\/api/,
          /^http:\/\/127\.0\.0\.1:8000/,
        ],
      }),
    ],
    tracesSampleRate: parseFloat(import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || '0.1'),
    replaysSessionSampleRate: 0,
    replaysOnErrorSampleRate: 0,
    attachStacktrace: true,
    beforeSend(event) {
      // Filtrar ruido
      if (isNoiseEvent(event)) return null

      // Filtrar dados sensiveis
      if (event.exception) {
        const values = event.exception.values || []
        for (const value of values) {
          const frames = value.stacktrace?.frames || []
          for (const frame of frames) {
            if (frame.vars) {
              for (const key of Object.keys(frame.vars)) {
                if (/password|token|secret|key|auth/i.test(key)) {
                  frame.vars[key] = '[FILTERED]'
                }
              }
            }
          }
        }
      }
      return event
    },
  })

  console.info(`[Sentry] Initialized — env=${ENVIRONMENT}, release=${RELEASE}`)
}

export function captureError(error, context = {}) {
  Sentry.captureException(error, { extra: context })
}

export function captureMessage(message, level = 'info') {
  Sentry.captureMessage(message, level)
}
