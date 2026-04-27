<template>
  <div class="dashboard">
    <!-- Cards de Estatísticas -->
    <div class="stats-grid">
      <div class="stat-card primary">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>{{ formatarValor(totalMes) }}</h3>
          <p>Total do Mês</p>
          <small>{{ gastosDoMes.length }} gastos</small>
        </div>
      </div>
      
      <div class="stat-card success">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>{{ formatarValor(mediaDiaria) }}</h3>
          <p>Média Diária</p>
          <small>Últimos 30 dias</small>
        </div>
      </div>
      
      <div class="stat-card warning">
        <div class="stat-icon">🎯</div>
        <div class="stat-content">
          <h3>{{ formatarValor(maiorGasto) }}</h3>
          <p>Maior Gasto</p>
          <small>{{ maiorCategoria }}</small>
        </div>
      </div>
      
      <div class="stat-card info">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <h3>{{ totalGastos }}</h3>
          <p>Total Gastos</p>
          <small>Cadastrados</small>
        </div>
      </div>
    </div>

    <!-- Gráficos -->
    <div class="charts-grid">
      <!-- Gráfico de Pizza - Categorias -->
      <div class="chart-container">
        <h3>Gastos por Categoria</h3>
        <div class="chart-wrapper">
          <canvas ref="categoriaChart"></canvas>
        </div>
      </div>

      <!-- Gráfico de Linha - Evolução Mensal -->
      <div class="chart-container">
        <h3>Evolução Mensal</h3>
        <div class="chart-wrapper">
          <canvas ref="evolucaoChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Top Categorias -->
    <div class="top-categories">
      <h3>Top Categorias</h3>
      <div class="category-list">
        <div v-for="(cat, index) in topCategorias" :key="cat.nome" class="category-item">
          <div class="category-rank">{{ index + 1 }}</div>
          <div class="category-info">
            <div class="category-icon">{{ getCategoriaIcon(cat.nome) }}</div>
            <div class="category-details">
              <h4>{{ getCategoriaLabel(cat.nome) }}</h4>
              <small>{{ cat.quantidade }} gastos</small>
            </div>
          </div>
          <div class="category-value">
            <strong>{{ formatarValor(cat.total) }}</strong>
            <small>{{ ((cat.total / totalGeral) * 100).toFixed(1) }}%</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'DashboardCharts',
  props: {
    gastos: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      categoriaChart: null,
      evolucaoChart: null
    }
  },
  computed: {
    gastosDoMes() {
      const mesAtual = new Date().getMonth() + 1
      const anoAtual = new Date().getFullYear()
      
      return this.gastos.filter(g => {
        const dataGasto = new Date(g.data)
        return dataGasto.getMonth() + 1 === mesAtual && 
               dataGasto.getFullYear() === anoAtual
      })
    },

    totalMes() {
      return this.gastosDoMes.reduce((soma, g) => soma + parseFloat(g.valor), 0)
    },

    mediaDiaria() {
      const diasNoMes = new Date().getDate()
      return this.totalMes / diasNoMes
    },

    maiorGasto() {
      if (this.gastos.length === 0) return 0
      return Math.max(...this.gastos.map(g => parseFloat(g.valor)))
    },

    maiorCategoria() {
      if (this.gastos.length === 0) return 'N/A'
      const maior = this.gastos.reduce((max, g) => 
        parseFloat(g.valor) > parseFloat(max.valor) ? g : max
      )
      return this.getCategoriaLabel(maior.categoria)
    },

    totalGastos() {
      return this.gastos.length
    },

    dadosPorCategoria() {
      const categorias = {}
      
      this.gastos.forEach(gasto => {
        if (!categorias[gasto.categoria]) {
          categorias[gasto.categoria] = {
            nome: gasto.categoria,
            total: 0,
            quantidade: 0
          }
        }
        categorias[gasto.categoria].total += parseFloat(gasto.valor)
        categorias[gasto.categoria].quantidade += 1
      })

      return Object.values(categorias)
    },

    topCategorias() {
      return this.dadosPorCategoria
        .sort((a, b) => b.total - a.total)
        .slice(0, 5)
    },

    totalGeral() {
      return this.gastos.reduce((soma, g) => soma + parseFloat(g.valor), 0)
    },

    dadosEvolucaoMensal() {
      const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
      const dados = new Array(12).fill(0)
      
      this.gastos.forEach(gasto => {
        const data = new Date(gasto.data)
        const mes = data.getMonth()
        dados[mes] += parseFloat(gasto.valor)
      })

      return { meses, dados }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.gastos && this.gastos.length > 0) {
        this.initCharts()
      }
    })
  },
  watch: {
    gastos: {
      deep: true,
      handler(newVal, oldVal) {
        this.$nextTick(() => {
          if (!newVal || newVal.length === 0) {
            this.destroyCharts()
            return
          }
          if (!this.categoriaChart) {
            this.initCharts()
          } else {
            this.updateCharts()
          }
        })
      }
    }
  },
  methods: {
    initCharts() {
      if (!this.gastos || this.gastos.length === 0) return
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

        // Destruir gráfico anterior se existir
        if (this.categoriaChart) {
          this.categoriaChart.destroy()
          this.categoriaChart = null
        }

        const dados = JSON.parse(JSON.stringify(this.dadosPorCategoria))
        if (!dados || dados.length === 0) return

        const cores = [
          '#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#06b6d4',
          '#ec4899', '#6b7280', '#10b981', '#f97316', '#6366f1'
        ]

        this.categoriaChart = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: dados.map(d => this.getCategoriaLabel(d.nome)),
            datasets: [{
              data: dados.map(d => d.total),
              backgroundColor: cores.slice(0, dados.length),
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

        // Destruir gráfico anterior se existir
        if (this.evolucaoChart) {
          this.evolucaoChart.destroy()
          this.evolucaoChart = null
        }

        const { meses, dados } = JSON.parse(JSON.stringify(this.dadosEvolucaoMensal))

        this.evolucaoChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: meses,
            datasets: [{
              label: 'Gastos Mensais',
              data: dados,
              borderColor: '#22c55e',
              backgroundColor: 'rgba(34, 197, 94, 0.1)',
              borderWidth: 3,
              tension: 0.4,
              fill: true,
              pointBackgroundColor: '#22c55e',
              pointBorderColor: '#1f2937',
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 7
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    return `Gastos: ${this.formatarValor(context.parsed.y)}`
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#9ca3af',
                  callback: (value) => this.formatarValor(value)
                }
              },
              x: {
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#9ca3af'
                }
              }
            }
          }
        })
      } catch (error) {
        console.error('Erro ao inicializar gráfico de evolução:', error)
      }
    },

    updateCharts() {
      if (!this.gastos || this.gastos.length === 0) {
        this.destroyCharts()
        return
      }
      if (this.categoriaChart) {
        const dados = JSON.parse(JSON.stringify(this.dadosPorCategoria))
        const cores = [
          '#f59e0b', '#3b82f6', '#8b5cf6', '#ef4444', '#06b6d4',
          '#ec4899', '#6b7280', '#10b981', '#f97316', '#6366f1'
        ]

        this.categoriaChart.data.labels = dados.map(d => this.getCategoriaLabel(d.nome))
        this.categoriaChart.data.datasets[0].data = dados.map(d => d.total)
        this.categoriaChart.data.datasets[0].backgroundColor = cores.slice(0, dados.length)
        this.categoriaChart.update()
      }

      if (this.evolucaoChart) {
        const { dados } = JSON.parse(JSON.stringify(this.dadosEvolucaoMensal))
        this.evolucaoChart.data.datasets[0].data = dados
        this.evolucaoChart.update()
      }
    },

    formatarValor(valor) {
      return parseFloat(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      })
    },

    getCategoriaLabel(categoriaValue) {
      const categorias = {
        alimentacao: 'Alimentação',
        transporte: 'Transporte',
        moradia: 'Moradia',
        saude: 'Saúde',
        educacao: 'Educação',
        lazer: 'Lazer',
        outros: 'Outros'
      }
      return categorias[categoriaValue] || categoriaValue
    },

    getCategoriaIcon(categoria) {
      const icons = {
        alimentacao: '🍔',
        transporte: '🚗',
        moradia: '🏠',
        saude: '🏥',
        educacao: '📚',
        lazer: '🎮',
        outros: '📦'
      }
      return icons[categoria] || '💳'
    }
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

/* Top Categories */
.top-categories {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 25px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.top-categories h3 {
  margin: 0 0 20px 0;
  color: #e5e7eb;
  font-size: 1.2rem;
  text-align: center;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  transition: background 0.3s ease;
}

.category-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.category-rank {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #22c55e;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  font-size: 0.9rem;
}

.category-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.category-icon {
  font-size: 1.5rem;
}

.category-details h4 {
  margin: 0;
  color: #e5e7eb;
  font-size: 1rem;
}

.category-details small {
  color: #9ca3af;
  font-size: 0.85rem;
}

.category-value {
  text-align: right;
}

.category-value strong {
  color: #22c55e;
  font-size: 1.1rem;
  display: block;
}

.category-value small {
  color: #9ca3af;
  font-size: 0.85rem;
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
</style>
