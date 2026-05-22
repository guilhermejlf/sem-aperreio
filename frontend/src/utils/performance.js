import { captureMessage, captureError } from '../config/sentry.js'

const METRICS = {
  fcp: 0,
  tti: 0,
  apiLatency: {},
  chartRenderTime: 0,
}

/**
 * Inicializa monitoramento de performance
 */
export function initPerformanceMonitoring() {
  // Web Vitals: First Contentful Paint
  if ('PerformanceObserver' in window) {
    try {
      const fcpObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.name === 'first-contentful-paint') {
            METRICS.fcp = Math.round(entry.startTime)
            console.info(`[Performance] FCP: ${METRICS.fcp}ms`)

            if (METRICS.fcp > 3000) {
              captureMessage(`Slow FCP: ${METRICS.fcp}ms`, 'warning')
            }
          }
        }
      })
      fcpObserver.observe({ entryTypes: ['paint'] })
    } catch (e) {
      // Paint Timing API não suportado
    }

    // Largest Contentful Paint
    try {
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries()
        const lastEntry = entries[entries.length - 1]
        if (lastEntry) {
          const lcp = Math.round(lastEntry.startTime)
          console.info(`[Performance] LCP: ${lcp}ms`)

          if (lcp > 4000) {
            captureMessage(`Slow LCP: ${lcp}ms`, 'warning')
          }
        }
      })
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] })
    } catch (e) {
      // LCP não suportado
    }

    // Long Tasks (main thread blocking)
    try {
      const longTaskObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          const duration = Math.round(entry.duration)
          console.warn(`[Performance] Long task: ${duration}ms`)

          if (duration > 100) {
            captureMessage(`Long task detected: ${duration}ms`, 'warning')
          }
        }
      })
      longTaskObserver.observe({ entryTypes: ['longtask'] })
    } catch (e) {
      // Long Tasks API não suportado
    }
  }

  // Time to Interactive (aproximado via DOMContentLoaded + load)
  window.addEventListener('load', () => {
    setTimeout(() => {
      const timing = performance.timing
      if (timing) {
        METRICS.tti = Math.round(timing.domInteractive - timing.navigationStart)
        console.info(`[Performance] TTI (approx): ${METRICS.tti}ms`)
      }
    }, 0)
  })

  // Monitor API calls
  monitorApiLatency()

  // Monitor lazy loading
  monitorLazyLoading()
}

/**
 * Monitora latência de chamadas API
 */
function monitorApiLatency() {
  const originalFetch = window.fetch

  window.fetch = async function (...args) {
    const start = performance.now()
    const url = typeof args[0] === 'string' ? args[0] : args[0].url

    try {
      const response = await originalFetch.apply(this, args)
      const duration = Math.round(performance.now() - start)

      // Log slow API calls
      if (duration > 1000) {
        console.warn(`[Performance] Slow API: ${url} took ${duration}ms`)
        captureMessage(`Slow API call: ${url} (${duration}ms)`, 'warning')
      }

      // Track metrics
      const endpoint = url.split('/api/')[1]?.split('?')[0] || 'unknown'
      METRICS.apiLatency[endpoint] = duration

      return response
    } catch (error) {
      const duration = Math.round(performance.now() - start)
      console.error(`[Performance] API error: ${url} failed after ${duration}ms`)
      captureError(error, { url, duration, context: 'api_call' })
      throw error
    }
  }
}

/**
 * Monitora carregamento lazy de views/componentes
 */
function monitorLazyLoading() {
  // Chunk loading errors
  window.addEventListener('error', (event) => {
    if (event.message?.includes('Loading chunk') || event.message?.includes('ChunkLoadError')) {
      console.error('[Performance] Chunk load error:', event.message)
      captureError(new Error(event.message), { context: 'chunk_load_error' })
    }
  })
}

/**
 * Mede tempo de renderização de charts
 */
export function measureChartRender(label = 'chart') {
  const start = performance.now()
  return () => {
    const duration = Math.round(performance.now() - start)
    METRICS.chartRenderTime = duration
    console.info(`[Performance] Chart render (${label}): ${duration}ms`)

    if (duration > 500) {
      captureMessage(`Slow chart render (${label}): ${duration}ms`, 'warning')
    }
  }
}

/**
 * Retorna métricas atuais (para debug/healthcheck)
 */
export function getMetrics() {
  return { ...METRICS }
}
