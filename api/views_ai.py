import json
import logging
import os
from datetime import date

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Gasto

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

CATEGORIAS_VALIDAS = [c[0] for c in Gasto.CATEGORIAS_CHOICES]
CATEGORIAS_LABELS = dict(Gasto.CATEGORIAS_CHOICES)

SYSTEM_PROMPT = """Voce e um assistente financeiro de um app chamado Sem Aperreio. Seu trabalho e interpretar mensagens em linguagem natural do usuario e extrair dados estruturados para registrar gastos ou receitas.

IMPORTANTE: Voce NAO salva nada. Voce apenas analisa e retorna JSON.

Categorias de gasto validas (use exatamente o valor do campo "slug"):
- moradia
- mercado
- restaurantes
- transporte
- saude
- educacao
- lazer
- contas
- compras
- outros

Regras:
1. Identifique se e gasto ou receita.
2. Extraia o valor numerico (convertendo textos como "5 mil" para 5000, "25 reais" para 25).
3. Classifique a categoria (use o slug listado acima).
4. A descricao deve ser o LUGAR, ESTABELECIMENTO ou ITEM do gasto. Nunca use verbos como "gastei", "paguei", "comprei" como descricao.
5. Se a descricao estiver apos uma preposicao (na, no, em, com, de), use a palavra apos a preposicao.
6. Se a mensagem nao fizer sentido como gasto ou receita, retorne intent: "unknown".

Se o usuario enviar apenas um numero (ex: "140", "25 reais", "5 mil"), ele provavelmente esta respondendo uma pergunta anterior sobre valor. Extraia o numero e retorne com os outros campos como null.

Se o usuario enviar apenas uma palavra (ex: "internet", "uber", "mercado"), extraia como descricao e tente inferir a categoria.

Exemplos de descricao:
- "gastei 25 reais de uber" -> descricao: "Uber" (nao "gastei")
- "paguei 150 no ifood" -> descricao: "iFood" (nao "paguei")
- "gastei 400 reais na feira" -> descricao: "Feira" (nao "gastei")
- "mercado 320" -> descricao: "Mercado"
- "recebi 5 mil hoje" -> descricao: "Receita"
- "dei 80 reais de gasolina" -> descricao: "Gasolina"
- "comprei remedio na farmacia, 45 reais" -> descricao: "Remedio"
- "paguei o aluguel, 1200 reais" -> descricao: "Aluguel"
- "140" -> valor: 140, descricao: null, categoria: null
- "internet" -> valor: null, descricao: "Internet", categoria: "contas"

Responda SEMPRE em JSON com este formato:
{
  "intent": "add_expense" | "add_income" | "unknown",
  "valor": 0.0 | null,
  "categoria": "slug_da_categoria" | null,
  "descricao": "string" | null
}
"""


