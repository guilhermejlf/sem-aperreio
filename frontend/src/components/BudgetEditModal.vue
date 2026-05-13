<template>
  <ModalBase
    :visible="visible"
    :title="titulo"
    highlight="Meta"
    :subtitle="subtitulo"
    size="small"
    @close="onCancel"
  >
    <!-- Step 1: Form -->
    <template v-if="etapa === 'form'">
      <div v-if="metaLocal.gasto_realizado > 0" class="modal-contexto">
        Você já despendeu <strong>{{ formatarValor(metaLocal.gasto_realizado) }}</strong>
        nesta categoria neste mês.
      </div>

      <div class="form-group">
        <label>Valor</label>
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

      <div v-if="metaLocal.modo === 'criar' || metaLocal.modo === 'criar_categoria'" class="form-group">
        <label>Período</label>
        <div class="period-selectors">
          <select v-model="mesSelecionado" class="input-field select-field period-select">
            <option v-for="(nome, idx) in mesesNomes" :key="idx" :value="idx + 1">{{ nome }}</option>
          </select>
          <select v-model="anoSelecionado" class="input-field select-field period-select">
            <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
          </select>
        </div>
      </div>

      <div v-if="metaLocal.modo === 'criar_categoria'" class="form-group">
        <label>Categoria</label>
        <select v-model="categoriaSelecionada" class="input-field select-field">
          <option value="" disabled>Selecione uma categoria</option>
          <option v-for="(label, value) in categoriasDisponiveis" :key="value" :value="value">
            {{ label }}
          </option>
        </select>
      </div>
    </template>

    <!-- Step 2: Confirmation -->
    <template v-else-if="etapa === 'confirmar'">
      <div class="confirmacao-texto">
        <p>
          Você já despendeu <strong>{{ formatarValor(metaLocal.gasto_realizado) }}</strong>
          em <strong>{{ metaLocal.categoria_nome || 'Geral' }}</strong> este mês.
        </p>
        <p>
          Alterar a meta de <strong>{{ formatarValor(metaLocal.valor_meta_original) }}</strong>
          para <strong>{{ formatarValor(valorNumerico) }}</strong>?
        </p>
      </div>
    </template>

    <template #footer>
      <template v-if="etapa === 'form'">
        <button class="btn-secondary" @click="onCancel">Cancelar</button>
        <button class="btn-primary" @click="onContinue" :disabled="!valido">
          Salvar Meta
        </button>
      </template>
      <template v-else-if="etapa === 'confirmar'">
        <button class="btn-secondary" @click="etapa = 'form'">Voltar</button>
        <button class="btn-primary" @click="onConfirmar">
          Confirmar
        </button>
      </template>
    </template>
  </ModalBase>
</template>

<script>
import ModalBase from './ModalBase.vue'
const CATEGORIA_OPTIONS = {
  moradia: 'Moradia',
  mercado: 'Mercado',
  restaurantes: 'Restaurantes / Delivery',
  transporte: 'Transporte',
  saude: 'Saúde',
  educacao: 'Educação',
  lazer: 'Lazer',
  contas: 'Contas e serviços',
  compras: 'Compras',
  outros: 'Outros'
}

const MES_NOMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

