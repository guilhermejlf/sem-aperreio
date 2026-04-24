// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const API_ENDPOINTS = {
  // Gastos
  GASTOS_LIST: `${API_BASE_URL}/api/gastos/`,
  GASTO_DETAIL: (id) => `${API_BASE_URL}/api/gastos/${id}/`,
  
  // Previsão
  PREVER_GASTO: `${API_BASE_URL}/api/prever/`,
}

// Headers padrão
export const API_HEADERS = {
  'Content-Type': 'application/json',
}

// Função helper para requests
export async function apiRequest(url, options = {}) {
  const config = {
    headers: { ...API_HEADERS, ...options.headers },
    ...options,
  }

  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.erro || `HTTP ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}
