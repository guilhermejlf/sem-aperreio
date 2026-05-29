<template>
  <ModalBase
    :visible="visible"
    :title="editingId ? 'Editar Receita' : 'Adicionar Receita'"
    highlight="Receita"
    size="small"
    @close="onClose"
  >
    <form @submit.prevent="onSubmit" class="revenue-form">
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
        <label class="form-label">Descrição</label>
        <input
          v-model="form.descricao"
          type="text"
          placeholder="Ex: Salário, Freelance..."
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label class="form-label">Data</label>
        <input
          type="date"
          v-model="form.data"
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
        <span v-else>{{ editingId ? 'Salvar alterações' : 'Salvar Receita' }}</span>
      </button>
    </template>
  </ModalBase>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import ModalBase from '../ModalBase.vue'
import { addReceita, updateReceita } from '../../config/api.js'
import { toastMessages, toastTitles } from '../../utils/toastMessages.js'
import { toastStore } from '../../stores/toast.store.js'

const DEFAULT_FORM = {
  valor: null,
  descricao: '',
  data: new Date().toISOString().split('T')[0]
}

const props = defineProps({
  visible: { type: Boolean, default: false },
  editingData: { type: Object, default: null }
})

const emit = defineEmits(['close', 'saved'])

const form = ref({ ...DEFAULT_FORM })
const loading = ref(false)
const error = ref(null)
const inputValorRef = ref(null)

const editingId = computed(() => props.editingData?.id || null)
const isValid = computed(() => form.value.valor && form.value.valor > 0 && form.value.data)

watch(() => props.visible, (val) => {
  if (val) {
    error.value = null
    if (props.editingData) {
      form.value = {
        valor: parseFloat(props.editingData.valor),
        descricao: props.editingData.descricao || '',
        data: props.editingData.data
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
    if (editingId.value) {
      await updateReceita(editingId.value, {
        valor: form.value.valor,
        descricao: form.value.descricao,
        data: form.value.data
      })
      toastStore.success(toastMessages.revenue.updated, { title: toastTitles.success })
    } else {
      await addReceita({
        valor: form.value.valor,
        descricao: form.value.descricao,
        data: form.value.data
      })
      toastStore.success(toastMessages.revenue.created, { title: toastTitles.success })
    }

    emit('saved')
    onClose()
  } catch (err) {
    error.value = err.message || toastMessages.revenue.saveError
    toastStore.error(toastMessages.revenue.saveError, { title: toastTitles.error })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.revenue-form {
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

.form-input {
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

.form-input:focus {
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