export default {
  name: 'BudgetEditModal',
  components: { ModalBase },
  props: {
    visible: { type: Boolean, default: false },
    meta: { type: Object, default: null },
    categoriasUsadas: { type: Array, default: () => [] }
  },
  emits: ['save', 'cancel'],
  data() {
    return {
      etapa: 'form',
      valorInput: '',
      erro: '',
      metaLocal: {},
      categoriaSelecionada: '',
      mesSelecionado: new Date().getMonth() + 1,
      anoSelecionado: new Date().getFullYear()
    }
  },
  computed: {
    titulo() {
      if (this.metaLocal.modo === 'criar') return 'Definir Meta Geral'
      if (this.metaLocal.modo === 'criar_categoria') return 'Adicionar Meta de Categoria'
      return 'Editar Meta'
    },
    subtitulo() {
      if (this.metaLocal.modo === 'criar') return 'Bora organizar esse mês e chegar lá!'
      if (this.metaLocal.modo === 'criar_categoria') return 'Defina um limite para essa categoria.'
      return `Ajustando meta de ${this.metaLocal.categoria_nome || 'Geral'}.`
    },
    valorNumerico() {
      const v = parseFloat(this.valorInput)
      return isNaN(v) ? 0 : v
    },
    valido() {
      return this.valorNumerico > 0 && (this.metaLocal.modo !== 'criar_categoria' || this.categoriaSelecionada)
    },
    categoriasDisponiveis() {
      const usadas = new Set(this.categoriasUsadas || [])
      return Object.fromEntries(
        Object.entries(CATEGORIA_OPTIONS).filter(([key]) => !usadas.has(key))
      )
    },
    mesesNomes() {
      return MES_NOMES
    },
    anosDisponiveis() {
      const atual = new Date().getFullYear()
      return [atual, atual - 1, atual - 2]
    }
  },
  watch: {
    visible: {
      immediate: true,
      handler(val) {
        if (val) {
          this.etapa = 'form'
          this.erro = ''
          this.metaLocal = { ...this.meta, valor_meta_original: this.meta?.valor_meta || 0 }
          this.valorInput = this.meta?.valor_meta ? String(this.meta.valor_meta) : ''
          this.categoriaSelecionada = this.meta?.categoria || ''
          this.mesSelecionado = this.meta?.mes || new Date().getMonth() + 1
          this.anoSelecionado = this.meta?.ano || new Date().getFullYear()
        }
      }
    },
    categoriaSelecionada(val) {
      this.metaLocal.categoria = val
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
      const payload = {
        ...this.metaLocal,
        valor_meta: this.valorNumerico
      }
      if (this.metaLocal.modo === 'criar' || this.metaLocal.modo === 'criar_categoria') {
        payload.mes = this.mesSelecionado
        payload.ano = this.anoSelecionado
      }
      this.$emit('save', payload)
    }
  }
}
</script>

<style scoped>
/* Contexto info box */
.modal-contexto {
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 24px;
  font-size: 14px;
  color: #93c5fd;
  line-height: 1.5;
}

/* Confirmation text */
.confirmacao-texto {
  line-height: 1.6;
  color: rgba(248, 250, 252, 0.82);
  font-size: 15px;
}

.confirmacao-texto p {
  margin: 8px 0;
}

.confirmacao-texto strong {
  color: #fbbf24;
}

/* Form groups */
.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: rgba(248, 250, 252, 0.72);
  margin-bottom: 10px;
}

/* Input wrapper */
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

/* Inputs */
.input-field {
  width: 100%;
  height: 56px;
  padding: 0 16px;
  padding-left: 44px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 16px;
  font-weight: 500;
  color: #F8FAFC;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-field::placeholder {
  color: rgba(248, 250, 252, 0.35);
}

.input-field:focus {
  outline: none;
  border-color: #60A637;
  box-shadow: 0 0 0 4px rgba(96, 166, 55, 0.12);
}

.select-field {
  padding-left: 16px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='rgba(248,250,252,0.45)' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
}

.period-selectors {
  display: flex;
  gap: 12px;
}

.period-select {
  flex: 1;
}

/* Error message */
.erro-msg {
  display: block;
  margin-top: 8px;
  font-size: 13px;
  color: #f87171;
}

/* Buttons */
.btn-secondary {
  height: 48px;
  padding: 0 24px;
  border-radius: 16px;
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
  border-radius: 16px;
  background: linear-gradient(180deg, #60A637 0%, #4C8932 100%);
  color: #FFFFFF;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 0 18px rgba(96, 166, 55, 0.12);
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(1.05);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(0.4);
}
</style>
