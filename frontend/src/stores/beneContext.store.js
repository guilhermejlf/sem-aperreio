import { reactive } from 'vue'

const INSIGHT_COOLDOWN = 60000
const INSIGHT_DISPLAY_MS = 6000

const INSIGHT_MESSAGES = {
  info: [
    'Tá tudo certo 😄',
    'Quer registrar um gasto?',
    'Posso ajudar com alguma coisa?',
    'Dia produtivo por aí?',
  ],
  success: [
    'Falta pouco pra tua meta 🎯',
    'Bom trabalho nas finanças!',
    'Tá no caminho certo 👍',
  ],
  warning: [
    'Mercado aumentou esse mês 👀',
    'Dá uma olhada nos gastos fixos',
    'Lembrou de registrar tudo?',
  ],
  neutral: [
    'Seu Bené por aqui 👋',
    'Qualquer coisa é só chamar',
    'To de olho nas contas 😉',
  ],
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

function generateInsight(variant) {
  const messages = INSIGHT_MESSAGES[variant] || INSIGHT_MESSAGES.neutral
  return {
    id: Date.now() + Math.random(),
    message: pickRandom(messages),
    variant: variant || 'neutral',
    timestamp: Date.now(),
  }
}

export const beneStore = reactive({
  currentInsight: null,
  queue: [],
  dismissed: [],
  visible: false,
  lastShown: 0,
  hideTimer: null,
  showTimer: null,

  showInsight(variant = 'neutral', delay = 0) {
    const now = Date.now()
    if (now - this.lastShown < INSIGHT_COOLDOWN && this.currentInsight) {
      return
    }

    clearTimeout(this.showTimer)
    this.showTimer = setTimeout(() => {
      const insight = generateInsight(variant)
      this.currentInsight = insight
      this.lastShown = Date.now()

      clearTimeout(this.hideTimer)
      this.hideTimer = setTimeout(() => {
        this.dismiss()
      }, INSIGHT_DISPLAY_MS)
    }, delay)
  },

  dismiss() {
    if (this.currentInsight) {
      this.dismissed.push(this.currentInsight.id)
      this.currentInsight = null
    }
    clearTimeout(this.hideTimer)
    clearTimeout(this.showTimer)
  },

  openChat() {
    this.dismiss()
    this.visible = true
  },

  closeChat() {
    this.visible = false
  },

  toggleChat() {
    this.visible = !this.visible
  },
})

export default beneStore
