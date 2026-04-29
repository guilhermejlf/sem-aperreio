import pickle
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import os
import logging
from calendar import monthrange

from django.db import models
from django.db.models import Q, Sum, Count, Max
from django.db.models.functions import Coalesce
from decimal import Decimal
from .models import Gasto, FamilyMembership, Receita
from .serializers import GastoSerializer, ReceitaSerializer
from .permissions import GastoPermission

logger = logging.getLogger(__name__)

# -------------------------
# MODELO IA (Lazy Loading)
# -------------------------
_modelo_ia = None

def get_modelo_ia():
    global _modelo_ia
    if _modelo_ia is None:
        try:
            caminho_modelo = os.path.join(os.path.dirname(__file__), "modelo.pkl")
            with open(caminho_modelo, "rb") as f:
                _modelo_ia = pickle.load(f)
            logger.info("Modelo IA carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo IA: {e}")
            _modelo_ia = None
    return _modelo_ia

# -------------------------
# IA - PREVISÃO
# -------------------------
@api_view(["POST"])
def prever_gasto(request):
    try:
        mes = request.data.get("mes")
        
        # Validação do mês
        if mes is None:
            return Response(
                {"erro": "Informe o mês (1-12)", "campo": "mes"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            mes_int = int(mes)
            if mes_int < 1 or mes_int > 12:
                return Response(
                    {"erro": "Mês deve estar entre 1 e 12", "campo": "mes"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"erro": "Mês deve ser um número válido", "campo": "mes"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Carregar modelo e fazer previsão
        modelo = get_modelo_ia()
        if modelo is None:
            return Response(
                {"erro": "Serviço de previsão indisponível no momento"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        entrada = pd.DataFrame({"mes": [mes_int]})
        previsao = modelo.predict(entrada)
        
        # Limitar previsão a valores razoáveis
        previsao_valor = max(0, min(float(previsao[0]), 100000))

        return Response({
            "mes": mes_int,
            "previsao": round(previsao_valor, 2),
            "moeda": "BRL"
        })

    except Exception as e:
        logger.error(f"Erro na previsão: {e}")
        return Response(
            {"erro": "Erro interno no servidor"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# -------------------------
# GASTOS CRUD
# -------------------------
def get_user_family(user):
    """Get the family of the current user, or None."""
    try:
        return user.membership.family
    except AttributeError:
        return None

def get_user_membership(user):
    """Get the family membership of the current user, or None."""
    try:
        return user.membership
    except AttributeError:
        return None

def get_user_gastos_queryset(user):
    """Get gastos queryset for user with effective date (data_competencia fallback to data)."""
    user_family = get_user_family(user)
    if user_family:
        queryset = Gasto.objects.filter(
            Q(family=user_family) | Q(user=user, family__isnull=True)
        )
    else:
        queryset = Gasto.objects.filter(user=user)

    return queryset.annotate(
        data_efetiva=Coalesce('data_competencia', 'data')
    )

@api_view(['GET', 'POST'])
def gastos(request):
    try:
        if request.method == 'GET':
            queryset = get_user_gastos_queryset(request.user)

            # Filtro por categoria
            categoria = request.query_params.get('categoria')
            if categoria:
                queryset = queryset.filter(categoria=categoria)

            # Filtro por período (data efetiva = data_competencia com fallback para data)
            data_inicio = request.query_params.get('data_inicio')
            data_fim = request.query_params.get('data_fim')
            if data_inicio:
                queryset = queryset.filter(data_efetiva__gte=data_inicio)
            if data_fim:
                queryset = queryset.filter(data_efetiva__lte=data_fim)

            # Filtro por data de competência explícita
            competencia_inicio = request.query_params.get('competencia_inicio')
            competencia_fim = request.query_params.get('competencia_fim')
            if competencia_inicio:
                queryset = queryset.filter(data_competencia__gte=competencia_inicio)
            if competencia_fim:
                queryset = queryset.filter(data_competencia__lte=competencia_fim)

            # Filtro por data de pagamento
            pagamento_inicio = request.query_params.get('pagamento_inicio')
            pagamento_fim = request.query_params.get('pagamento_fim')
            if pagamento_inicio:
                queryset = queryset.filter(data_pagamento__gte=pagamento_inicio)
            if pagamento_fim:
                queryset = queryset.filter(data_pagamento__lte=pagamento_fim)

            # Filtro por status pago
            pago = request.query_params.get('pago')
            if pago is not None:
                queryset = queryset.filter(pago=pago.lower() in ('true', '1', 'yes', 'sim'))

            # Ordenação e limite (por data efetiva)
            queryset = queryset.order_by('-data_efetiva', '-criado_em')

            # Paginação simples
            limite = int(request.query_params.get('limite', 50))
            if limite > 100:
                limite = 100
            queryset = queryset[:limite]

            serializer = GastoSerializer(queryset, many=True)
            return Response({
                "gastos": serializer.data,
                "total": len(serializer.data)
            })

        elif request.method == 'POST':
            dados = request.data.copy()
            # Se data_competencia não informado, copiar de data
            if not dados.get('data_competencia') and dados.get('data'):
                dados['data_competencia'] = dados['data']
            # Se pago não informado, setar como False
            if 'pago' not in dados:
                dados['pago'] = False

            serializer = GastoSerializer(data=dados)

            if serializer.is_valid():
                family = get_user_family(request.user)
                gasto = serializer.save(user=request.user, family=family)
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            
            # Formatar erros de validação
            errors = {}
            for field, messages in serializer.errors.items():
                errors[field] = messages[0] if isinstance(messages, list) else str(messages)
            
            return Response(
                {"erro": "Dados inválidos", "detalhes": errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"Erro na API de gastos: {e}")
        return Response(
            {"erro": "Erro interno no servidor"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'PUT', 'DELETE'])
def gasto_detail(request, pk):
    try:
        gasto = Gasto.objects.get(pk=pk)
    except Gasto.DoesNotExist:
        return Response(
            {"erro": "Gasto não encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # Check permission
    permission = GastoPermission()
    if not permission.has_object_permission(request, None, gasto):
        return Response(
            {"erro": "Você não tem permissão para acessar este gasto."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        if request.method == 'GET':
            serializer = GastoSerializer(gasto)
            return Response(serializer.data)

        elif request.method == 'PUT':
            dados = request.data.copy()
            # Se data_competencia não informado, manter o existente ou copiar de data
            if not dados.get('data_competencia'):
                if dados.get('data'):
                    dados['data_competencia'] = dados['data']
                else:
                    dados['data_competencia'] = gasto.data_competencia or gasto.data

            serializer = GastoSerializer(gasto, data=dados)
            if serializer.is_valid():
                # Verificar permissão para editar
                if gasto.user != request.user:
                    user_membership = get_user_membership(request.user)
                    if not user_membership or user_membership.role != 'admin':
                        return Response(
                            {"erro": "Você não tem permissão para editar este gasto."},
                            status=status.HTTP_403_FORBIDDEN
                        )

                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"erro": "Dados inválidos", "detalhes": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif request.method == 'DELETE':
            # Same permission logic as PUT
            if gasto.user != request.user:
                user_membership = get_user_membership(request.user)
                if not user_membership or user_membership.role != 'admin':
                    return Response(
                        {"erro": "Você não tem permissão para excluir este gasto."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            gasto.delete()
            return Response(
                {"mensagem": "Gasto excluído com sucesso"}, 
                status=status.HTTP_204_NO_CONTENT
            )

    except Exception as e:
        logger.error(f"Erro no detalhe do gasto: {e}")
        return Response(
            {"erro": "Erro interno no servidor"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# -------------------------
# DASHBOARD
# -------------------------
MES_NOMES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

@api_view(['GET'])
def dashboard(request):
    try:
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')

        if mes is None or ano is None:
            return Response(
                {"erro": "Informe os parâmetros 'mes' (1-12) e 'ano' (YYYY)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            mes_int = int(mes)
            ano_int = int(ano)
            if mes_int < 1 or mes_int > 12:
                return Response(
                    {"erro": "Mês deve estar entre 1 e 12"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"erro": "Mês e ano devem ser números válidos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Base queryset com filtro de family/user + data efetiva anotada
        base_queryset = get_user_gastos_queryset(request.user)

        # Período atual (por data efetiva = data_competencia com fallback para data)
        queryset_atual = base_queryset.filter(data_efetiva__month=mes_int, data_efetiva__year=ano_int)

        # Período anterior
        if mes_int == 1:
            mes_ant, ano_ant = 12, ano_int - 1
        else:
            mes_ant, ano_ant = mes_int - 1, ano_int
        queryset_anterior = base_queryset.filter(data_efetiva__month=mes_ant, data_efetiva__year=ano_ant)

        # Agregações do período atual
        agg_atual = queryset_atual.aggregate(
            total=Sum('valor'),
            quantidade=Count('id'),
            maior=Max('valor')
        )

        # Agregações do período anterior
        agg_anterior = queryset_anterior.aggregate(
            total=Sum('valor')
        )

        total_mes = agg_atual['total'] or Decimal('0.00')
        total_anterior = agg_anterior['total'] or Decimal('0.00')

        # Base queryset de receitas (mesmo filtro family/user)
        user_family = get_user_family(request.user)
        if user_family:
            receitas_queryset = Receita.objects.filter(
                Q(family=user_family) | Q(user=request.user, family__isnull=True)
            )
        else:
            receitas_queryset = Receita.objects.filter(user=request.user)

        # Total de receitas no período (por data)
        receitas_agg = receitas_queryset.filter(
            data__month=mes_int, data__year=ano_int
        ).aggregate(total=Sum('valor'))
        total_receitas = receitas_agg['total'] or Decimal('0.00')

        # Total de gastos pagos no período (por data_pagamento)
        gastos_pagos_agg = base_queryset.filter(
            data_pagamento__month=mes_int,
            data_pagamento__year=ano_int,
            pago=True
        ).aggregate(total=Sum('valor'))
        total_gastos_pagos = gastos_pagos_agg['total'] or Decimal('0.00')

        # Saldo
        saldo = total_receitas - total_gastos_pagos

        # Variacao
        if total_anterior > 0:
            variacao_absoluta = total_mes - total_anterior
            variacao_percentual = (variacao_absoluta / total_anterior) * 100
        else:
            variacao_absoluta = Decimal('0.00')
            variacao_percentual = Decimal('0.00')

        # Maior gasto
        maior_gasto_obj = queryset_atual.order_by('-valor').first()
        maior_gasto = None
        if maior_gasto_obj:
            maior_gasto = {
                "valor": float(maior_gasto_obj.valor),
                "categoria": maior_gasto_obj.get_categoria_display(),
                "descricao": maior_gasto_obj.descricao or ""
            }

        # Ranking de categorias (apenas com gastos)
        ranking = (
            queryset_atual
            .values('categoria')
            .annotate(
                total=Sum('valor'),
                quantidade=Count('id')
            )
            .filter(total__gt=0)
            .order_by('-total')
        )

        total_categorias = sum(item['total'] for item in ranking) or Decimal('1.00')
        ranking_categorias = [
            {
                "categoria": item['categoria'],
                "nome": dict(Gasto.CATEGORIAS_CHOICES).get(item['categoria'], item['categoria']),
                "total": float(item['total']),
                "quantidade": item['quantidade'],
                "percentual": round(float(item['total'] / total_categorias) * 100, 1)
            }
            for item in ranking
        ]

        # Evolução mensal comparativa (últimos 12 meses)
        meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        evolucao_mensal = []
        for i in range(11, -1, -1):
            m = mes_int - i
            a = ano_int
            while m <= 0:
                m += 12
                a -= 1

            # Gastos do mês (por data_efetiva = data_competencia com fallback)
            gastos_agg = base_queryset.filter(
                data_efetiva__month=m, data_efetiva__year=a
            ).aggregate(total=Sum('valor'))
            total_gastos_mes = gastos_agg['total'] or Decimal('0.00')

            # Receitas do mês (por data)
            receitas_agg = receitas_queryset.filter(
                data__month=m, data__year=a
            ).aggregate(total=Sum('valor'))
            total_receitas_mes = receitas_agg['total'] or Decimal('0.00')

            evolucao_mensal.append({
                "mes": meses_labels[m - 1],
                "ano": a,
                "receitas": float(total_receitas_mes),
                "gastos": float(total_gastos_mes)
            })

        # Média diária
        dias_no_mes = monthrange(ano_int, mes_int)[1]
        media_diaria = float(total_mes) / dias_no_mes if dias_no_mes > 0 else 0.0

        return Response({
            "periodo": {
                "mes": mes_int,
                "ano": ano_int,
                "mes_nome": MES_NOMES[mes_int - 1]
            },
            "total_mes": float(total_mes),
            "total_mes_anterior": float(total_anterior),
            "variacao_absoluta": float(variacao_absoluta),
            "variacao_percentual": round(float(variacao_percentual), 2),
            "media_diaria": round(media_diaria, 2),
            "maior_gasto": maior_gasto,
            "quantidade_gastos": agg_atual['quantidade'] or 0,
            "ranking_categorias": ranking_categorias,
            "evolucao_mensal": evolucao_mensal,
            "total_receitas": float(total_receitas),
            "total_gastos_pagos": float(total_gastos_pagos),
            "saldo": float(saldo)
        })

    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# -------------------------
# RECEITAS
# -------------------------
@api_view(['GET', 'POST'])
def receitas(request):
    try:
        if request.method == 'GET':
            user_family = get_user_family(request.user)

            if user_family:
                queryset = Receita.objects.filter(
                    Q(family=user_family) | Q(user=request.user, family__isnull=True)
                )
            else:
                queryset = Receita.objects.filter(user=request.user)

            # Filtro por período
            data_inicio = request.query_params.get('data_inicio')
            data_fim = request.query_params.get('data_fim')
            if data_inicio:
                queryset = queryset.filter(data__gte=data_inicio)
            if data_fim:
                queryset = queryset.filter(data__lte=data_fim)

            queryset = queryset.order_by('-data', '-criado_em')

            # Paginação simples
            limite = int(request.query_params.get('limite', 50))
            if limite > 100:
                limite = 100
            queryset = queryset[:limite]

            serializer = ReceitaSerializer(queryset, many=True)
            return Response({
                "receitas": serializer.data,
                "total": len(serializer.data)
            })

        elif request.method == 'POST':
            dados = request.data.copy()
            serializer = ReceitaSerializer(data=dados)

            if serializer.is_valid():
                family = get_user_family(request.user)
                receita = serializer.save(user=request.user, family=family)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            # Formatar erros de validação
            errors = {}
            for field, messages in serializer.errors.items():
                errors[field] = messages[0] if isinstance(messages, list) else str(messages)

            return Response(
                {"erro": "Dados inválidos", "detalhes": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        logger.error(f"Erro na API de receitas: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )