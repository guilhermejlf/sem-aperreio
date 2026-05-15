/**
 * Dashboard Insights Engine
 * Gera insights contextuais, leves e humanos a partir dos dados do dashboard.
 */

const TIPOS = {
  CRITICAL: 'critical',
  WARNING: 'warning',
  INFO: 'info',
  POSITIVE: 'positive',
}

const PESOS = { [TIPOS.CRITICAL]: 4, [TIPOS.WARNING]: 3, [TIPOS.INFO]: 2, [TIPOS.POSITIVE]: 1 }

function formatarValor(valor) {
  return parseFloat(valor || 0).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

function gerarMensagensTendencia(variacaoPercentual, gastosMesAnterior) {
  const abs = Math.abs(variacaoPercentual)
  if (abs < 5) {
    return {
      tipo: TIPOS.INFO,
      mensagem: 'Teus gastos tão bem equilibrados em relação ao mês passado.',
      icone: 'pi pi-check-circle',
    }
  }
  if (variacaoPercentual > 0) {
    if (abs > 25) {
      return {
        tipo: TIPOS.WARNING,
        mensagem: `Teus gastos subiram ${abs.toFixed(0)}% em relação ao mês passado. Vale revisar onde tá indo o dinheiro.`,
        icone: 'pi pi-arrow-up',
      }
    }
    return {
      tipo: TIPOS.INFO,
      mensagem: `Gastos ${abs.toFixed(0)}% acima do mês passado. Nada demais, mas fica de olho.`,
      icone: 'pi pi-arrow-up',
    }
  }
  return {
    tipo: TIPOS.POSITIVE,
    mensagem: `Boa! Teus gastos diminuíram ${abs.toFixed(0)}% em relação ao mês passado.`,
    icone: 'pi pi-arrow-down',
  }
}

function gerarMensagensSaldo(saldo, totalAPagar) {
  if (totalAPagar <= 0) return null
  const cobertura = saldo / totalAPagar
  if (cobertura < 0.5) {
    return {
      tipo: TIPOS.CRITICAL,
      mensagem: `Saldo tá bem apertado. Ainda falta pagar ${formatarValor(totalAPagar)}.`,
      icone: 'pi pi-exclamation-circle',
    }
  }
  if (cobertura < 1) {
    return {
      tipo: TIPOS.WARNING,
      mensagem: `Ainda tem ${formatarValor(totalAPagar)} pra pagar. O saldo cobre parte.`,
      icone: 'pi pi-clock',
    }
  }
  return {
    tipo: TIPOS.POSITIVE,
    mensagem: `Saldo tranquilo pra cobrir os ${formatarValor(totalAPagar)} que ainda faltam.`,
    icone: 'pi pi-check-circle',
  }
}

function gerarMensagensMeta(meta) {
  const pct = meta.percentual_usado
  if (pct >= 100) {
    return {
      tipo: TIPOS.WARNING,
      mensagem: `Meta de ${meta.categoria_nome || 'geral'} ultrapassada (${pct.toFixed(0)}%).`,
      icone: 'pi pi-flag-fill',
    }
  }
  if (pct >= 80) {
    const restante = 100 - pct
    return {
      tipo: TIPOS.INFO,
      mensagem: `Faltam só ${restante.toFixed(0)}% pra bater a meta de ${meta.categoria_nome || 'geral'}.`,
      icone: 'pi pi-flag',
    }
  }
  return null
}

function gerarMensagemCategoriaDominante(categoria, totalGastos) {
  const pct = totalGastos > 0 ? (categoria.total / totalGastos) * 100 : 0
  if (pct < 30) return null
  return {
    tipo: TIPOS.INFO,
    mensagem: `${categoria.nome} representa ${pct.toFixed(0)}% dos teus gastos esse mês.`,
    icone: 'pi pi-chart-pie',
  }
}

function gerarMensagemReceitas(receitas, gastos) {
  if (receitas <= 0) return null
  const margem = receitas - gastos
  if (margem >= 0) {
    return {
      tipo: TIPOS.POSITIVE,
      mensagem: `Soberano! Sobrou ${formatarValor(margem)} esse mês.`,
      icone: 'pi pi-wallet',
    }
  }
  return {
    tipo: TIPOS.WARNING,
    mensagem: `Gastos passaram as receitas em ${formatarValor(Math.abs(margem))}. Revisa aí.`,
    icone: 'pi pi-exclamation-triangle',
  }
}

function gerarMensagemPendentes(qtd, totalPendente) {
  if (qtd === 0) return null
  if (qtd === 1) {
    return {
      tipo: TIPOS.INFO,
      mensagem: `Só falta pagar uma conta (${formatarValor(totalPendente)}).`,
      icone: 'pi pi-receipt',
    }
  }
  return {
    tipo: TIPOS.INFO,
    mensagem: `${qtd} contas pendentes somando ${formatarValor(totalPendente)}.`,
    icone: 'pi pi-receipt',
  }
}

function gerarMensagemPrevisao(previsao, diasRestantes) {
  if (!previsao || diasRestantes <= 3) return null
  return {
    tipo: TIPOS.INFO,
    mensagem: `Pelo ritmo atual, teus gastos devem fechar perto de ${formatarValor(previsao)}.`,
    icone: 'pi pi-chart-line',
  }
}

export function gerarInsights(dados) {
  if (!dados) return []

  const d = dados
  const insights = []

  const receitas = d.total_receitas || 0
  const gastos = d.total_gastos || 0
  const saldo = d.saldo || 0
  const variacao = d.variacao_percentual || 0
  const totalAPagar = d.total_a_pagar || 0
  const qtdPendentes = d.quantidade_pendentes || 0

  // 1. Tendência vs mês anterior
  const tendencia = gerarMensagensTendencia(variacao, d.gastos_mes_anterior)
  if (tendencia) insights.push(tendencia)

  // 2. Receitas vs gastos
  const receitasInsight = gerarMensagemReceitas(receitas, gastos)
  if (receitasInsight) insights.push(receitasInsight)

  // 3. Saldo e contas pendentes
  const saldoInsight = gerarMensagensSaldo(saldo, totalAPagar)
  if (saldoInsight) insights.push(saldoInsight)

  // 4. Pendentes
  const pendentesInsight = gerarMensagemPendentes(qtdPendentes, totalAPagar)
  if (pendentesInsight) insights.push(pendentesInsight)

  // 5. Meta mais próxima
  if (d.metas) {
    const metaGeral = d.metas.geral
    if (metaGeral) {
      const metaInsight = gerarMensagensMeta(metaGeral)
      if (metaInsight) insights.push(metaInsight)
    }
    const metaCritica = (d.metas.por_categoria || [])
      .filter(m => m.percentual_usado >= 80)
      .sort((a, b) => b.percentual_usado - a.percentual_usado)[0]
    if (metaCritica) {
      const catInsight = gerarMensagensMeta(metaCritica)
      if (catInsight && !insights.some(i => i.mensagem.includes(metaCritica.categoria_nome))) {
        insights.push(catInsight)
      }
    }
  }

  // 6. Categoria dominante
  const ranking = d.ranking_categorias
  if (ranking && ranking.length > 0) {
    const dom = gerarMensagemCategoriaDominante(ranking[0], gastos)
    if (dom) insights.push(dom)
  }

  // 7. Previsão ML
  const diasRestantes = Math.max(0, 30 - new Date().getDate())
  if (d.previsao_mes) {
    const previsao = gerarMensagemPrevisao(d.previsao_mes, diasRestantes)
    if (previsao) insights.push(previsao)
  }

  // Priorizar e limitar a 4 insights
  return insights
    .sort((a, b) => (PESOS[b.tipo] || 0) - (PESOS[a.tipo] || 0))
    .slice(0, 4)
}

export { TIPOS }
