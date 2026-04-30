<template>
  <div v-if="visible" class="modal-overlay" @click.self="onCancel">
    <div class="modal-card">
      <!-- Step 1: Form -->
      <template v-if="etapa === 'form'">
        <div class="modal-header">
          <span class="modal-icon">✏️</span>
          <h3>{{ titulo }}</h3>
        </div>

        <div v-if="metaLocal.gasto_realizado > 0" class="modal-contexto">
          Você já gastou <strong>{{ formatarValor(metaLocal.gasto_realizado) }}</strong>
          nesta categoria neste mês.
        </div>

        <div class="form-group">
          <label>Valor da Meta (R$)</label>
          <div class="input-wrapper">
            <span class="input-prefix">R$</span>
            <input
              v-model="valorInput"
              type="number"
              step="0.01"
              min="0.01"
              class="input-field"
              placeholder="0,00"
              @keyup.enter="onContinue"
            />
          </div>
          <span v-if="erro" class="erro-msg">{{ erro }}</span>
        </div>

        <div v-if="metaLocal.modo === 'criar_categoria'" class="form-group">
          <label>Categoria</label>
          <select v-model="metaLocal.categoria" class="input-field select-field">
            <option value="" disabled>Selecione uma categoria</option>
            <option value="alimentacao">Alimentação</option>
            <option value="transporte">Transporte</option>
            <option value="moradia">Moradia</option>
            <option value="saude">Saúde</option>
            <option value="educacao">Educação</option>
            <option value="lazer">Lazer</option>
            <option value="vestuario">Vestuário</option>
            <option value="servicos">Serviços</option>
            <option value="outros">Outros</option>
          </select>
        </div>

        <div class="modal-actions">
          <button class="btn-secondary" @click="onCancel">Cancelar</button>
          <button class="btn-primary" @click="onContinue" :disabled="!valido">
            Salvar Meta
          </button>
        </div>
      </template>

      <!-- Step 2: Confirmation -->
      <template v-else-if="etapa === 'confirmar'">
        <div class="modal-header confirmacao">
          <span class="modal-icon">⚠️</span>
          <h3>Confirme a alteração</h3>
        </div>

        <div class="confirmacao-texto">
          <p>
            Você já gastou <strong>{{ formatarValor(metaLocal.gasto_realizado) }}</strong>
            em <strong>{{ metaLocal.categoria_nome || 'Geral' }}</strong> este mês.
          </p>
          <p>
            Alterar a meta de <strong>{{ formatarValor(metaLocal.valor_meta_original) }}</strong>
            para <strong>{{ formatarValor(valorNumerico) }}</strong>?
          </p>
        </div>

        <div class="modal-actions">
          <button class="btn-secondary" @click="etapa = 'form'">Voltar</button>
          <button class="btn-primary" @click="onConfirmar">
            Confirmar
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BudgetEditModal',
  props: {
    visible: { type: Boolean, default: false },
    meta: { type: Object, default: null }
  },
  emits: ['save', 'cancel'],
  data() {
    return {
      etapa: 'form',
      valorInput: '',
      erro: '',
      metaLocal: {}
    }
  },
  computed: {
    titulo() {
      if (this.metaLocal.modo === 'criar') return 'Definir Meta Geral'
      if (this.metaLocal.modo === 'criar_categoria') return 'Adicionar Meta de Categoria'
      return `Editar Meta — ${this.metaLocal.categoria_nome || 'Geral'}`
    },
    valorNumerico() {
      const v = parseFloat(this.valorInput)
      return isNaN(v) ? 0 : v
    },
    valido() {
      return this.valorNumerico > 0 && (this.metaLocal.modo !== 'criar_categoria' || this.metaLocal.categoria)
    }
  },
  watch: {
    visible(val) {
      if (val) {
        this.etapa = 'form'
        this.erro = ''
        this.metaLocal = { ...this.meta, valor_meta_original: this.meta?.valor_meta || 0 }
        this.valorInput = this.meta?.valor_meta ? String(this.meta.valor_meta) : ''
      }
    }
  },
  methods: {
    formatarValor(valor) {
      return parseFloat(valor || 0).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    onCancel() {
      this.$emit('cancel')
    },

    onContinue() {
      if (!this.valido) {
        this.erro = 'Informe um valor maior que zero'
        return
      }

      // Se editando meta existente e já há gastos, mostrar confirmação
      if (this.metaLocal.id && this.metaLocal.gasto_realizado > 0 && this.valorNumerico !== parseFloat(this.metaLocal.valor_meta_original)) {
        this.etapa = 'confirmar'
        return
      }

      this.onConfirmar()
    },

    onConfirmar() {
      this.$emit('save', {
        ...this.metaLocal,
        valor_meta: this.valorNumerico
      })
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-card {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 28px;
  width: min(480px, 90vw);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5);
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.modal-header.confirmacao h3 {
  color: #fbbf24;
}

.modal-icon {
  font-size: 1.5rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #e5e7eb;
}

.modal-contexto {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3b82f6;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: #93c5fd;
  line-height: 1.5;
}

.confirmacao-texto {
  margin-bottom: 24px;
  line-height: 1.6;
  color: #e5e7eb;
}

.confirmacao-texto p {
  margin: 8px 0;
}

.confirmacao-texto strong {
  color: #fbbf24;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 14px;
  color: #64748b;
  font-weight: 500;
  font-size: 1.1rem;
}

.input-field {
  width: 100%;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  padding: 12px 14px 12px 44px;
  color: #e5e7eb;
  font-size: 1.1rem;
  text-align: center;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.select-field {
  padding-left: 14px;
  text-align: left;
}

.input-field:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.15);
}

.erro-msg {
  display: block;
  margin-top: 6px;
  font-size: 0.85rem;
  color: #f87171;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.btn-secondary {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #94a3b8;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}

.btn-secondary:hover {
  color: #e5e7eb;
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.05);
}

.btn-primary {
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 24px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #16a34a;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #374151;
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
