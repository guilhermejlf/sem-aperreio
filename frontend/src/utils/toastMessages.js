export const toastTitles = {
  success: 'Sucesso',
  error: 'Erro',
  warning: 'Atenção',
  info: 'Info',
}

export const toastMessages = {
  expense: {
    created: 'Despesa salva 😄',
    updated: 'Despesa atualizada.',
    deleted: 'Despesa removida.',
    saveError: 'Vixe 😅 Não consegui salvar agora.',
    deleteError: 'Vixe 😅 Não consegui excluir agora.',
  },
  revenue: {
    created: 'Receita adicionada 😄',
    updated: 'Receita atualizada.',
    deleted: 'Receita removida.',
    saveError: 'Vixe 😅 Não consegui salvar agora.',
    deleteError: 'Vixe 😅 Não consegui excluir agora.',
  },
  goals: {
    created: 'Meta criada com sucesso.',
    updated: 'Meta atualizada.',
    deleted: 'Meta removida.',
    saveError: 'Vixe 😅 Não consegui salvar agora.',
    deleteError: 'Não consegui concluir essa ação.',
  },
  family: {
    created: 'Grupo criado 😄',
    joined: 'Você entrou no grupo!',
    left: 'Você saiu do grupo.',
    memberRemoved: 'Membro removido.',
    groupDeleted: 'Grupo removido.',
    codeCopied: 'Código copiado.',
    codeRegenerated: 'Novo código gerado.',
    nameRequired: 'Dá um nome pro grupo 😄',
    codeLength: 'O código precisa ter 6 caracteres.',
    saveError: 'Vixe 😅 Não consegui concluir.',
  },
  export: {
    downloaded: (formato) => `Arquivo ${formato.toUpperCase()} baixado.`,
    loadError: 'Não consegui carregar o extrato.',
    exportError: 'Não consegui exportar agora.',
  },
  generic: {
    networkError: 'Não consegui conectar agora.',
    deleteError: 'Não consegui concluir essa ação.',
    actionError: 'Vixe 😅 Algo deu errado.',
    loadError: 'Não consegui carregar isso agora.',
  },
}
