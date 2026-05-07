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

Exemplos de descricao:
- "gastei 25 reais de uber" -> descricao: "Uber" (nao "gastei")
- "paguei 150 no ifood" -> descricao: "iFood" (nao "paguei")
- "gastei 400 reais na feira" -> descricao: "Feira" (nao "gastei")
- "mercado 320" -> descricao: "Mercado"
- "recebi 5 mil hoje" -> descricao: "Receita"
- "dei 80 reais de gasolina" -> descricao: "Gasolina"
- "comprei remedio na farmacia, 45 reais" -> descricao: "Remedio"
- "paguei o aluguel, 1200 reais" -> descricao: "Aluguel"

Responda SEMPRE em JSON com este formato:
{
  "intent": "add_expense" | "add_income" | "unknown",
  "valor": 0.0,
  "categoria": "slug_da_categoria" | null,
  "descricao": "string"
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


def _fallback_parser(message: str):
    """Parser simples de fallback quando OpenAI falha ou nao esta configurada."""
    import re
    msg_lower = message.lower().strip()

    # Detectar tipo
    palavras_receita = ['recebi', 'receita', 'ganhei', 'salario', 'pagaram', 'entrada']
    is_receita = any(p in msg_lower for p in palavras_receita)
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
    categoria_map = {
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
    categoria = 'outros'
    for cat, keywords in categoria_map.items():
        if any(k in msg_lower for k in keywords):
            categoria = cat
            break

    # Extrair descricao inteligente
    descricao = _extract_description(message, msg_lower, categoria, categoria_map)
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
        msg = f'Entendi! Você gastou {valor_fmt} em {cat_label}{desc_extra}.'
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
        msg = f'Entendi! Você recebeu {valor_fmt}{desc_extra}.'
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
    Body: {"message": "uber 25 reais"}
    Responde com interpretacao + pedido de confirmacao.
    NAO salva nada no banco.
    """
    try:
        message = request.data.get('message', '').strip()
        if not message:
            return Response(
                {'erro': 'Mensagem vazia'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tentar OpenAI primeiro
        parsed = _call_openai(message)

        # Fallback se OpenAI falhar ou nao estiver configurada
        if not parsed:
            parsed = _fallback_parser(message)

        if not parsed:
            return Response(
                {
                    'intent': 'unknown',
                    'confirmation_required': False,
                    'message': 'Nao consegui entender. Tente algo como "mercado 150" ou "recebi 3000".',
                    'data': None
                }
            )

        # Validar categoria se for gasto
        if parsed.get('intent') == 'add_expense' and parsed.get('categoria'):
            if parsed['categoria'] not in CATEGORIAS_VALIDAS:
                parsed['categoria'] = 'outros'

        response_data = _build_confirmation_response(parsed, message)
        return Response(response_data)

    except Exception as e:
        logger.error(f'Erro no AI chat: {e}')
        return Response(
            {'erro': 'Erro interno no servidor'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
