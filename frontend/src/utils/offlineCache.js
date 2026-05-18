const DB_NAME = 'sem_aperreio_cache'
const DB_VERSION = 1
const STORE_NAME = 'api_cache'

let dbPromise = null

function openDB() {
  if (dbPromise) return dbPromise
  dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)
    request.onerror = () => reject(request.error)
    request.onsuccess = () => resolve(request.result)
    request.onupgradeneeded = (event) => {
      const db = event.target.result
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'key' })
      }
    }
  })
  return dbPromise
}

export async function cacheGet(key) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readonly')
      const store = tx.objectStore(STORE_NAME)
      const request = store.get(key)
      request.onsuccess = () => {
        const record = request.result
        if (!record) return resolve(null)
        // Expire após 24h
        if (Date.now() - record.timestamp > 24 * 60 * 60 * 1000) {
          cacheDelete(key)
          return resolve(null)
        }
        resolve(record.data)
      }
      request.onerror = () => reject(request.error)
    })
  } catch (e) {
    console.warn('Cache get error:', e)
    return null
  }
}

export async function cacheSet(key, data) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite')
      const store = tx.objectStore(STORE_NAME)
      const request = store.put({ key, data, timestamp: Date.now() })
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  } catch (e) {
    console.warn('Cache set error:', e)
  }
}

export async function cacheDelete(key) {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite')
      const store = tx.objectStore(STORE_NAME)
      const request = store.delete(key)
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  } catch (e) {
    console.warn('Cache delete error:', e)
  }
}

export async function cacheClear() {
  try {
    const db = await openDB()
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite')
      const store = tx.objectStore(STORE_NAME)
      const request = store.clear()
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  } catch (e) {
    console.warn('Cache clear error:', e)
  }
}

function getCacheKey(url) {
  try {
    const u = new URL(url)
    return u.pathname + u.search
  } catch {
    return url
  }
}

const CACHEABLE_ENDPOINTS = [
  '/api/dashboard/',
  '/api/gastos/',
  '/api/receitas/',
  '/api/metas/',
  '/api/extrato/',
  '/api/family/',
]

export function isCacheable(url) {
  return CACHEABLE_ENDPOINTS.some(path => url.includes(path))
}

export { getCacheKey }
