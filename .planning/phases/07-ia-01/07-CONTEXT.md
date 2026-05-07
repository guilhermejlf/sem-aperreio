# Phase 7 — IA-01 Context

## Decisões Capturadas

### Arquitetura
- **Parser estruturado, não chatbot**: A IA funciona como extrator de entidades (tipo, valor, categoria, descrição) a partir de linguagem natural. Não há conversação contínua.
- **Sem salvamento automático**: O backend NUNCA salva no banco. Apenas retorna uma estrutura padronizada para confirmação no frontend.
- **Reutilização de endpoints**: Após confirmação do usuário, o frontend chama os endpoints existentes (`/api/gastos/` ou `/api/receitas/`). Zero duplicação de lógica.
- **Fallback local**: Se a OpenAI não estiver configurada ou falhar, um parser regex simples assume. Isso garante que o sistema funcione mesmo sem API key.

### OpenAI
- Modelo: `gpt-4o-mini` (econômico, suficiente para NER simples)
- Temperatura: 0.0 (determinístico)
- Response format: `json_object`
- System prompt contém categorias válidas, exemplos, e regras de extração

### UX
- Drawer lateral com animação slide
- FAB flutuante no canto inferior direito (gradiente roxo/verde)
- Bolhas de mensagem estilo chat (verde para usuário, escuro para IA)
- Card de confirmação com dados estruturados e botões Confirmar/Cancelar
- Mobile: drawer ocupa 100% da largura

### Categorias
Reutiliza as categorias existentes do model `Gasto`:
moradia, mercado, restaurantes, transporte, saude, educacao, lazer, contas, compras, outros

### Fora de escopo (deliberado)
- OCR / PDF / visão
- Embeddings / memória longa
- LangChain / RAG / agentes
- Chat contínuo com contexto
