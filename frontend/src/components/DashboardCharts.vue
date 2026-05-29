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

      <!-- BLOCO 1 — SITUAÇÃO FINANCEIRA -->
      <div class="block-title">Situação Financeira</div>
      <div class="stats-grid bloco-situacao">
        <!-- Saldo (DESTAQUE) -->
        <div class="stat-card saldo-destaque" :class="[saldoClasse, { 'risco': saldoInsuficiente }]">
          <div class="stat-icon-saldo">{{ saldoInsuficiente ? '⚠️' : saldoIcone }}</div>
          <div class="stat-content">
            <p class="saldo-label">Saldo disponível</p>
            <h2 class="saldo-valor">{{ formatarValor(dashboardData.saldo || 0) }}</h2>
            <small v-if="saldoInsuficiente" class="saldo-aviso">Saldo pode não cobrir as contas pendentes</small>
            <small v-else>Receitas - Contas pagas</small>
          </div>
        </div>

        <div class="stat-card mini receita">
          <div class="stat-icon">📈</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_receitas || 0) }}</h3>
            <p>Receitas no mês</p>
          </div>
        </div>

        <div class="stat-card mini gasto-pago">
          <div class="stat-icon">💸</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_gastos_pagos || 0) }}</h3>
            <p>Contas pagas</p>
          </div>
        </div>

        <div class="stat-card mini gasto-pendente" v-if="(dashboardData.total_a_pagar || 0) > 0">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_a_pagar || 0) }}</h3>
            <p>Ainda a pagar</p>
            <small>{{ dashboardData.quantidade_pendentes || 0 }} conta{{ (dashboardData.quantidade_pendentes || 0) === 1 ? '' : 's' }}</small>
          </div>
        </div>
      </div>

      <!-- Previsão de Saldo -->
      <div v-if="dashboardData.previsao_mensagem" class="previsao-card" :class="{ 'negativa': (dashboardData.saldo_projetado || 0) < 0 }">
        <span class="previsao-icon">{{ (dashboardData.saldo_projetado || 0) < 0 ? '🔮' : '🔮' }}</span>
        <p>{{ dashboardData.previsao_mensagem }}</p>
      </div>

      <!-- Contextual Insights -->
      <div class="insights-wrapper">
        <DashboardInsights :data="dashboardData" />
      </div>

      <!-- BLOCO 2 — COMPORTAMENTO -->
      <div class="block-title">Comportamento</div>
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

      <!-- Gráficos -->
      <div class="charts-grid">
        <div class="chart-container">
          <h3>Despesas por Categoria</h3>
          <div class="chart-wrapper">
            <canvas ref="categoriaChartRef"></canvas>
          </div>
          <div v-if="categoriaDominante" class="chart-mini-insight">
            <i class="pi pi-chart-pie" />
            <span>
              <strong>{{ categoriaDominante.nome }}</strong> representa
              <strong>{{ ((categoriaDominante.total / (dashboardData.total_gastos || 1)) * 100).toFixed(0) }}%</strong>
              dos gastos
            </span>
          </div>
        </div>

        <div class="chart-container chart-evolucao">
          <h3>Evolução Mensal</h3>
          <div class="chart-wrapper">
            <canvas ref="evolucaoChartRef"></canvas>
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
const saldoIcone = computed(() => {
  if (!dashboardData.value || dashboardData.value.saldo === undefined) return '⚖️'
  return dashboardData.value.saldo >= 0 ? '🟢' : '🔴'
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
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#e5e7eb',
              font: { size: 12 },
              usePointStyle: true
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
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            ticks: {
              color: '#9ca3af',
              callback: (value) => formatarValor(value)
            }
          },
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            ticks: { color: '#9ca3af' }
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
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  background: radial-gradient(ellipse at 50% 0%, rgba(30, 41, 59, 0.4) 0%, transparent 60%);
}

/* Títulos de bloco */
.block-title {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(148, 163, 184, 0.75);
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
  gap: 16px;
  margin-bottom: 20px;
}

/* BLOCO 1: Situação Financeira */
.bloco-situacao {
  grid-template-columns: 1.5fr repeat(3, 1fr);
  align-items: stretch;
}

/* Saldo Destaque — âncora visual do dashboard */
.saldo-destaque {
  grid-row: span 1;
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 22px;
  padding: 28px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.saldo-destaque:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.saldo-destaque.positive {
  border-left: 6px solid #10b981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), #1e293b);
}

.saldo-destaque.negative {
  border-left: 6px solid #ef4444;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), #1e293b);
}

.saldo-destaque .stat-icon-saldo {
  font-size: 3rem;
  flex-shrink: 0;
}

.saldo-destaque .stat-content {
  flex: 1;
}

.saldo-label {
  margin: 0 0 6px 0;
  color: #94a3b8;
  font-size: 0.95rem;
  font-weight: 500;
}

.saldo-valor {
  font-size: 2.4rem;
  font-weight: 800;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.saldo-destaque.positive .saldo-valor { color: #10b981; }
.saldo-destaque.negative .saldo-valor { color: #ef4444; }
.saldo-destaque.neutral .saldo-valor { color: #e5e7eb; }

/* Estado de risco: saldo insuficiente para contas pendentes */
.saldo-destaque.risco {
  border-left: 6px solid #f59e0b;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), #1e293b);
  animation: pulse-risco 2s ease-in-out infinite;
}

.saldo-destaque.risco .saldo-valor {
  color: #f59e0b;
}

.saldo-aviso {
  color: #fbbf24 !important;
  font-weight: 500;
}

@keyframes pulse-risco {
  0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.12); }
  50% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
}

.saldo-destaque .stat-content small {
  color: rgba(148, 163, 184, 0.7);
  font-size: 0.85rem;
}

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
  font-size: 1.5rem;
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
  color: rgba(148, 163, 184, 0.85);
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.4;
}

.stat-card.mini .stat-content small {
  color: rgba(117, 133, 153, 0.8);
  font-size: 0.78rem;
  line-height: 1.3;
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
  margin: 0 auto 16px auto;
  font-size: 0.9rem;
  color: #93c5fd;
  line-height: 1.5;
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
  gap: 24px;
  margin-top: 8px;
}

.chart-container {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 24px;
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
  font-size: 0.85rem;
  color: #94a3b8;
  line-height: 1.4;
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

  .bloco-situacao {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .insights-wrapper {
    max-width: 100%;
  }

  .saldo-destaque {
    width: 100%;
    padding: 20px;
    border-radius: 18px;
    box-sizing: border-box;
  }

  .saldo-valor {
    font-size: clamp(1.3rem, 5.5vw, 1.7rem);
    white-space: nowrap;
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
  gap: 12px;
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
