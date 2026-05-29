<template>
  <ModalBase
    :visible="visible"
    :title="editingId ? 'Editar Despesa' : 'Adicionar Despesa'"
    highlight="Despesa"
    size="medium"
    @close="onClose"
  >
    <form @submit.prevent="onSubmit" class="expense-form">
      <div class="form-group">
        <label class="form-label">Valor</label>
        <div class="input-wrapper">
          <span class="input-prefix">R$</span>
          <input
            v-model.number="form.valor"
            type="number"
            step="0.01"
            min="0.01"
            class="form-input input-field"
            placeholder="0,00"
            ref="inputValorRef"
          />
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Categoria</label>
        <select v-model="form.categoria" class="form-select">
          <option value="">Selecione uma categoria</option>
          <option v-for="cat in categorias" :key="cat.value" :value="cat.value">
            {{ cat.label }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Descrição</label>
        <input
          v-model="form.descricao"
          type="text"
          placeholder="Ex: Mercado, Uber, McDonald's..."
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label class="form-label">Data da despesa</label>
        <input
          type="date"
          v-model="form.data_competencia"
          class="form-input"
        />
      </div>

      <div class="form-group checkbox-group">
        <label class="form-checkbox">
          <input
            type="checkbox"
            v-model="form.pago"
          />
          <span>Já paguei essa despesa</span>
        </label>
      </div>

      <div class="form-group" v-if="form.pago">
        <label class="form-label">Data do pagamento</label>
        <input
          type="date"
          v-model="form.data_pagamento"
          class="form-input"
        />
      </div>

      <p v-if="error" class="form-error">{{ error }}</p>
    </form>

    <template #footer>
      <button class="btn-secondary" @click="onClose">Cancelar</button>
      <button
        class="btn-primary"
        :disabled="loading || !isValid"
        @click="onSubmit"
      >
        <span v-if="loading" class="btn-spinner"></span>
        <span v-else>{{ editingId ? 'Salvar alterações' : 'Salvar despesa' }}</span>
      </button>
    </template>
  </ModalBase>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import ModalBase from '../ModalBase.vue'
import { apiRequest, API_ENDPOINTS } from '../../config/api.js'
import { toastMessages, toastTitles } from '../../utils/toastMessages.js'
import { toastStore } from '../../stores/toast.store.js'

const CATEGORIAS = [
  { value: 'moradia', label: 'Moradia' },
  { value: 'mercado', label: 'Mercado' },
  { value: 'restaurantes', label: 'Restaurantes / Delivery' },
  { value: 'transporte', label: 'Transporte' },
  { value: 'saude', label: 'Saúde' },
  { value: 'educacao', label: 'Educação' },
  { value: 'lazer', label: 'Lazer' },
  { value: 'contas', label: 'Contas e serviços' },
  { value: 'compras', label: 'Compras' },
  { value: 'outros', label: 'Outros' }
]

const DEFAULT_FORM = {
  valor: null,
  categoria: '',
  descricao: '',
  data: new Date().toISOString().split('T')[0],
  data_competencia: '',
  data_pagamento: '',
  pago: false
}

const props = defineProps({
  visible: { type: Boolean, default: false },
  editingData: { type: Object, default: null }
})

const emit = defineEmits(['close', 'saved'])

const form = ref({ ...DEFAULT_FORM })
const loading = ref(false)
const error = ref(null)
const categorias = ref(CATEGORIAS)
const inputValorRef = ref(null)

const editingId = computed(() => props.editingData?.id || null)
const isValid = computed(() => form.value.valor && form.value.valor > 0 && form.value.categoria && form.value.data_competencia)

watch(() => props.visible, (val) => {
  if (val) {
    error.value = null
    if (props.editingData) {
      form.value = {
        valor: parseFloat(props.editingData.valor),
        categoria: props.editingData.categoria,
        descricao: props.editingData.descricao || '',
        data: new Date().toISOString().split('T')[0],
        data_competencia: props.editingData.data_competencia || '',
        data_pagamento: props.editingData.data_pagamento || '',
        pago: props.editingData.pago || false
      }
    } else {
      form.value = { ...DEFAULT_FORM }
    }
    nextTick(() => {
      inputValorRef.value?.focus()
    })
  }
})

function onClose() {
  emit('close')
}

async function onSubmit() {
  if (!isValid.value) return
  loading.value = true
  error.value = null

  try {
    const payload = { ...form.value, data: form.value.data_competencia || form.value.data }

    if (editingId.value) {
      const response = await apiRequest(API_ENDPOINTS.GASTO_DETAIL(editingId.value), {
        method: 'PUT',
        body: JSON.stringify(payload)
      })
      toastStore.success(toastMessages.expense.updated, { title: toastTitles.success })
      if (response?.alerta_meta) {
        const variant = response.alerta_meta.status === 'critical' ? 'error' : 'warning'
        toastStore[variant](response.alerta_meta.mensagem, { title: 'Meta de Despesas' })
      }
    } else {
      const response = await apiRequest(API_ENDPOINTS.GASTOS_LIST, {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      toastStore.success(toastMessages.expense.created, { title: toastTitles.success })
      if (response?.alerta_meta) {
        const variant = response.alerta_meta.status === 'critical' ? 'error' : 'warning'
        toastStore[variant](response.alerta_meta.mensagem, { title: 'Meta de Despesas' })
      }
    }

    emit('saved')
    onClose()
  } catch (err) {
    error.value = err.message || toastMessages.expense.saveError
    toastStore.error(toastMessages.expense.saveError, { title: toastTitles.error })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.expense-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form-label {
  font-size: 13px;
  font-weight: var(--weight-semibold);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: var(--space-4);
  color: var(--text-muted);
  font-weight: var(--weight-medium);
  font-size: 15px;
  pointer-events: none;
  z-index: 1;
}

.form-input,
.form-select {
  width: 100%;
  height: 48px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-sm);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 15px;
  font-weight: var(--weight-medium);
  color: var(--text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-glow);
}

.input-field {
  padding-left: 44px;
}

.form-input::placeholder {
  color: var(--text-muted);
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='rgba(248,250,252,0.45)' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.form-checkbox input {
  width: 18px;
  height: 18px;
  accent-color: var(--color-primary);
}

.form-error {
  color: var(--color-error);
  font-size: 13px;
  margin: 0;
}

.btn-secondary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.06);
}

.btn-primary {
  height: 48px;
  padding: 0 var(--space-6);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-glow);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-width: 160px;
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.05);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.4);
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
