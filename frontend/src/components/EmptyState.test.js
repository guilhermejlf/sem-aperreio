import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import EmptyState from './EmptyState.vue'

describe('EmptyState', () => {
  it('renderiza título e ícone', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Nada aqui', icon: 'pi pi-inbox' }
    })
    expect(wrapper.text()).toContain('Nada aqui')
    expect(wrapper.find('.empty-state-icon').exists()).toBe(true)
  })

  it('renderiza descrição quando fornecida', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', description: 'Adicione algo', icon: 'pi pi-inbox' }
    })
    expect(wrapper.text()).toContain('Adicione algo')
  })

  it('não renderiza descrição quando omitida', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', icon: 'pi pi-inbox' }
    })
    expect(wrapper.find('.empty-state-description').exists()).toBe(false)
  })

  it('renderiza botão de ação quando actionLabel fornecido', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', actionLabel: 'Adicionar', icon: 'pi pi-inbox' }
    })
    expect(wrapper.find('.empty-state-action').exists()).toBe(true)
    expect(wrapper.text()).toContain('Adicionar')
  })

  it('emite evento action ao clicar no botão', async () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', actionLabel: 'Ir', icon: 'pi pi-inbox' }
    })
    await wrapper.find('.empty-state-action').trigger('click')
    expect(wrapper.emitted('action')).toBeTruthy()
    expect(wrapper.emitted('action').length).toBe(1)
  })

  it('renderiza Seu Bené quando showBene é true', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', showBene: true, beneText: 'Oi!', icon: 'pi pi-inbox' }
    })
    expect(wrapper.find('.empty-state-bene').exists()).toBe(true)
    expect(wrapper.text()).toContain('Oi!')
  })

  it('não renderiza Seu Bené por padrão', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', icon: 'pi pi-inbox' }
    })
    expect(wrapper.find('.empty-state-bene').exists()).toBe(false)
  })

  it('aplica classe de variante quando fornecida', () => {
    const wrapper = mount(EmptyState, {
      props: { title: 'Vazio', variant: 'no-results', icon: 'pi pi-inbox' }
    })
    expect(wrapper.find('.empty-state--no-results').exists()).toBe(true)
  })
})
