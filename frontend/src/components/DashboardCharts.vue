<template>
  <div class="dashboard">
    <!-- Seletor de Período -->
    <div class="period-selector">
      <select v-model="periodo.mes" class="period-select">
        <option v-for="(nome, idx) in mesesNomes" :key="idx" :value="idx + 1">{{ nome }}</option>
      </select>
      <select v-model="periodo.ano" class="period-select">
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="dashboard-loading">
      <i class="pi pi-spin pi-spinner"></i>
      <p>Carregando...</p>
    </div>

    <EmptyState
      v-else-if="dashboardData && dashboardData.quantidade_gastos === 0 && (dashboardData.total_receitas || 0) === 0"
      title="Nenhum movimento neste período"
      :description="dashboardData.periodo ? `Adicione uma receita ou despesa pra ver o painel de ${dashboardData.periodo.mes_nome} ${dashboardData.periodo.ano}.` : 'Teu painel ganhará vida depois dos primeiros lançamentos.'"
      icon="pi pi-inbox"
    />

    <!-- Conteúdo do Dashboard -->
    <template v-else-if="dashboardData">

      <!-- BLOCO 1 — RESUMO FINANCEIRO -->
      <div class="resumo-financeiro">
        <div class="saldo-card" :class="[saldoClasse, { 'risco': saldoInsuficiente }]">
          <div class="saldo-card-inner">
            <div class="saldo-header">
              <span class="saldo-icone">$</span>
              <span class="saldo-label">Saldo disponível</span>
            </div>
            <h2 class="saldo-valor">{{ formatarValor(dashboardData.saldo || 0) }}</h2>
            <div v-if="saldoInsuficiente" class="saldo-aviso">⚠️ Saldo pode não cobrir as contas pendentes</div>
            <div v-else class="saldo-badges">
              <span v-if="saldoBadgeNegativo" class="saldo-badge saldo-badge-negativo">{{ saldoBadgeNegativo }}</span>
              <span v-else-if="saldoContextoPositivo" class="saldo-badge">{{ saldoContextoPositivo }}</span>
              <span v-else-if="saldoContextoNegativo" class="saldo-badge saldo-badge-negativo">{{ saldoContextoNegativo }}</span>
            </div>
            <div class="saldo-breakdown">
              <span class="breakdown-receitas">Receitas {{ formatarValor(dashboardData.total_receitas || 0) }}</span>
              <span class="breakdown-sep">•</span>
              <span class="breakdown-despesas">Despesas {{ formatarValor(dashboardData.total_mes || 0) }}</span>
            </div>
          </div>
        </div>

        <div class="pizza-card">
          <h3 class="pizza-title">Despesas por categoria</h3>
          <div v-if="categoriaDominante && rankingCategorias.length > 1" class="pizza-chart-wrapper">
            <div class="chart-wrapper-pizza">
              <canvas ref="categoriaChartRef"></canvas>
            </div>
          </div>
          <div v-else-if="categoriaDominante" class="categoria-unica">
            <div class="categoria-unica-label">Categoria dominante</div>
            <div class="categoria-unica-nome">{{ categoriaDominante.nome }}</div>
            <div class="categoria-unica-valor">{{ formatarValor(categoriaDominante.total) }}</div>
            <div class="categoria-unica-pct">{{ ((categoriaDominante.total / (dashboardData.total_mes || 1)) * 100).toFixed(0) }}% dos gastos registrados</div>
          </div>
          <div v-else class="pizza-vazia">
            <span>Sem gastos por categoria neste período</span>
          </div>
          <div v-if="categoriaDominante" class="pizza-insight-card">
            <span class="pizza-insight-icon">🏆</span>
            <span class="pizza-insight-text">
              <strong>{{ categoriaDominante.nome }}</strong> representa <strong>{{ categoriaDominante.percentual }}%</strong> dos gastos
            </span>
          </div>
        </div>

        <div class="resumo-row-secundaria">
          <div class="resumo-card-mini receita-card">
            <div class="resumo-card-header">
              <span class="resumo-card-icon">📈</span>
              <span class="resumo-card-label">Receitas</span>
            </div>
            <h3 class="resumo-mini-valor">{{ formatarValor(dashboardData.total_receitas || 0) }}</h3>
            <p v-if="receitasMetaTexto" class="resumo-mini-meta">
              <span class="meta-dot dot-receita"></span>{{ receitasMetaTexto }}
            </p>
          </div>
          <div class="resumo-card-mini despesa-card">
            <div class="resumo-card-header">
              <span class="resumo-card-icon">📉</span>
              <span class="resumo-card-label">Despesas</span>
            </div>
            <h3 class="resumo-mini-valor">{{ formatarValor(dashboardData.total_mes || 0) }}</h3>
            <p v-if="despesasMetaTexto" class="resumo-mini-meta">
              <span class="meta-dot dot-despesa"></span>{{ despesasMetaTexto }}
            </p>
          </div>
        </div>
      </div>

      <!-- Previsão de Saldo -->
      <div v-if="dashboardData.previsao_mensagem" class="previsao-card" :class="{ 'negativa': (dashboardData.saldo_projetado || 0) < 0 }">
        <span class="previsao-icon">{{ (dashboardData.saldo_projetado || 0) < 0 ? '🔮' : '🔮' }}</span>
        <p>{{ dashboardData.previsao_mensagem }}</p>
      </div>

      <!-- Seção do Meio: 2 colunas -->
      <div class="dashboard-mid-grid">
        <div class="mid-card mid-card-insights">
          <h3 class="mid-card-title">Insights do período</h3>
          <DashboardInsights :data="dashboardData" />
        </div>

        <div class="mid-card mid-card-comportamento">
          <h3 class="mid-card-title">Comportamento financeiro</h3>
          <div class="stats-grid bloco-comportamento">
            <div class="stat-card mini primary">
              <div class="stat-icon">💰</div>
              <div class="stat-content">
                <h3>{{ formatarValor(dashboardData.total_mes || 0) }}</h3>
                <p>Total de despesas no mês</p>
                <small>{{ dashboardData.quantidade_gastos || 0 }} registros</small>
              </div>
            </div>

            <div class="stat-card mini warning" v-if="categoriaDominante">
              <div class="stat-icon">🏆</div>
              <div class="stat-content">
                <h3>{{ categoriaDominante.nome }}</h3>
                <p>Seu maior foco de despesas</p>
                <small>{{ categoriaDominante.percentual }}% das despesas</small>
              </div>
            </div>

            <div :class="['stat-card', 'mini', 'comparativo', variacaoClasse]" v-if="mostrarComparacao">
              <div class="stat-icon">{{ variacaoIcone }}</div>
              <div class="stat-content">
                <h3>{{ formatarVariacao(dashboardData.variacao_percentual) }}</h3>
                <p>Comparado ao mês passado</p>
                <small>{{ formatarValor(Math.abs(dashboardData.variacao_absoluta)) }}</small>
              </div>
            </div>
          </div>
        </div>

        <div class="mid-card mid-card-evolucao">
          <h3 class="mid-card-title">Evolução mensal</h3>
          <div class="chart-wrapper-evolucao">
            <canvas ref="evolucaoChartRef"></canvas>
          </div>
        </div>
      </div>

      <!-- BLOCO 3 — METAS DO MÊS -->
      <div v-if="metasPorCategoria.length" class="block-title">Metas do Mês</div>
      <div v-if="metasPorCategoria.length" class="budget-mini-grid">
        <div
          v-for="meta in metasPorCategoria"
          :key="meta.id"
          class="budget-mini-card"
          :class="meta.status"
        >
          <div class="budget-mini-header">
            <span class="budget-categoria">{{ meta.categoria_nome }}</span>
            <span class="budget-pct" :class="meta.status">{{ meta.percentual_usado }}%</span>
          </div>
          <div class="budget-mini-bar">
            <div class="budget-mini-fill" :class="meta.status" :style="{width: Math.min(meta.percentual_usado, 100) + '%'}"></div>
          </div>
          <div class="budget-mini-values">
            {{ formatarValor(meta.gasto_realizado) }} / {{ formatarValor(meta.valor_meta) }}
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import EmptyState from './EmptyState.vue'
import DashboardInsights from './DashboardInsights.vue'
import { fetchDashboard } from '../config/api.js'

