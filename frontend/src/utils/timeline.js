/**
 * Agrupa itens financeiros por período temporal.
 * Retorna grupos ordenados: Hoje, Ontem, Esta semana, Mês, etc.
 */

function isSameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
         d1.getMonth() === d2.getMonth() &&
         d1.getDate() === d2.getDate()
}

function isYesterday(date, hoje) {
  const ontem = new Date(hoje)
  ontem.setDate(ontem.getDate() - 1)
  return isSameDay(date, ontem)
}

function isThisWeek(date, hoje) {
  const diff = hoje.getDate() - date.getDate()
  return diff > 1 && diff < 7 && date.getDay() >= hoje.getDay() - 6
}

function getGroupKey(item, hoje) {
  const data = new Date(item.data + 'T12:00:00')
  if (isNaN(data.getTime())) return 'Outros'

  if (isSameDay(data, hoje)) return 'Hoje'
  if (isYesterday(data, hoje)) return 'Ontem'
  if (isThisWeek(data, hoje)) return 'Esta semana'

  // Mês/Ano
  const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
  return `${meses[data.getMonth()]} ${data.getFullYear()}`
}

export function groupByTimeline(itens) {
  const hoje = new Date()
  hoje.setHours(0, 0, 0, 0)

  const grupos = {}

  for (const item of itens) {
    const key = getGroupKey(item, hoje)
    if (!grupos[key]) grupos[key] = []
    grupos[key].push(item)
  }

  // Ordem de prioridade dos grupos
  const ordem = ['Hoje', 'Ontem', 'Esta semana']
  const resultado = []

  // Primeiro os grupos conhecidos em ordem
  for (const key of ordem) {
    if (grupos[key]) {
      resultado.push({ titulo: key, itens: grupos[key] })
      delete grupos[key]
    }
  }

  // Depois os grupos de mês/ano (ordenados cronologicamente, mais recentes primeiro)
  const mesesRestantes = Object.keys(grupos)
    .filter(k => !ordem.includes(k) && k !== 'Outros')
    .sort((a, b) => {
      // Extrair mês/ano e comparar
      const parse = (s) => {
        const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
          'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        for (let i = 0; i < meses.length; i++) {
          if (s.includes(meses[i])) {
            const ano = parseInt(s.match(/\d{4}/)?.[0] || 0)
            return ano * 12 + i
          }
        }
        return 0
      }
      return parse(b) - parse(a)
    })

  for (const key of mesesRestantes) {
    resultado.push({ titulo: key, itens: grupos[key] })
    delete grupos[key]
  }

  // Finalmente "Outros"
  if (grupos['Outros']) {
    resultado.push({ titulo: 'Outros', itens: grupos['Outros'] })
  }

  return resultado
}

export function formatarDataContextual(dataStr, hoje = new Date()) {
  if (!dataStr) return ''
  try {
    const data = new Date(dataStr + 'T12:00:00')
    if (isNaN(data.getTime())) return dataStr

    if (isSameDay(data, hoje)) {
      return data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    }

    if (isYesterday(data, hoje)) {
      return 'Ontem'
    }

    const diffDias = Math.floor((hoje - data) / (1000 * 60 * 60 * 24))
    if (diffDias < 7) {
      return data.toLocaleDateString('pt-BR', { weekday: 'long' })
    }

    return data.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short'
    })
  } catch {
    return dataStr
  }
}
