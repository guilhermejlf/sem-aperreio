import * as Sentry from '@sentry/vue'
import { BrowserTracing } from '@sentry/browser'

const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || ''
const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT || 'development'
const RELEASE = import.meta.env.VITE_RELEASE || 'unknown'

export function initSentry(app) {
  if (!SENTRY_DSN) {
    console.info('[Sentry] DSN não configurado — skipping initialization')
    return
  }

  Sentry.init({
    app,
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    release: RELEASE,
    integrations: [
      new BrowserTracing({
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
      // Filtra dados sensíveis
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