Chart.register(...registerables)

const MES_NOMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

const hoje = new Date()
const periodo = ref({
  mes: hoje.getMonth() + 1,
  ano: hoje.getFullYear()
})
const dashboardData = ref(null)
const loading = ref(false)
let categoriaChart = null
let evolucaoChart = null

const categoriaChartRef = ref(null)
const evolucaoChartRef = ref(null)

const mesesNomes = computed(() => MES_NOMES)
const anosDisponiveis = computed(() => {
  const atual = new Date().getFullYear()
  return [atual, atual - 1, atual - 2]
})
const variacaoClasse = computed(() => {
  if (!dashboardData.value) return 'neutral'
  return dashboardData.value.variacao_percentual <= 0 ? 'positive' : 'negative'
})
const variacaoIcone = computed(() => {
  if (!dashboardData.value) return '➖'
  return dashboardData.value.variacao_percentual <= 0 ? '↓' : '↑'
})
const saldoClasse = computed(() => {
  if (!dashboardData.value || dashboardData.value.saldo === undefined) return 'neutral'
  return dashboardData.value.saldo >= 0 ? 'positive' : 'negative'
})
const saldoInsuficiente = computed(() => {
  if (!dashboardData.value) return false
  const saldo = dashboardData.value.saldo || 0
  const aPagar = dashboardData.value.total_a_pagar || 0
  return aPagar > 0 && saldo < aPagar
})
const categoriaDominante = computed(() => {
  const ranking = dashboardData.value?.ranking_categorias
  if (!ranking || ranking.length === 0) return null
  return ranking[0]
})
const mostrarComparacao = computed(() => {
  if (!dashboardData.value) return false
  const abs = Math.abs(dashboardData.value.variacao_absoluta || 0)
  return abs > 0.01
})
const metasPorCategoria = computed(() => {
  if (!dashboardData.value || !dashboardData.value.metas) return []
  const metas = dashboardData.value.metas.por_categoria || []
  return [...metas].sort((a, b) => b.percentual_usado - a.percentual_usado)
})

