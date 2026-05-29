import { ref } from 'vue'

/**
 * Composable para paginação em componentes <script setup>.
 *
 * Uso:
 *   const { pagination, applyPagination, goToPage } = usePagination()
 *   const data = await fetchSomething(page, pagination.value.pageSize)
 *   applyPagination(data)
 *   goToPage(2, carregarDados)
 */
export function usePagination(defaultPageSize = 20) {
  const pagination = ref({
    page: 1,
    pages: 1,
    pageSize: defaultPageSize,
    total: 0,
    next: null,
    previous: null,
  })

  function applyPagination(data, totalKey = 'total') {
    pagination.value.page = data.page || 1
    pagination.value.pages = data.pages || 1
    pagination.value.total = data[totalKey] || 0
    pagination.value.next = data.next || null
    pagination.value.previous = data.previous || null
  }

  function goToPage(page, loader) {
    if (page >= 1 && page <= pagination.value.pages) {
      loader(page)
    }
  }

  return {
    pagination,
    applyPagination,
    goToPage,
  }
}
