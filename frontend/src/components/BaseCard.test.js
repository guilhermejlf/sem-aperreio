import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseCard from './BaseCard.vue'

describe('BaseCard', () => {
  it('renderiza título e valor', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Mercado', value: 'R$ 150,00' }
    })
    expect(wrapper.text()).toContain('Mercado')
    expect(wrapper.text()).toContain('R$ 150,00')
  })

  it('renderiza ícone quando fornecido', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', icon: '🛒', value: 'R$ 0' }
    })
    expect(wrapper.find('.base-card__icon').text()).toBe('🛒')
  })

  it('aplica classe de grupo quando isGroup é true', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', value: 'R$ 0', isGroup: true }
    })
    expect(wrapper.find('.base-card--group').exists()).toBe(true)
  })

  it('aplica cor customizada ao valor', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', value: 'R$ 0', valueColor: '#ff0000' }
    })
    const valueEl = wrapper.find('.base-card__value')
    expect(valueEl.attributes('style')).toContain('color: rgb(255, 0, 0)')
  })

  it('renderiza slot de badges', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', value: 'R$ 0' },
      slots: {
        badges: '<span class="badge">Pago</span>'
      }
    })
    expect(wrapper.find('.badge').exists()).toBe(true)
    expect(wrapper.text()).toContain('Pago')
  })

  it('renderiza slot de actions', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', value: 'R$ 0' },
      slots: {
        actions: '<button>Editar</button>'
      }
    })
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('renderiza slot de extras', () => {
    const wrapper = mount(BaseCard, {
      props: { title: 'Teste', value: 'R$ 0' },
      slots: {
        extras: '<small>Detalhe</small>'
      }
    })
    expect(wrapper.text()).toContain('Detalhe')
  })
})