const rankingCategorias = computed(() => {
  return dashboardData.value?.ranking_categorias || []
})

const saldoPctDisponivel = computed(() => {
  if (!dashboardData.value) return ''
  const saldo = dashboardData.value.saldo || 0
  const receitas = dashboardData.value.total_receitas || 0
  if (receitas > 0) {
    return ((saldo / receitas) * 100).toFixed(0)
  }
  return ''
})

const saldoBadgeNegativo = computed(() => {
  if (!dashboardData.value) return ''
  const saldo = dashboardData.value.saldo || 0
  if (saldo >= 0) return ''
  const receitas = dashboardData.value.total_receitas || 0
  const despesas = dashboardData.value.total_mes || 0
  if (receitas > 0 && despesas > receitas) {
    return 'Despesas acima das receitas'
  }
  return 'Saldo comprometido'
})

const saldoContextoPositivo = computed(() => {
  if (!dashboardData.value) return ''
  const saldo = dashboardData.value.saldo || 0
  if (saldo < 0) return ''
  const receitas = dashboardData.value.total_receitas || 0
  if (receitas > 0) {
    const pct = ((saldo / receitas) * 100).toFixed(0)
    return `${pct}% da receita permanece disponível`
  }
  return 'Você encerra o período com saldo positivo'
})

const saldoContextoNegativo = computed(() => {
  if (!dashboardData.value) return ''
  const saldo = dashboardData.value.saldo || 0
  if (saldo >= 0) return ''
  const receitas = dashboardData.value.total_receitas || 0
  const despesas = dashboardData.value.total_mes || 0
  if (receitas > 0) {
    const pct = ((Math.abs(saldo) / receitas) * 100).toFixed(0)
    return `${pct}% da receita foi comprometida`
  }
  if (despesas > 0) {
    return 'Despesas superaram as receitas neste período'
  }
  return ''
})

const saldoMetaTexto = computed(() => {
  if (!dashboardData.value) return ''
  const saldo = dashboardData.value.saldo || 0
  const receitas = dashboardData.value.total_receitas || 0
  const despesas = dashboardData.value.total_mes || 0

  if (receitas > 0 && despesas > 0) {
    return `Receitas ${formatarValor(receitas)} • Despesas ${formatarValor(despesas)}`
  }

  return saldo >= 0 ? 'Saldo positivo neste período' : 'Saldo negativo neste período'
})

