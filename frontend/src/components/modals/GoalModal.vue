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
          <span v-if="loading" class="btn-spinner"></span>
          <span v-else>Salvar Meta</span>
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

<script setup>
import { ref, computed, watch } from 'vue'
import ModalBase from '../ModalBase.vue'
import { formatarValor } from '../../utils/formatCurrency.js'

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

const props = defineProps({
  visible: { type: Boolean, default: false },
  meta: { type: Object, default: null },
  categoriasUsadas: { type: Array, default: () => [] }
})

const emit = defineEmits(['save', 'cancel'])

const etapa = ref('form')
const valorInput = ref('')
const erro = ref('')
const metaLocal = ref({})
const categoriaSelecionada = ref('')
const mesSelecionado = ref(new Date().getMonth() + 1)
const anoSelecionado = ref(new Date().getFullYear())
const loading = ref(false)

const titulo = computed(() => {
  if (metaLocal.value.modo === 'criar') return 'Definir Meta Geral'
  if (metaLocal.value.modo === 'criar_categoria') return 'Adicionar Meta de Categoria'
  return 'Editar Meta'
})
const subtitulo = computed(() => {
  if (metaLocal.value.modo === 'criar') return 'Bora organizar esse mês e chegar lá!'
  if (metaLocal.value.modo === 'criar_categoria') return 'Defina um limite para essa categoria.'
  return `Ajustando meta de ${metaLocal.value.categoria_nome || 'Geral'}.`
})
const valorNumerico = computed(() => {
  const v = parseFloat(valorInput.value)
  return isNaN(v) ? 0 : v
})
const valido = computed(() =>
  valorNumerico.value > 0 && (metaLocal.value.modo !== 'criar_categoria' || categoriaSelecionada.value)
)
const categoriasDisponiveis = computed(() => {
  const usadas = new Set(props.categoriasUsadas || [])
  return Object.fromEntries(
    Object.entries(CATEGORIA_OPTIONS).filter(([key]) => !usadas.has(key))
  )
})
const mesesNomes = computed(() => MES_NOMES)
const anosDisponiveis = computed(() => {
  const atual = new Date().getFullYear()
  return [atual, atual - 1, atual - 2]
})

watch(() => props.visible, (val) => {
  if (val) {
    etapa.value = 'form'
    erro.value = ''
    metaLocal.value = { ...props.meta, valor_meta_original: props.meta?.valor_meta || 0 }
    valorInput.value = props.meta?.valor_meta ? String(props.meta.valor_meta) : ''
    categoriaSelecionada.value = props.meta?.categoria || ''
    mesSelecionado.value = props.meta?.mes || new Date().getMonth() + 1
    anoSelecionado.value = props.meta?.ano || new Date().getFullYear()
  }
}, { immediate: true })

watch(categoriaSelecionada, (val) => {
  metaLocal.value.categoria = val
})

function onCancel() {
  emit('cancel')
}

function onContinue() {
  if (!valido.value) {
    erro.value = 'Informe um valor maior que zero'
    return
  }

  if (metaLocal.value.id && metaLocal.value.gasto_realizado > 0 && valorNumerico.value !== parseFloat(metaLocal.value.valor_meta_original)) {
    etapa.value = 'confirmar'
    return
  }

  onConfirmar()
}

function onConfirmar() {
  const payload = {
    ...metaLocal.value,
    valor_meta: valorNumerico.value
  }
  if (metaLocal.value.modo === 'criar' || metaLocal.value.modo === 'criar_categoria') {
    payload.mes = mesSelecionado.value
    payload.ano = anoSelecionado.value
  }
  emit('save', payload)
}
</script>

<style scoped>
/* Contexto info box */
.modal-contexto {
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-4);
  margin-bottom: var(--space-6);
  font-size: var(--font-sm);
  color: var(--color-info);
  line-height: 1.5;
}

/* Confirmation text */
.confirmacao-texto {
  line-height: 1.6;
  color: var(--text-secondary);
  font-size: 15px;
}

.confirmacao-texto p {
  margin: var(--space-2) 0;
}

.confirmacao-texto strong {
  color: var(--color-warning);
}

/* Form groups */
.form-group {
  margin-bottom: var(--space-6);
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: var(--weight-semibold);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: var(--space-3);
}

/* Input wrapper */
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

/* Inputs */
.input-field {
  width: 100%;
  height: 56px;
  padding: 0 var(--space-4);
  padding-left: 44px;
  border-radius: var(--radius-md);
  background: var(--bg-hover);
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: var(--font-md);
  font-weight: var(--weight-medium);
  color: var(--text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.input-field::placeholder {
  color: var(--text-muted);
}

.input-field:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px var(--color-primary-glow);
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
  gap: var(--space-3);
}

.period-select {
  flex: 1;
}

/* Error message */
.erro-msg {
  display: block;
  margin-top: var(--space-2);
  font-size: 13px;
  color: var(--color-error);
}

/* Buttons */
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
  min-width: 140px;
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
