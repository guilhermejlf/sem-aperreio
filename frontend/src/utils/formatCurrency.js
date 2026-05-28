/**
 * Formata um valor numérico para moeda BRL.
 * @param {number|string} valor
 * @returns {string}
 */
export function formatarValor(valor) {
  return parseFloat(valor || 0).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}