const receitasMetaTexto = computed(() => {
  if (!dashboardData.value) return ''
  const receitas = dashboardData.value.total_receitas || 0
  const anterior = dashboardData.value.total_receitas_anterior
  if (receitas > 0 && anterior > 0) {
    const diff = ((receitas - anterior) / anterior) * 100
    const sinal = diff >= 0 ? '↑' : '↓'
    return `${sinal} ${Math.abs(diff).toFixed(0)}% vs período anterior`
  }
  return ''
})

const despesasMetaTexto = computed(() => {
  if (!dashboardData.value) return ''
  const despesas = dashboardData.value.total_mes || 0
  const receitas = dashboardData.value.total_receitas || 0
  const partes = []

  if (receitas > 0 && despesas > 0) {
    const pct = ((despesas / receitas) * 100).toFixed(0)
    partes.push(`${pct}% da receita comprometida`)
  }

  const variacao = dashboardData.value.variacao_percentual
  const abs = Math.abs(dashboardData.value.variacao_absoluta || 0)
  if (abs > 0.01 && variacao !== undefined) {
    const sinal = variacao <= 0 ? '↓' : '↑'
    partes.push(`${sinal} ${Math.abs(variacao).toFixed(0)}% vs período anterior`)
  }

  return partes.join(' • ')
})

onMounted(() => {
  carregarDashboard()
})

watch(periodo, () => {
  carregarDashboard()
}, { deep: true })

async function carregarDashboard() {
  try {
    loading.value = true
    dashboardData.value = await fetchDashboard(periodo.value.mes, periodo.value.ano)
  } catch (err) {
    console.error('Erro ao carregar dashboard:', err)
  } finally {
    loading.value = false
    nextTick(() => {
      destroyCharts()
      initCharts()
    })
  }
}

function initCharts() {
  if (!dashboardData.value) return
  initCategoriaChart()
  initEvolucaoChart()
}

function destroyCharts() {
  if (categoriaChart) {
    categoriaChart.destroy()
    categoriaChart = null
  }
  if (evolucaoChart) {
    evolucaoChart.destroy()
    evolucaoChart = null
  }
}

function initCategoriaChart() {
  try {
    const ctx = categoriaChartRef.value
    if (!ctx) return

    if (categoriaChart) {
      categoriaChart.destroy()
      categoriaChart = null
    }

    const ranking = dashboardData.value.ranking_categorias
    if (!ranking || ranking.length === 0) return

    const cores = [
      '#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#06b6d4',
      '#ec4899', '#6b7280', '#10b981', '#f97316', '#6366f1'
    ]

    categoriaChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ranking.map(d => d.nome),
        datasets: [{
          data: ranking.map(d => d.total),
          backgroundColor: cores.slice(0, ranking.length),
          borderWidth: 2,
          borderColor: '#1f2937'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#e5e7eb',
              padding: 15,
              font: { size: 12 }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const value = formatarValor(context.parsed)
                const total = context.dataset.data.reduce((a, b) => a + b, 0)
                const percentage = ((context.parsed / total) * 100).toFixed(1)
                return `${value} (${percentage}%)`
              }
            }
          }
        }
      }
    })
  } catch (err) {
    console.error('Erro ao inicializar gráfico de categorias:', err)
  }
}

