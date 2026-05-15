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
          this.$toast.success('Receita atualizada!')
        } else {
          await addReceita({
            valor: this.form.valor,
            descricao: this.form.descricao,
            data: this.form.data
          })
          this.$toast.success('Receita adicionada!')
        }

        this.$emit('saved')
        this.onClose()
      } catch (err) {
        this.error = err.message || 'Erro ao salvar receita'
        this.$toast.error(this.error)
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
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: rgba(248, 250, 252, 0.72);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 16px;
  color: rgba(248, 250, 252, 0.45);
  font-weight: 500;
  font-size: 15px;
  pointer-events: none;
  z-index: 1;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 15px;
  font-weight: 500;
  color: #F8FAFC;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #60A637;
  box-shadow: 0 0 0 3px rgba(96, 166, 55, 0.12);
}

.input-field {
  padding-left: 44px;
}

.form-input::placeholder {
  color: rgba(248, 250, 252, 0.35);
}

.form-error {
  color: #f87171;
  font-size: 13px;
  margin: 0;
}

.btn-secondary {
  height: 48px;
  padding: 0 24px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(248, 250, 252, 0.82);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.06);
}

.btn-primary {
  height: 48px;
  padding: 0 24px;
  border-radius: 14px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 18px rgba(96, 166, 55, 0.12);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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
