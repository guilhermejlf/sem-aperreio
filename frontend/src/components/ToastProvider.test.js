import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { reactive } from 'vue'

vi.mock('../stores/toast.store.js', () => {
  const items = reactive([])
  return {
    toastStore: {
      items,
      remove: vi.fn((id) => {
        const idx = items.findIndex(i => i.id === id)
        if (idx !== -1) items.splice(idx, 1)
      }),
      pauseAll: vi.fn(),
      resumeAll: vi.fn(),
    }
  }
})

import { toastStore } from '../stores/toast.store.js'
import ToastProvider from './ToastProvider.vue'

describe('ToastProvider', () => {
  beforeEach(() => {
    toastStore.items.length = 0
    toastStore.remove.mockClear()
    toastStore.pauseAll.mockClear()
    toastStore.resumeAll.mockClear()
  })

  it('renderiza lista vazia quando não há toasts', () => {
    const wrapper = mount(ToastProvider)
    expect(wrapper.findAll('.toast-item').length).toBe(0)
  })

  it('renderiza toast quando há items na store', async () => {
    toastStore.items.push({ id: 1, title: 'Sucesso', message: 'Salvo!', variant: 'success', dismissible: true })
    await flushPromises()
    const wrapper = mount(ToastProvider)
    expect(wrapper.findAll('.toast-item').length).toBe(1)
    expect(wrapper.text()).toContain('Sucesso')
    expect(wrapper.text()).toContain('Salvo!')
  })

  it('chama remove ao clicar no toast', async () => {
    toastStore.items.push({ id: 1, message: 'Teste', variant: 'info', dismissible: true })
    await flushPromises()
    const wrapper = mount(ToastProvider)
    await wrapper.find('.toast-item').trigger('click')
    expect(toastStore.remove).toHaveBeenCalledWith(1)
  })

  it('renderiza ícone correto por variante', async () => {
    const variants = [
      { variant: 'success', icon: '✓' },
      { variant: 'error', icon: '✕' },
      { variant: 'warning', icon: '⚠' },
      { variant: 'info', icon: 'ℹ' },
    ]
    for (const v of variants) {
      toastStore.items.length = 0
      toastStore.items.push({ id: 1, message: 'Test', variant: v.variant, dismissible: false })
      await flushPromises()
      const wrapper = mount(ToastProvider)
      expect(wrapper.find('.toast-icon').text()).toBe(v.icon)
    }
  })

  it('não renderiza botão de fechar quando dismissible é false', async () => {
    toastStore.items.push({ id: 1, message: 'Teste', variant: 'info', dismissible: false })
    await flushPromises()
    const wrapper = mount(ToastProvider)
    expect(wrapper.find('.toast-close').exists()).toBe(false)
  })
})