function initEvolucaoChart() {
  try {
    const ctx = evolucaoChartRef.value
    if (!ctx) return

    if (evolucaoChart) {
      evolucaoChart.destroy()
      evolucaoChart = null
    }

    const evolucao = dashboardData.value.evolucao_mensal || dashboardData.value.evolucao_12meses || []
    const labels = evolucao.map(e => `${e.mes}/${e.ano.toString().slice(-2)}`)
    const dadosReceitas = evolucao.map(e => e.receitas || 0)
    const dadosGastos = evolucao.map(e => e.gastos || e.total || 0)

    const chartCtx = ctx.getContext('2d')
    const gradReceitas = chartCtx.createLinearGradient(0, 0, 0, 300)
    gradReceitas.addColorStop(0, 'rgba(16, 185, 129, 0.18)')
    gradReceitas.addColorStop(1, 'rgba(16, 185, 129, 0)')

    const gradDespesas = chartCtx.createLinearGradient(0, 0, 0, 300)
    gradDespesas.addColorStop(0, 'rgba(239, 68, 68, 0.12)')
    gradDespesas.addColorStop(1, 'rgba(239, 68, 68, 0)')

    evolucaoChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Receitas',
            data: dadosReceitas,
            borderColor: 'rgba(16, 185, 129, 0.85)',
            backgroundColor: gradReceitas,
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: 'rgba(16, 185, 129, 0.85)',
            pointBorderColor: '#1f2937',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
          },
          {
            label: 'Despesas',
            data: dadosGastos,
            borderColor: 'rgba(239, 68, 68, 0.85)',
            backgroundColor: gradDespesas,
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: 'rgba(239, 68, 68, 0.85)',
            pointBorderColor: '#1f2937',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: { top: 4, bottom: 4, left: 4, right: 4 }
        },
        plugins: {
          legend: {
            position: 'top',
            align: 'end',
            labels: {
              color: '#e5e7eb',
              font: { size: 11 },
              usePointStyle: true,
              boxWidth: 8,
              padding: 10
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${formatarValor(context.parsed.y)}`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(255, 255, 255, 0.08)' },
            ticks: {
              color: '#9ca3af',
              font: { size: 10 },
              callback: (value) => formatarValor(value)
            },
            border: { display: false }
          },
          x: {
            grid: { display: false },
            ticks: {
              color: '#9ca3af',
              font: { size: 10 }
            },
            border: { display: false }
          }
        }
      }
    })
  } catch (err) {
    console.error('Erro ao inicializar gráfico de evolução:', err)
  }
}

function formatarValor(valor) {
  return parseFloat(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

function formatarVariacao(valor) {
  const sinal = valor > 0 ? '+' : ''
  return `${sinal}${valor.toFixed(1)}%`
}
</script>

<style scoped>
/* ── Tokens globais do dashboard ── */
.dashboard {
  --dashboard-gap: 16px;
  --card-padding-lg: 20px;
  --card-padding-md: 16px;
  --card-padding-sm: 12px;
  --label-font-size: 0.8rem;
  --label-font-weight: 600;
  --label-letter-spacing: 0.06em;
  --label-color: rgba(148, 163, 184, 0.8);
  --label-margin-bottom: 4px;
  --aux-font-size: 0.78rem;
  --aux-line-height: 1.4;
  --aux-color: rgba(148, 163, 184, 0.65);

  max-width: 1200px;
  margin: 0 auto;
  background: radial-gradient(ellipse at 50% 0%, rgba(30, 41, 59, 0.4) 0%, transparent 60%);
}

/* Títulos de bloco */
.block-title {
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
  margin: 32px 0 14px 0;
  padding-left: 4px;
}

/* Insights wrapper */
.insights-wrapper {
  max-width: 92%;
  margin: 0 auto;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  gap: var(--dashboard-gap);
  margin-bottom: 20px;
}

/* BLOCO 1: Resumo Financeiro */
.resumo-financeiro {
  display: grid;
  grid-template-columns: 3fr 2fr;
  grid-template-rows: auto auto;
  gap: var(--dashboard-gap);
  margin-bottom: var(--dashboard-gap);
  align-items: stretch;
}

.saldo-card {
  grid-column: 1;
  grid-row: 1;
}

.pizza-card {
  grid-column: 2;
  grid-row: 1 / 3;
}

.resumo-row-secundaria {
  grid-column: 1;
  grid-row: 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--dashboard-gap);
}

/* Saldo Card — protagonista */
.saldo-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 22px;
  padding: var(--card-padding-lg);
  display: flex;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.saldo-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.saldo-card.positive {
  border-left: 6px solid #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), #1e293b);
}

.saldo-card.negative {
  border-left: 6px solid #ef4444;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), #1e293b);
}

.saldo-card.neutral {
  border-left: 6px solid rgba(148, 163, 184, 0.4);
}

.saldo-card-inner {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  width: 100%;
}

.saldo-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

.saldo-icone {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.saldo-label {
  margin: 0 0 var(--label-margin-bottom) 0;
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
  text-align: center;
}

.saldo-valor {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.02em;
}

.saldo-card.positive .saldo-valor { color: #10b981; }
.saldo-card.negative .saldo-valor { color: #ef4444; }
.saldo-card.neutral .saldo-valor { color: #e5e7eb; }

.saldo-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.saldo-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.saldo-badge-negativo {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
}

.saldo-breakdown {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
  margin-top: 4px;
  width: 100%;
}

.breakdown-receitas {
  color: #10b981;
  font-weight: 500;
}

.breakdown-despesas {
  color: #ef4444;
  font-weight: 500;
}

.breakdown-sep {
  color: rgba(148, 163, 184, 0.5);
}

/* Estado de risco */
.saldo-card.risco {
  border-left: 6px solid #f59e0b;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), #1e293b);
  animation: pulse-risco 2s ease-in-out infinite;
}

.saldo-card.risco .saldo-valor {
  color: #f59e0b;
}

.saldo-aviso {
  margin: 4px 0 0 0;
  color: #fbbf24;
  font-weight: 500;
  font-size: 0.9rem;
}

@keyframes pulse-risco {
  0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.12); }
  50% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
}

/* Pizza Card */
.pizza-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 22px;
  padding: var(--card-padding-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  min-height: 0;
}

.pizza-title {
  margin: 0 0 var(--label-margin-bottom) 0;
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
  text-align: center;
}

.pizza-chart-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
  min-height: 0;
}

.chart-wrapper-pizza {
  position: relative;
  width: 100%;
  height: 180px;
}

.chart-wrapper-pizza canvas {
  max-width: 100% !important;
}

/* Categoria Única (sem gráfico) */
.categoria-unica {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: var(--card-padding-sm);
}

.categoria-unica-label {
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
}

.categoria-unica-nome {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e5e7eb;
}

.categoria-unica-valor {
  font-size: 1.1rem;
  font-weight: 600;
  color: #f59e0b;
}

.categoria-unica-pct {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

.pizza-vazia {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
  text-align: center;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pizza-insight-card {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

.pizza-insight-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.pizza-insight-text {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

.pizza-insight-text strong {
  color: #e5e7eb;
  font-weight: 600;
}

/* Linha 2: Receitas + Despesas (secundários) */
.resumo-row-secundaria {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--dashboard-gap);
}

.resumo-card-mini {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 16px;
  padding: var(--card-padding-md);
  border: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.resumo-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.resumo-card-icon {
  font-size: 1.1rem;
  opacity: 0.7;
}

.resumo-card-label {
  margin: 0 0 var(--label-margin-bottom) 0;
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
  text-align: center;
}

.receita-card .resumo-card-label { color: #10b981; }
.despesa-card .resumo-card-label { color: #ef4444; }

.resumo-mini-valor {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
  color: #e5e7eb;
}

.resumo-mini-meta {
  margin: 2px 0 0 0;
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
  display: flex;
  align-items: center;
  gap: 6px;
}

.meta-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}

.dot-receita { background: #10b981; }
.dot-despesa { background: #ef4444; }

.receita-card { border-left: 3px solid rgba(16, 185, 129, 0.4); }
.despesa-card { border-left: 3px solid rgba(239, 68, 68, 0.4); }

/* Mini Cards (Comportamento — secundário) */
.stat-card.mini {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 14px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: var(--transition-fast);
}

.stat-card.mini:hover {
  transform: var(--hover-lift);
  border-color: rgba(255, 255, 255, 0.1);
}

.stat-card.mini .stat-icon {
  font-size: 1.3rem;
  opacity: 0.6;
  flex-shrink: 0;
}

.stat-card.mini .stat-content h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: #cbd5e1;
}

.stat-card.mini .stat-content p {
  margin: 0 0 4px 0;
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
  font-weight: 500;
}

.stat-card.mini .stat-content small {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

/* Cores por tipo (secundário — mais sutis) */
.stat-card.receita { border-left: 3px solid rgba(16, 185, 129, 0.4); }
.stat-card.receita .stat-content h3 { color: rgba(16, 185, 129, 0.85); }

.stat-card.gasto-pago { border-left: 3px solid rgba(239, 68, 68, 0.4); }
.stat-card.gasto-pago .stat-content h3 { color: rgba(239, 68, 68, 0.85); }

.stat-card.gasto-pendente { border-left: 3px solid rgba(245, 158, 11, 0.32); }
.stat-card.gasto-pendente .stat-content h3 { color: rgba(245, 158, 11, 0.78); }

.stat-card.primary { border-left: 3px solid rgba(59, 130, 246, 0.4); }
.stat-card.primary .stat-content h3 { color: rgba(59, 130, 246, 0.85); }

.stat-card.warning { border-left: 3px solid rgba(245, 158, 11, 0.4); }
.stat-card.warning .stat-content h3 { color: rgba(245, 158, 11, 0.85); }

/* Comparativo */
.stat-card.comparativo.positive { border-left-color: rgba(16, 185, 129, 0.4); }
.stat-card.comparativo.positive .stat-content h3 { color: rgba(16, 185, 129, 0.85); }
.stat-card.comparativo.negative { border-left-color: rgba(239, 68, 68, 0.4); }
.stat-card.comparativo.negative .stat-content h3 { color: rgba(239, 68, 68, 0.85); }
.stat-card.comparativo.neutral { border-left-color: rgba(107, 114, 128, 0.4); }

/* BLOCO 2: Comportamento */
.bloco-comportamento {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

/* Previsão Card */
.previsao-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(59, 130, 246, 0.04);
  border: 1px solid rgba(59, 130, 246, 0.12);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin: 0 auto var(--dashboard-gap) auto;
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: #93c5fd;
  max-width: 600px;
}

.previsao-card.negativa {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), #1e293b);
  border-color: rgba(239, 68, 68, 0.3);
  color: #f87171;
  animation: pulse-risco 2.5s ease-in-out infinite;
}

.previsao-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
  opacity: 0.7;
}

.previsao-card p {
  margin: 0;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--dashboard-gap);
  margin-top: 8px;
}

.chart-container {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: var(--card-padding-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-width: 0;
  overflow: hidden;
}

.chart-container h3 {
  margin: 0 0 18px 0;
  color: #e5e7eb;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  height: 255px;
  overflow: hidden;
}

.chart-evolucao .chart-wrapper {
  padding-top: 6px;
}

.chart-wrapper canvas {
  max-width: 100% !important;
}

.chart-mini-insight {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

.chart-mini-insight i {
  font-size: 0.8rem;
  color: var(--color-brand);
  flex-shrink: 0;
}

.chart-mini-insight strong {
  color: #e5e7eb;
  font-weight: 600;
}

/* Dashboard Mid Grid (2 colunas) */
.dashboard-mid-grid {
  display: grid;
  grid-template-columns: 1fr 1.8fr;
  grid-auto-rows: auto;
  gap: var(--dashboard-gap);
  margin-bottom: var(--dashboard-gap);
  align-items: stretch;
}

.mid-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
  overflow: hidden;
}

.mid-card-title,
.mid-card-insights .mid-card-title,
.mid-card-comportamento .mid-card-title,
.mid-card-evolucao .mid-card-title {
  margin: 0 0 var(--label-margin-bottom) 0;
  font-size: var(--label-font-size);
  font-weight: var(--label-font-weight);
  text-transform: uppercase;
  letter-spacing: var(--label-letter-spacing);
  color: var(--label-color);
  text-align: center;
}

/* Insights — compacto, leitura rápida (~30% da coluna) */
.mid-card-insights {
  grid-column: 1;
  grid-row: 1;
  padding: 6px 8px;
  gap: 1px;
}

/* Comportamento — valorizado (~70% da coluna) */
.mid-card-comportamento {
  grid-column: 1;
  grid-row: 2;
  padding: 8px 10px;
  gap: 4px;
}

.mid-card-comportamento .bloco-comportamento {
  grid-template-columns: 1fr;
  gap: 3px;
}

.mid-card-comportamento .stat-card.mini {
  padding: 6px 8px;
  border-radius: 8px;
}

.mid-card-comportamento .stat-card.mini .stat-icon {
  font-size: 1.2rem;
}

.mid-card-comportamento .stat-card.mini .stat-content h3 {
  font-size: 1.05rem;
}

.mid-card-comportamento .stat-card.mini .stat-content p {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

.mid-card-comportamento .stat-card.mini .stat-content small {
  font-size: var(--aux-font-size);
  line-height: var(--aux-line-height);
  color: var(--aux-color);
}

/* Evolução — reduzida e alinhada exatamente à coluna esquerda */
.mid-card-evolucao {
  grid-column: 2;
  grid-row: 1 / 3;
  padding: 8px 10px;
  gap: 2px;
}

.chart-wrapper-evolucao {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.chart-wrapper-evolucao canvas {
  max-width: 100% !important;
}

/* Period Selector */
.period-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  justify-content: center;
}

.period-select {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px 16px;
  color: #e5e7eb;
  font-size: 14px;
  cursor: pointer;
  min-width: 140px;
}

.period-select:focus {
  outline: none;
  border-color: #60A637;
}

.period-select option {
  background: #1e293b;
  color: #e5e7eb;
}

/* Dashboard Loading */
.dashboard-loading {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.dashboard-loading i {
  font-size: 2rem;
  margin-bottom: 12px;
  display: block;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard {
    padding: 12px;
  }

  .resumo-financeiro {
    gap: 12px;
  }

  /* Mobile: coluna única */
  .resumo-financeiro {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .saldo-card {
    grid-column: 1;
    grid-row: auto;
  }

  .pizza-card {
    grid-column: 1;
    grid-row: auto;
  }

  .resumo-row-secundaria {
    grid-column: 1;
    grid-row: auto;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .insights-wrapper {
    max-width: 100%;
  }

  .saldo-card {
    width: 100%;
    padding: 24px;
    border-radius: 18px;
    box-sizing: border-box;
  }

  .saldo-valor {
    font-size: clamp(1.8rem, 7vw, 2.2rem);
    white-space: nowrap;
  }

  .saldo-meta {
    font-size: 0.85rem;
  }

  .pizza-card {
    padding: 16px;
    border-radius: 18px;
  }

  .chart-wrapper-pizza {
    height: 200px;
  }

  .resumo-card-mini {
    padding: 16px;
    border-radius: 14px;
  }

  .resumo-mini-valor {
    font-size: 1.15rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .bloco-comportamento {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .chart-wrapper {
    height: 240px;
  }

  .chart-mini-insight {
    font-size: 0.8rem;
    padding: 6px 10px;
    margin-top: 8px;
  }

  .dashboard-mid-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    gap: 12px;
  }

  .mid-card-insights,
  .mid-card-comportamento,
  .mid-card-evolucao {
    grid-column: 1;
    grid-row: auto;
  }

  .mid-card {
    padding: 16px;
  }

  .chart-wrapper-evolucao {
    height: 240px;
    flex: none;
  }

  .period-selector {
    flex-direction: column;
    align-items: stretch;
  }

  .period-select {
    width: 100%;
  }
}

/* Budget Mini Block */
.budget-mini-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--dashboard-gap);
  margin-bottom: 20px;
}

.budget-mini-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-left: 3px solid #10b981;
}

.budget-mini-card.ok { border-left-color: #10b981; }
.budget-mini-card.warning { border-left-color: #f59e0b; }
.budget-mini-card.danger { border-left-color: #ef4444; }
.budget-mini-card.critical { border-left-color: #dc2626; }

.budget-mini-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.budget-categoria {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e5e7eb;
}

.budget-pct {
  font-size: 0.8rem;
  font-weight: 700;
}

.budget-pct.ok { color: #10b981; }
.budget-pct.warning { color: #f59e0b; }
.budget-pct.danger { color: #ef4444; }
.budget-pct.critical { color: #dc2626; }

.budget-mini-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 6px;
}

.budget-mini-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease-out;
}

.budget-mini-fill.ok { background: #10b981; }
.budget-mini-fill.warning { background: #f59e0b; }
.budget-mini-fill.danger { background: #ef4444; }
.budget-mini-fill.critical { background: #dc2626; }

.budget-mini-values {
  font-size: 0.8rem;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .budget-mini-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .budget-mini-grid {
    grid-template-columns: 1fr;
  }
}
</style>