def _call_openai(message: str):
    """Chama a API da OpenAI para interpretar a mensagem. Retorna dict ou None."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY nao configurada")
        return None

    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.0,
            max_tokens=256,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"Erro na chamada OpenAI: {e}")
        return None


def _extract_description(message, msg_lower, categoria, categoria_map):
    """Extrai a descricao do gasto usando heurísticas de linguagem natural."""
    import re

    # 1. Procurar palavras após preposições (na, no, em, com, de, do, da, para, pra)
    prep_pattern = r'(?:na|no|em|com|de|do|da|para|pra|d[a-o]\s+)\s+([a-zA-Zà-úç]+(?:\s+[a-zA-Zà-úç]+)?)'
    prep_match = re.search(prep_pattern, msg_lower)
    if prep_match:
        desc = prep_match.group(1).strip()
        # Verificar se não é uma stop word
        stop_words = {'reais', 'real', 'mil', 'vezes', 'dia', 'mês', 'ano', 'semana'}
        if desc not in stop_words and len(desc) > 1:
            # Capitalizar
            return ' '.join(w.capitalize() for w in desc.split())

    # 2. Usar a keyword que acionou a categoria como descrição
    keywords = categoria_map.get(categoria, [])
    for kw in keywords:
        if kw in msg_lower:
            # Pegar a palavra exatamente como aparece na mensagem original
            idx = msg_lower.find(kw)
            if idx >= 0:
                # Extrair da mensagem original mantendo case
                original = message[idx:idx + len(kw)]
                return original.capitalize()

    # 3. Ignorar verbos iniciais e pegar substantivo antes do número
    verbos_iniciais = {'gastei', 'paguei', 'dei', 'comprei', 'fiz', 'tive',
                        'gasto', 'pago', 'dou', 'compro', 'uso', 'peguei',
                        'gastei', 'gastos', 'paguei', 'pago', 'gasto'}
    words = message.strip().split()
    for i, w in enumerate(words):
        # Encontrar posição do número na mensagem
        clean = w.replace('.', '').replace(',', '').replace('R$', '').replace('r$', '')
        if clean.isdigit():
            # Procurar para trás o primeiro substantivo não-verbo
            for j in range(i - 1, -1, -1):
                candidate = words[j].replace(',', '').replace('.', '').lower()
                if candidate not in verbos_iniciais and len(candidate) > 1:
                    # Capitalizar
                    return ' '.join(wd.capitalize() for wd in words[j:i]).strip()
            break

    # 4. Fallback: categoria capitalizada
    return categoria.capitalize()


# Categoria map global para reutilização
CATEGORIA_MAP = {
    'moradia': ['aluguel', 'condominio', 'iptu', 'moradia'],
    'mercado': ['mercado', 'supermercado', 'feira', 'açougue'],
    'restaurantes': ['restaurante', 'ifood', 'uber eats', 'mcdonalds', 'burger', 'pizza', 'lanche'],
    'transporte': ['uber', '99', 'taxi', 'onibus', 'metro', 'combustivel', 'gasolina', 'estacionamento', 'transporte'],
    'saude': ['remedio', 'farmacia', 'hospital', 'consulta', 'dentista', 'saude'],
    'educacao': ['curso', 'escola', 'faculdade', 'livro', 'educacao'],
    'lazer': ['cinema', 'bar', 'show', 'jogo', 'netflix', 'spotify', 'lazer'],
    'contas': ['luz', 'agua', 'internet', 'telefone', 'gas', 'conta'],
    'compras': ['shopping', 'loja', 'roupa', 'tenis', 'compra'],
    'outros': []
}


def _detect_category_from_text(msg_lower: str):
    """Detecta categoria a partir de palavras-chave no texto."""
    for cat, keywords in CATEGORIA_MAP.items():
        if any(k in msg_lower for k in keywords):
            return cat
    return 'outros'


def _extract_value(message: str):
    """Extrai valor numerico de uma mensagem curta (resposta a pergunta)."""
    import re
    msg_lower = message.lower().strip()

    patterns = [
        r'(?:(?:r\$)?\s?)([\d.]+(?:,\d+)?)(?:\s?(?:mil|k|reais|real|r\$))?',
        r'(\d+(?:\.\d{3})*(?:,\d+)?)\s?(?:mil|k|reais|real)',
        r'(\d+(?:,\d+)?)',
    ]
    for pat in patterns:
        match = re.search(pat, msg_lower)
        if match:
            raw = match.group(1).replace('.', '').replace(',', '.')
            try:
                v = float(raw)
                if 'mil' in msg_lower or 'k ' in msg_lower or msg_lower.endswith('k'):
                    v *= 1000
                return round(v, 2)
            except ValueError:
                continue
    return None


def _check_completeness(parsed: dict, original_message: str):
    """Verifica se os dados estão completos. Se faltar valor, marca como incompleto."""
    intent = parsed.get('intent')
    valor = parsed.get('valor')
    categoria = parsed.get('categoria')
    descricao = parsed.get('descricao')

    # Se não tem intent valido ou não conseguiu nenhum dado
    if intent == 'unknown':
        return parsed

    # Se tem valor, consideramos completo (categoria e descricao tem fallback)
    if valor and valor > 0:
        return parsed

    # Falta valor - verificar se pelo menos temos descricao ou categoria
    if not descricao and not categoria:
        # Nem valor nem descricao - tentar extrair descricao da mensagem
        msg_lower = original_message.lower().strip()
        # Remover verbos comuns
        verbos = {'gastei', 'paguei', 'comprei', 'dei', 'fiz', 'tive', 'gasto', 'pago'}
        words = [w for w in msg_lower.split() if w not in verbos and not w.replace('.', '').replace(',', '').isdigit()]
        if words:
            parsed['descricao'] = ' '.join(words).capitalize()
            parsed['categoria'] = _detect_category_from_text(msg_lower)

    # Se tem descricao mas nao tem valor, ainda esta incompleto
    if not valor or valor <= 0:
        # Marcar como incompleto - precisa perguntar valor
        pass

    return parsed


def _is_continuation(message: str):
    """Detecta se mensagem é continuação de assunto ('e mercado 120', 'também', 'sim')."""
    msg_lower = message.lower().strip()
    continuation_markers = ['e ', 'tambem', 'também', 'tbm ', 'tb ', 'mais ', 'outro ', 'outra ', 'sim', 'confirmo', 'pode ', 'beleza', 'ok', 'blz']
    return any(msg_lower.startswith(m) or msg_lower == m.strip() for m in continuation_markers)


def _is_greeting(message: str):
    """Detecta saudações e cumprimentos."""
    msg_lower = message.lower().strip()
    greetings = ['oi', 'olá', 'ola', 'opa', 'e aí', 'e ai', 'eae', 'hey',
                 'hello', 'hi', 'bom dia', 'boa tarde', 'boa noite',
                 'beleza', 'tudo bem', 'tudo bem?', 'como vai', 'eai',
                 'salve', 'fala', 'fala ai', 'fala aí', 'tchau', 'xau',
                 'até mais', 'ate mais', 'falou', 'flw', 'valeu', 'obrigado',
                 'obrigada', 'blz', 'tranquilo', 'suave', 'de boa', 'deboa',
                 'show', 'massa', 'top', 'legal', 'nice', 'perfeito',
                 'maravilha', 'excelente', 'ótimo', 'otimo', 'bom', 'bom demais']
    return msg_lower in greetings or any(msg_lower.startswith(g + ' ') for g in greetings if len(g) > 3)


def _is_conversation_end(message: str):
    """Detecta se mensagem encerra a conversa (não, obrigado, tchau, valeu)."""
    msg_lower = message.lower().strip()
    # Recusas
    negative = ['não', 'nao', 'nope', 'n', 'cancela', 'cancelar', 'sair',
                'fechar', 'nada', 'passo', 'esquece', 'deixa', 'n quero',
                'nao quero', 'não quero', 'já deu', 'chega', 'pare',
                'n preciso', 'nao preciso', 'não preciso',
                'nenhum', 'nenhum gasto', 'nenhuma']
    # Gratidão
    thanks = ['obrigado', 'obrigada', 'valeu', 'thanks', 'thank you',
              'grato', 'grata', 'agradeço', 'agradeco', 'flw', 'falou',
              'show', 'massa', 'top', 'legal']
    # Despedida
    goodbye = ['tchau', 'xau', 'até', 'ate', 'bye', 'cya', 'até logo',
               'ate logo', 'até mais', 'ate mais', 'fui', 'té']
    all_markers = negative + thanks + goodbye
    return msg_lower in all_markers or any(msg_lower.startswith(m + ' ') for m in all_markers)


def _detect_continuation_intent(message: str, history: list):
    """Infere o intent da mensagem de continuação baseado no histórico."""
    if not history:
        return None

    # Pegar últimas mensagens do usuário do histórico
    last_user_msgs = [h for h in history if h.get('role') == 'user']
    if not last_user_msgs:
        return None

    # Pegar última mensagem do usuário que tinha conteúdo
    last_user_msg = last_user_msgs[-1].get('content', '')
    last_lower = last_user_msg.lower()

    # Se a última mensagem tinha receita, provavelmente continua receita
    receita_keywords = ['recebi', 'receita', 'ganhei', 'salario', 'entrada']
    if any(k in last_lower for k in receita_keywords):
        return 'add_income'

    return 'add_expense'


def _process_contextual(message: str, context: dict):
    """Processa resposta do usuario quando ha contexto pendente."""
    awaiting_field = context.get('awaiting_field')
    partial = context.get('partial_data', {})
    msg_lower = message.lower().strip()

    result = dict(partial)
    result.setdefault('intent', 'add_expense')
    result.setdefault('descricao', '')
    result.setdefault('categoria', 'outros')

    if awaiting_field == 'valor':
        valor = _extract_value(message)
        if valor and valor > 0:
            result['valor'] = valor
        else:
            return None

    elif awaiting_field == 'categoria':
        cat = _detect_category_from_text(msg_lower)
        result['categoria'] = cat

    elif awaiting_field == 'descricao':
        result['descricao'] = message.strip().capitalize()

    # Se nao tinha awaiting_field especifico, tentar extrair o que falta
    elif not result.get('valor'):
        valor = _extract_value(message)
        if valor:
            result['valor'] = valor
        else:
            return None

    return result


def _fallback_parser(message: str, conversation_history: list = None):
    """Parser simples de fallback quando OpenAI falha ou nao esta configurada.
    Detecta continuidade de assunto baseado no conversation_history.
    """
    import re
    msg_lower = message.lower().strip()

    # Detectar tipo
    palavras_receita = ['recebi', 'receita', 'ganhei', 'salario', 'pagaram', 'entrada']
    is_receita = any(p in msg_lower for p in palavras_receita)

    # Se mensagem é continuação e temos histórico, manter o intent do histórico
    if _is_continuation(message) and conversation_history:
        inferred_intent = _detect_continuation_intent(message, conversation_history)
        if inferred_intent:
            intent = inferred_intent
            # Remover marcadores de continuidade do início da mensagem
            for marker in ['e ', 'tambem ', 'também ', 'tbm ', 'tb ', 'mais ', 'outro ', 'outra ', 'sim', 'confirmo', 'pode ', 'beleza', 'ok', 'blz']:
                if msg_lower.startswith(marker):
                    msg_lower = msg_lower[len(marker):].strip()
                    break
        else:
            intent = 'add_income' if is_receita else 'add_expense'
    else:
        intent = 'add_income' if is_receita else 'add_expense'

    # Extrair valor numerico
    # Procura padroes como 5 mil, 5000, 1.200,50, 25 reais, R$ 50
    patterns = [
        r'(?:(?:r\$)?\s?)([\d.]+(?:,\d+)?)(?:\s?(?:mil|k|reais|real|r\$))?',
        r'(\d+(?:\.\d{3})*(?:,\d+)?)\s?(?:mil|k|reais|real)',
    ]
    valor = None
    for pat in patterns:
        match = re.search(pat, msg_lower)
        if match:
            raw = match.group(1).replace('.', '').replace(',', '.')
            try:
                v = float(raw)
                # Multiplicador "mil" ou "k"
                if 'mil' in msg_lower or 'k ' in msg_lower or msg_lower.endswith('k'):
                    v *= 1000
                valor = round(v, 2)
                break
            except ValueError:
                continue

    if not valor:
        return None

    # Categoria
    categoria = _detect_category_from_text(msg_lower)

    # Extrair descricao inteligente
    descricao = _extract_description(message, msg_lower, categoria, CATEGORIA_MAP)
    descricao = descricao[:60] or (CATEGORIAS_LABELS.get(categoria, 'Gasto'))

    return {
        'intent': intent,
        'valor': valor,
        'categoria': None if intent == 'add_income' else categoria,
        'descricao': descricao
    }


def _build_confirmation_response(parsed: dict, message: str):
    """Monta a resposta de confirmacao para o frontend."""
    intent = parsed.get('intent', 'unknown')
    valor = parsed.get('valor')
    categoria = parsed.get('categoria')
    descricao = parsed.get('descricao', '')

    if intent == 'unknown' or valor is None or valor <= 0:
        return {
            'intent': 'unknown',
            'confirmation_required': False,
            'message': 'Nao entendi. Tente algo como "mercado 150" ou "recebi 3000".',
            'data': None
        }

    valor_fmt = f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    if intent == 'add_expense':
        cat_label = CATEGORIAS_LABELS.get(categoria, categoria) if categoria else 'Outros'
        desc_extra = f' ({descricao})' if descricao and descricao.lower() != cat_label.lower() else ''
        msg = f'Perfeito! Adicionar gasto de {valor_fmt} em {cat_label}{desc_extra}?'
        return {
            'intent': 'add_expense',
            'confirmation_required': True,
            'message': msg,
            'data': {
                'valor': valor,
                'categoria': categoria,
                'descricao': descricao,
                'data': date.today().isoformat()
            }
        }

    if intent == 'add_income':
        desc_extra = f' ({descricao})' if descricao else ''
        msg = f'Perfeito! Adicionar receita de {valor_fmt}{desc_extra}?'
        return {
            'intent': 'add_income',
            'confirmation_required': True,
            'message': msg,
            'data': {
                'valor': valor,
                'descricao': descricao,
                'data': date.today().isoformat()
            }
        }

    return {
        'intent': 'unknown',
        'confirmation_required': False,
        'message': 'Nao entendi. Tente algo como "mercado 150" ou "recebi 3000".',
        'data': None
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chat(request):
    """
    POST /api/ai/chat/
    Body: {"message": "uber 25 reais", "context": {...}, "conversation_history": []}
    Responde com interpretacao + pedido de confirmacao OU pergunta complementar.
    NAO salva nada no banco.
    """
    try:
        message = request.data.get('message', '').strip()
        context = request.data.get('context', {})
        conversation_history = request.data.get('conversation_history', [])

        if not message:
            return Response(
                {'erro': 'Mensagem vazia'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Detectar saudações
        if _is_greeting(message):
            return Response({
                'intent': 'unknown',
                'confirmation_required': False,
                'awaiting_field': None,
                'partial_data': {},
                'message': 'Oi! Como posso ajudar? Me diga um gasto ou receita que eu registro pra voc\u00ea \U0001f44b',
                'data': None
            })

        # Detectar fim de conversa (não, obrigado, tchau, valeu)
        if _is_conversation_end(message):
            return Response({
                'intent': 'unknown',
                'confirmation_required': False,
                'awaiting_field': None,
                'partial_data': {},
                'message': '\U0001f44b',
                'data': None
            })

        # Se ha contexto pendente, processar resposta complementar
        if context.get('awaiting_field') or context.get('partial_data'):
            parsed = _process_contextual(message, context)
            if not parsed:
                return Response({
                    'intent': 'unknown',
                    'confirmation_required': False,
                    'awaiting_field': context.get('awaiting_field'),
                    'partial_data': context.get('partial_data'),
                    'message': 'Não entendi direito. Pode repetir?',
                    'data': None
                })
        else:
            # Primeira mensagem - tentar OpenAI primeiro
            parsed = _call_openai(message)

            # Fallback se OpenAI falhar ou nao estiver configurada
            if not parsed:
                parsed = _fallback_parser(message, conversation_history)

            # Fallback para mensagens sem valor (ex: "paguei internet")
            if not parsed:
                msg_lower = message.lower().strip()
                cat = _detect_category_from_text(msg_lower)
                desc = _extract_description(message, msg_lower, cat, CATEGORIA_MAP)
                desc = desc[:60] or CATEGORIAS_LABELS.get(cat, 'Gasto')

                # Se pelo menos temos descricao ou categoria
                if desc and desc.lower() not in ('gastei', 'paguei', 'comprei', 'dei'):
                    # Se é continuação, manter intent do histórico
                    if _is_continuation(message) and conversation_history:
                        intent = _detect_continuation_intent(message, conversation_history) or 'add_expense'
                    else:
                        intent = 'add_income' if any(p in msg_lower for p in ['recebi', 'receita', 'ganhei', 'salario', 'pagaram', 'entrada']) else 'add_expense'
                    parsed = {
                        'intent': intent,
                        'valor': None,
                        'categoria': None if intent == 'add_income' else cat,
                        'descricao': desc
                    }
                else:
                    return Response(
                        {
                            'intent': 'unknown',
                            'confirmation_required': False,
                            'message': 'Hmm, não consegui entender. Que tal "mercado 150" ou "recebi 3000"?',
                            'data': None
                        }
                    )

        # Validar categoria se for gasto
        if parsed.get('intent') == 'add_expense' and parsed.get('categoria'):
            if parsed['categoria'] not in CATEGORIAS_VALIDAS:
                parsed['categoria'] = 'outros'

        # Verificar completude: falta valor?
        valor = parsed.get('valor')
        if not valor or valor <= 0:
            # Ainda falta valor - perguntar de forma natural
            descricao = parsed.get('descricao', '')
            categoria = parsed.get('categoria', 'outros')
            cat_label = CATEGORIAS_LABELS.get(categoria, categoria)

            # Montar pergunta contextual
            item = descricao or cat_label
            intent = parsed.get('intent', 'add_expense')
            if intent == 'add_income':
                question = f'Qual foi o valor recebido?'
            else:
                if item != 'Outros':
                    question = f'Quanto você gastou com {item}?'
                else:
                    question = 'Qual foi o valor?'

            return Response({
                'intent': intent,
                'confirmation_required': False,
                'awaiting_field': 'valor',
                'partial_data': {
                    'intent': intent,
                    'categoria': categoria if intent == 'add_expense' else None,
                    'descricao': descricao
                },
                'message': question,
                'data': None
            })

        # Dados completos - montar confirmacao
        response_data = _build_confirmation_response(parsed, message)
        response_data['awaiting_field'] = None
        response_data['partial_data'] = None
        return Response(response_data)

    except Exception as e:
        logger.error(f'Erro no AI chat: {e}')
        return Response(
            {'erro': 'Erro interno no servidor'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
