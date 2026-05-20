import { test, expect } from '@playwright/test'

const API_BASE = 'http://127.0.0.1:8000'
const TEST_USER = {
  username: 'teste_e2e_' + Date.now(),
  email: `teste_e2e_${Date.now()}@example.com`,
  password: 'SenhaSegura123!',
  first_name: 'Teste',
  last_name: 'E2E'
}

test.describe('Fluxo critico: Auth + Dashboard + Gasto', () => {
  test.beforeAll(async ({ request }) => {
    // Verifica se backend está rodando
    try {
      const health = await request.get(`${API_BASE}/api/health/`, { timeout: 5000 })
      console.log('Backend health:', health.status())
    } catch (e) {
      console.error('Backend não está rodando em', API_BASE)
      console.error('Inicie o Django: python manage.py runserver')
      throw new Error('Backend não disponível')
    }

    // Cria usuario direto via API
    const resp = await request.post(`${API_BASE}/api/auth/register/`, {
      data: {
        username: TEST_USER.username,
        email: TEST_USER.email,
        first_name: TEST_USER.first_name,
        last_name: TEST_USER.last_name,
        password: TEST_USER.password,
        password2: TEST_USER.password
      },
      failOnStatusCode: false
    })
    console.log('Register status:', resp.status())
    const body = await resp.text()
    console.log('Register body:', body.substring(0, 200))
    // 201 = criado, 400 = ja existe — ambos sao ok
    if (![201, 400].includes(resp.status())) {
      console.warn('Register API status:', resp.status(), body)
    }
  })

  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('login via API, adicionar gasto e ver no dashboard', async ({ page, request }) => {
    // === LOGIN VIA API ===
    const loginResp = await request.post(`${API_BASE}/api/auth/login/`, {
      data: { identifier: TEST_USER.email, password: TEST_USER.password }
    })
    expect(loginResp.ok()).toBeTruthy()
    const tokens = await loginResp.json()

    // Navega para app com tokens pré-setados
    await page.goto('/')
    await page.evaluate((t) => {
      localStorage.setItem('access_token', t.access)
      localStorage.setItem('refresh_token', t.refresh)
    }, tokens)
    await page.reload()

    // === VERIFICA DASHBOARD ===
    await page.waitForSelector('text=Painel', { timeout: 10000 })
    await expect(page.locator('text=Painel')).toBeVisible()

    // === ADICIONAR GASTO ===
    await page.click('text=Despesas')
    await page.click('button:has-text("Nova Despesa")')

    await page.fill('input[placeholder="0,00"]', '150.00')
    await page.selectOption('select', 'transporte')
    await page.fill('input[placeholder="Ex: Mercado, Uber, McDonald\'s..."]', 'Uber para trabalho')
    await page.click('button:has-text("Salvar despesa")')

    // Aguarda toast de sucesso
    await page.waitForSelector('.p-toast-message-success', { timeout: 5000 })

    // === VERIFICA NO DASHBOARD ===
    await page.click('text=Painel')
    await expect(page.locator('text=Transporte')).toBeVisible()
  })
})
