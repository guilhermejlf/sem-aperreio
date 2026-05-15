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
            ref="inputValor"
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

<script>
import ModalBase from '../ModalBase.vue'
import { addReceita, updateReceita } from '../../config/api.js'
import { toastMessages, toastTitles } from '../../utils/toastMessages.js'

const DEFAULT_FORM = {
  valor: null,
  descricao: '',
  data: new Date().toISOString().split('T')[0]
}

export default {
  name: 'RevenueModal',
  components: { ModalBase },
  props: {
    visible: { type: Boolean, default: false },
    editingData: { type: Object, default: null }
  },
  emits: ['close', 'saved'],
  data() {
    return {
      form: { ...DEFAULT_FORM },
      loading: false,
      error: null
    }
  },
  computed: {
    editingId() {
      return this.editingData?.id || null
    },
    isValid() {
      return this.form.valor && this.form.valor > 0 && this.form.data
    }
  },
  watch: {
    visible(val) {
      if (val) {
        this.error = null
        if (this.editingData) {
          this.form = {
            valor: parseFloat(this.editingData.valor),
            descricao: this.editingData.descricao || '',
            data: this.editingData.data
          }
        } else {
          this.form = { ...DEFAULT_FORM }
        }
        this.$nextTick(() => {
          this.$refs.inputValor?.focus()
        })
      }
    }
  },
  methods: {
    onClose() {
      this.$emit('close')
    },
    async onSubmit() {
      if (!this.isValid) return
      this.loading = true
      this.error = null

      try {
        if (this.editingId) {
          await updateReceita(this.editingId, {
            valor: this.form.valor,
            descricao: this.form.descricao,
            data: this.form.data
          })
          this.$toast.success(toastMessages.revenue.updated, { title: toastTitles.success })
        } else {
          await addReceita({
            valor: this.form.valor,
            descricao: this.form.descricao,
            data: this.form.data
          })
          this.$toast.success(toastMessages.revenue.created, { title: toastTitles.success })
        }

        this.$emit('saved')
        this.onClose()
      } catch (err) {
        this.error = err.message || toastMessages.revenue.saveError
        this.$toast.error(toastMessages.revenue.saveError, { title: toastTitles.error })
      } finally {
        this.loading = false
      }
    }
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
