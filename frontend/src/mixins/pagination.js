/**
 * Mixin reutilizável para paginação no Vue Options API.
 *
 * Uso:
 *   import { paginationMixin } from '../mixins/pagination.js'
 *   mixins: [paginationMixin],
 *   methods: {
 *     async carregarDados(page = 1) {
 *       const data = await fetchSomething(page, this.pagination.pageSize)
 *       this.applyPagination(data, 'items', 'total')
 *     }
 *   }
 */

export const paginationMixin = {
  data() {
    return {
      pagination: {
        page: 1,
        pages: 1,
        pageSize: 20,
        total: 0,
        next: null,
        previous: null,
      },
    }
  },

  methods: {
    /**
     * Aplica metadados de paginação a partir da resposta da API.
     * @param {Object} data - resposta da API
     * @param {string} itemsKey - chave dos itens na resposta (padrão: não usado diretamente)
     * @param {string} totalKey - chave do total na resposta (padrão: 'total')
     */
    applyPagination(data, totalKey = 'total') {
      this.pagination.page = data.page || 1
      this.pagination.pages = data.pages || 1
      this.pagination.total = data[totalKey] || 0
      this.pagination.next = data.next || null
      this.pagination.previous = data.previous || null
    },

    /**
     * Navega para uma página específica se válida.
     * @param {number} page
     * @param {Function} loader - método de carregamento async
     */
    goToPage(page, loader) {
      if (page >= 1 && page <= this.pagination.pages) {
        loader(page)
      }
    },
  },
}
