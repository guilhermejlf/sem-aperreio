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

    <!-- Estado Vazio -->
    <div v-else-if="dashboardData && dashboardData.quantidade_gastos === 0" class="empty-state">
      <i class="pi pi-inbox"></i>
      <h3>Nenhum gasto neste período</h3>
      <p v-if="dashboardData.periodo">
        Adicione um gasto para ver o dashboard de {{ dashboardData.periodo.mes_nome }} {{ dashboardData.periodo.ano }}.
      </p>
    </div>

    <!-- Conteúdo do Dashboard -->
    <template v-else-if="dashboardData">
      <!-- Cards de Estatísticas -->
      <div class="stats-grid">
        <div class="stat-card primary">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_mes) }}</h3>
            <p>Total do Mês</p>
            <small>{{ dashboardData.quantidade_gastos }} gastos</small>
          </div>
        </div>

        <div :class="['stat-card', 'comparativo', variacaoClasse]">
          <div class="stat-icon">{{ variacaoIcone }}</div>
          <div class="stat-content">
            <h3>{{ formatarVariacao(dashboardData.variacao_percentual) }}</h3>
            <p>vs. Mês Anterior</p>
            <small>{{ formatarValor(Math.abs(dashboardData.variacao_absoluta)) }}</small>
          </div>
        </div>

        <div class="stat-card success">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.media_diaria) }}</h3>
            <p>Média Diária</p>
            <small>{{ dashboardData.periodo.mes_nome }}</small>
          </div>
        </div>

        <div class="stat-card warning">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <h3>{{ dashboardData.maior_gasto ? formatarValor(dashboardData.maior_gasto.valor) : 'R$ 0,00' }}</h3>
            <p>Maior Gasto</p>
            <small>{{ dashboardData.maior_gasto ? dashboardData.maior_gasto.categoria : '-' }}</small>
          </div>
        </div>

        <div class="stat-card receita">
          <div class="stat-icon">📈</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_receitas || 0) }}</h3>
            <p>Receitas do Mês</p>
            <small>Entradas</small>
          </div>
        </div>

        <div class="stat-card gasto-pago">
          <div class="stat-icon">💸</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.total_gastos_pagos || 0) }}</h3>
            <p>Gastos Pagos</p>
            <small>Saídas confirmadas</small>
          </div>
        </div>

        <div class="stat-card saldo" :class="saldoClasse">
          <div class="stat-icon">⚖️</div>
          <div class="stat-content">
            <h3>{{ formatarValor(dashboardData.saldo || 0) }}</h3>
            <p>Saldo</p>
            <small>Receitas - Gastos Pagos</small>
          </div>
        </div>
      </div>

      <!-- Gráficos -->
      <div class="charts-grid">
        <div class="chart-container">
          <h3>Gastos por Categoria</h3>
          <div class="chart-wrapper">
            <canvas ref="categoriaChart"></canvas>
          </div>
        </div>

        <div class="chart-container">
          <h3>Evolução Mensal</h3>
          <div class="chart-wrapper">
            <canvas ref="evolucaoChart"></canvas>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
import { fetchDashboard } from '../config/api.js'

Chart.register(...registerables)

const MES_NOMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

