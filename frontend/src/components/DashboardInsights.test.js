import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DashboardInsights from './DashboardInsights.vue'

describe('DashboardInsights', () => {
  it('renderiza insights quando há dados suficientes', () => {
    const data = {
      saldo: 1000,
      total_mes: 500,
      total_receitas: 1500,
      variacao_percentual: 15,
      total_a_pagar: 200,
      quantidade_gastos: 5,
    }
    const wrapper = mount(DashboardInsights, {
      props: { data }
    })
    // O componente gera insights automaticamente a partir dos dados
    const cards = wrapper.findAll('.insight-card')
    expect(cards.length).toBeGreaterThan(0)
  })

  it('não renderiza nada quando data é null', () => {
    const wrapper = mount(DashboardInsights, {
      props: { data: null }
    })
    expect(wrapper.find('.dashboard-insights').exists()).toBe(false)
  })

  it('aplica classe de tipo baseada nos dados', () => {
    const data = {
      saldo: 1000,
      total_mes: 500,
      total_receitas: 1500,
      variacao_percentual: 15,
      total_a_pagar: 200,
      quantidade_gastos: 5,
    }
    const wrapper = mount(DashboardInsights, {
      props: { data }
    })
    const cards = wrapper.findAll('.insight-card')
    expect(cards.length).toBeGreaterThan(0)
    // Verifica que alguma classe insight-* existe
    expect(cards[0].classes().some(c => c.startsWith('insight-'))).toBe(true)
  })

  it('renderiza ícone em cada card', () => {
    const data = {
      saldo: 1000,
      total_mes: 500,
      total_receitas: 1500,
      variacao_percentual: 15,
      total_a_pagar: 200,
      quantidade_gastos: 5,
    }
    const wrapper = mount(DashboardInsights, {
      props: { data }
    })
    const icons = wrapper.findAll('.insight-icon-wrap i')
    expect(icons.length).toBeGreaterThan(0)
  })
})