export default {
  name: 'DashboardCharts',
  data() {
    const hoje = new Date()
    return {
      periodo: {
        mes: hoje.getMonth() + 1,
        ano: hoje.getFullYear()
      },
      dashboardData: null,
      loading: false,
      categoriaChart: null,
      evolucaoChart: null
    }
  },
  computed: {
    mesesNomes() {
      return MES_NOMES
    },
    anosDisponiveis() {
      const atual = new Date().getFullYear()
      return [atual, atual - 1, atual - 2]
    },
    variacaoClasse() {
      if (!this.dashboardData) return 'neutral'
      return this.dashboardData.variacao_percentual <= 0 ? 'positive' : 'negative'
    },
    variacaoIcone() {
      if (!this.dashboardData) return '➖'
      return this.dashboardData.variacao_percentual <= 0 ? '↓' : '↑'
    },
    saldoClasse() {
      if (!this.dashboardData || this.dashboardData.saldo === undefined) return 'neutral'
      return this.dashboardData.saldo >= 0 ? 'positive' : 'negative'
    }
  },
  mounted() {
    this.carregarDashboard()
  },
  watch: {
    periodo: {
      deep: true,
      handler() {
        this.carregarDashboard()
      }
    }
  },
  methods: {
    async carregarDashboard() {
      try {
        this.loading = true
        this.dashboardData = await fetchDashboard(this.periodo.mes, this.periodo.ano)
      } catch (error) {
        console.error('Erro ao carregar dashboard:', error)
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.destroyCharts()
          this.initCharts()
        })
      }
    },

    initCharts() {
      if (!this.dashboardData) return
      this.initCategoriaChart()
      this.initEvolucaoChart()
    },

    destroyCharts() {
      if (this.categoriaChart) {
        this.categoriaChart.destroy()
        this.categoriaChart = null
      }
      if (this.evolucaoChart) {
        this.evolucaoChart.destroy()
        this.evolucaoChart = null
      }
    },

    initCategoriaChart() {
      try {
        const ctx = this.$refs.categoriaChart
        if (!ctx) return

        if (this.categoriaChart) {
          this.categoriaChart.destroy()
          this.categoriaChart = null
        }

        const ranking = this.dashboardData.ranking_categorias
        if (!ranking || ranking.length === 0) return

        const cores = [
          '#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#06b6d4',
          '#ec4899', '#6b7280', '#10b981', '#f97316', '#6366f1'
        ]

        this.categoriaChart = new Chart(ctx, {
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
                    const value = this.formatarValor(context.parsed)
                    const total = context.dataset.data.reduce((a, b) => a + b, 0)
                    const percentage = ((context.parsed / total) * 100).toFixed(1)
                    return `${value} (${percentage}%)`
                  }
                }
              }
            }
          }
        })
      } catch (error) {
        console.error('Erro ao inicializar gráfico de categorias:', error)
      }
    },

    initEvolucaoChart() {
      try {
        const ctx = this.$refs.evolucaoChart
        if (!ctx) return

        if (this.evolucaoChart) {
          this.evolucaoChart.destroy()
          this.evolucaoChart = null
        }

        const evolucao = this.dashboardData.evolucao_mensal || this.dashboardData.evolucao_12meses || []
        const labels = evolucao.map(e => `${e.mes}/${e.ano.toString().slice(-2)}`)
        const dadosReceitas = evolucao.map(e => e.receitas || 0)
        const dadosGastos = evolucao.map(e => e.gastos || e.total || 0)

        this.evolucaoChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels,
            datasets: [
              {
                label: 'Receitas',
                data: dadosReceitas,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#1f2937',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
              },
              {
                label: 'Gastos',
                data: dadosGastos,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.05)',
                borderWidth: 3,
                tension: 0.4,
                fill: false,
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#1f2937',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
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
                    return `${context.dataset.label}: ${this.formatarValor(context.parsed.y)}`
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
                  callback: (value) => this.formatarValor(value)
                }
              },
              x: {
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#9ca3af' }
              }
            }
          }
        })
      } catch (error) {
        console.error('Erro ao inicializar gráfico de evolução:', error)
      }
    },

    formatarValor(valor) {
      return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    formatarVariacao(valor) {
      const sinal = valor > 0 ? '+' : ''
      return `${sinal}${valor.toFixed(1)}%`
    },

  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.stat-card.primary { border-left: 4px solid #22c55e; }
.stat-card.success { border-left: 4px solid #3b82f6; }
.stat-card.warning { border-left: 4px solid #f59e0b; }
.stat-card.info { border-left: 4px solid #06b6d4; }
.stat-card.receita { border-left: 4px solid #10b981; }
.stat-card.gasto-pago { border-left: 4px solid #ef4444; }

.stat-card.saldo.neutral { border-left: 4px solid #6b7280; }
.stat-card.saldo.positive { border-left: 4px solid #22c55e; }
.stat-card.saldo.positive .stat-content h3 { color: #22c55e; }
.stat-card.saldo.negative { border-left: 4px solid #ef4444; }
.stat-card.saldo.negative .stat-content h3 { color: #ef4444; }

.stat-card.receita .stat-content h3 { color: #10b981; }
.stat-card.gasto-pago .stat-content h3 { color: #ef4444; }

.stat-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.stat-content h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 0 5px 0;
  color: #22c55e;
}

.stat-content p {
  margin: 0 0 5px 0;
  color: #e5e7eb;
  font-weight: 500;
}

.stat-content small {
  color: #9ca3af;
  font-size: 0.85rem;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.chart-container {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.chart-container h3 {
  margin: 0 0 20px 0;
  color: #e5e7eb;
  font-size: 1.2rem;
  text-align: center;
}

.chart-wrapper {
  position: relative;
  height: 300px;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard {
    padding: 10px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .charts-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .chart-wrapper {
    height: 250px;
  }

  .category-item {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }

  .category-info {
    justify-content: center;
  }
}

/* Period Selector */
.period-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
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
  border-color: #22c55e;
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

/* Comparativo Card */
.stat-card.comparativo.positive {
  border-left-color: #22c55e;
}

.stat-card.comparativo.positive .stat-icon {
  color: #22c55e;
}

.stat-card.comparativo.positive h3 {
  color: #22c55e;
}

.stat-card.comparativo.negative {
  border-left-color: #ef4444;
}

.stat-card.comparativo.negative .stat-icon {
  color: #ef4444;
}

.stat-card.comparativo.negative h3 {
  color: #ef4444;
}

.stat-card.comparativo.neutral {
  border-left-color: #6b7280;
}

/* Empty State dentro do dashboard */
.dashboard .empty-state {
  background: rgba(30, 41, 59, 0.3);
  border-radius: 20px;
  padding: 60px 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .period-selector {
    flex-direction: column;
    align-items: stretch;
  }

  .period-select {
    width: 100%;
  }
}
</style>
