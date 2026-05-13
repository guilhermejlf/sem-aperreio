import csv
import io
import os
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse, HttpResponse
import logging
from calendar import monthrange

from django.db import models
from django.db.models import Q, Sum, Count, Max
from django.db.models.functions import Coalesce, TruncMonth
from decimal import Decimal
from .models import Gasto, FamilyMembership, Receita, Family, MetaGasto
from .serializers import GastoSerializer, ReceitaSerializer, MetaGastoSerializer
from .permissions import GastoPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

logger = logging.getLogger(__name__)

def _clean_optional_dates(data, fields=('data_competencia', 'data_pagamento')):
    """Converte strings vazias em None para campos de data opcionais no DRF."""
    for field in fields:
        if field in data and data[field] == '':
            data[field] = None
    return data

# -------------------------
# IA - PREVISÃO COM DADOS REAIS (por categoria)
# -------------------------
from sklearn.linear_model import LinearRegression
import numpy as np
from collections import defaultdict


def _treinar_modelo_temporal(totais_por_mes):
    """
    Treina LinearRegression com índice temporal como feature.
    totais_por_mes: lista ordenada de floats (total do mês)
    Retorna modelo treinado ou None se insuficiente.
    """
    n = len(totais_por_mes)
    if n < 2:
        return None
    X = np.arange(n).reshape(-1, 1)
    y = np.array([float(v) for v in totais_por_mes])
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo


def _prever_serie(serie, mes_alvo_idx):
    """
    Prevê valor para um índice temporal alvo dado uma série histórica.
    Fallback: < 3 meses -> média simples.
    Retorna (valor, modo).
    """
    n = len(serie)
    if n == 0:
        return 0.0, "sem_dados"
    if n < 3:
        media = sum(float(v) for v in serie) / n
        return media, "media"
    modelo = _treinar_modelo_temporal(serie)
    if modelo is None:
        return 0.0, "sem_dados"
    valor = max(0.0, float(modelo.predict(np.array([[mes_alvo_idx]]))[0]))
    return valor, "modelo"


def _construir_serie_categoria(meses_unicos, dados_categoria):
    """
    Constrói série temporal completa (meses faltantes = 0) para uma categoria.
    """
    return [dados_categoria.get(m, 0.0) for m in meses_unicos]


@api_view(["POST"])
def prever_gasto(request):
    try:
        mes = request.data.get("mes")
        ano = request.data.get("ano")

        queryset = get_user_gastos_queryset(request.user)

        # Agrupar por (ano, mes, categoria)
        categoria_map = defaultdict(lambda: defaultdict(float))
        for g in queryset:
            data = g.data_efetiva
            if data:
                categoria_map[g.categoria][(data.year, data.month)] += float(g.valor)

        if not categoria_map:
            return Response(
                {"erro": "Nenhum gasto encontrado para previsão. Cadastre gastos e tente novamente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Meses únicos ordenados (união de todos os meses de todas as categorias)
        meses_unicos = sorted({
            (ano, mes)
            for cat_dict in categoria_map.values()
            for (ano, mes) in cat_dict.keys()
        })

        n_meses = len(meses_unicos)
        if n_meses < 1:
            return Response(
                {"erro": "Nenhum gasto encontrado para previsão. Cadastre gastos e tente novamente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Determinar mês alvo
        ultimo_ano, ultimo_mes = meses_unicos[-1]
        if ano is not None and mes is not None:
            try:
                mes_alvo = int(mes)
                ano_alvo = int(ano)
            except (ValueError, TypeError):
                return Response(
                    {"erro": "Mês e ano devem ser números válidos"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            if ultimo_mes == 12:
                mes_alvo = 1
                ano_alvo = ultimo_ano + 1
            else:
                mes_alvo = ultimo_mes + 1
                ano_alvo = ultimo_ano

        # Índice do mês alvo no eixo temporal (após o último mês conhecido)
        distancia = (ano_alvo - ultimo_ano) * 12 + (mes_alvo - ultimo_mes)
        mes_alvo_idx = n_meses - 1 + distancia

        # Prever por categoria
        categorias_labels = dict(Gasto.CATEGORIAS_CHOICES)
        previsao_por_categoria = {}
        total_previsto = 0.0
        modos_usados = set()

        for cat_key, cat_dict in categoria_map.items():
            serie = _construir_serie_categoria(meses_unicos, cat_dict)
            valor, modo = _prever_serie(serie, mes_alvo_idx)
            previsao_por_categoria[categorias_labels.get(cat_key, cat_key)] = round(valor, 2)
            total_previsto += valor
            if modo != "sem_dados":
                modos_usados.add(modo)

        # Determinar modo geral
        modo_geral = "modelo" if "modelo" in modos_usados else "media"

        # Dados históricos para contexto (total por mês, últimos 6)
        historico = []
        for (a, m) in meses_unicos[-6:]:
            total_mes = sum(cat_dict.get((a, m), 0.0) for cat_dict in categoria_map.values())
            historico.append({"ano": a, "mes": m, "total": round(total_mes, 2)})

        total_previsto = max(0, min(total_previsto, 1000000))

        return Response({
            "previsao": round(total_previsto, 2),
            "mes": mes_alvo,
            "ano": ano_alvo,
            "moeda": "BRL",
            "modo": modo_geral,
            "por_categoria": previsao_por_categoria,
            "dados_historicos": historico,
            "meses_de_dados": n_meses,
            "mensagem": (
                "Previsão baseada em média simples (poucos dados)." if modo_geral == "media"
                else "Previsão baseada em tendência dos últimos meses por categoria."
            )
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
            dados = _clean_optional_dates(dados)
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
                alerta = check_budget_alert(request.user, gasto)
                return Response(
                    {
                        "gasto": serializer.data,
                        "alerta_meta": alerta
                    },
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
            dados = _clean_optional_dates(dados)
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
                alerta = check_budget_alert(request.user, gasto)
                return Response(
                    {
                        "gasto": serializer.data,
                        "alerta_meta": alerta
                    },
                    status=status.HTTP_200_OK
                )
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


@api_view(['GET', 'PUT', 'DELETE'])
def receita_detail(request, pk):
    try:
        receita = Receita.objects.get(pk=pk)
    except Receita.DoesNotExist:
        return Response(
            {"erro": "Receita não encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # Check permission - same logic as gasto
    permission = GastoPermission()
    if not permission.has_object_permission(request, None, receita):
        return Response(
            {"erro": "Você não tem permissão para acessar esta receita."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        if request.method == 'GET':
            serializer = ReceitaSerializer(receita)
            return Response(serializer.data)

        elif request.method == 'PUT':
            dados = request.data.copy()
            dados = _clean_optional_dates(dados, fields=('data_competencia',))
            # Se data_competencia não informada, manter existente ou copiar de data
            if not dados.get('data_competencia'):
                if dados.get('data'):
                    dados['data_competencia'] = dados['data']
                else:
                    dados['data_competencia'] = receita.data_competencia or receita.data
            serializer = ReceitaSerializer(receita, data=dados)
            if serializer.is_valid():
                if receita.user != request.user:
                    user_membership = get_user_membership(request.user)
                    if not user_membership or user_membership.role != 'admin':
                        return Response(
                            {"erro": "Você não tem permissão para editar esta receita."},
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
            if receita.user != request.user:
                user_membership = get_user_membership(request.user)
                if not user_membership or user_membership.role != 'admin':
                    return Response(
                        {"erro": "Você não tem permissão para excluir esta receita."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            receita.delete()
            return Response(
                {"mensagem": "Receita excluída com sucesso"}, 
                status=status.HTTP_204_NO_CONTENT
            )

    except Exception as e:
        logger.error(f"Erro no detalhe da receita: {e}")
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

        # Total de receitas no período (por data_competencia com fallback para data)
        receitas_agg = receitas_queryset.filter(
            Q(data_competencia__month=mes_int, data_competencia__year=ano_int) |
            Q(data_competencia__isnull=True, data__month=mes_int, data__year=ano_int)
        ).aggregate(total=Sum('valor'))
        total_receitas = receitas_agg['total'] or Decimal('0.00')

        # Total de gastos pagos no período (por data_competencia via data_efetiva)
        gastos_pagos_agg = base_queryset.filter(
            data_efetiva__month=mes_int,
            data_efetiva__year=ano_int,
            pago=True
        ).aggregate(total=Sum('valor'))
        total_gastos_pagos = gastos_pagos_agg['total'] or Decimal('0.00')

        # Total a pagar (gastos não pagos do período atual)
        pendentes_agg = queryset_atual.filter(pago=False).aggregate(
            total=Sum('valor'),
            quantidade=Count('id')
        )
        total_a_pagar = pendentes_agg['total'] or Decimal('0.00')
        quantidade_pendentes = pendentes_agg['quantidade'] or 0

        # Saldo
        saldo = total_receitas - total_gastos_pagos

        # Previsão de saldo até o fim do mês
        saldo_projetado = saldo - total_a_pagar
        if total_a_pagar > 0:
            if saldo_projetado < 0:
                previsao_mensagem = f"Se você não tiver novas receitas, seu saldo ficará negativo em R$ {float(abs(saldo_projetado)):.2f}"
            else:
                previsao_mensagem = f"Mesmo com as contas pendentes, você ainda terá R$ {float(saldo_projetado):.2f} disponíveis"
        else:
            previsao_mensagem = None

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

            # Receitas do mês (por data_competencia com fallback para data)
            receitas_agg = receitas_queryset.filter(
                Q(data_competencia__month=m, data_competencia__year=a) |
                Q(data_competencia__isnull=True, data__month=m, data__year=a)
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

        # Metas de gasto
        metas_context = _build_metas_context(request.user, mes_int, ano_int)

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
            "total_a_pagar": float(total_a_pagar),
            "quantidade_pendentes": quantidade_pendentes,
            "saldo": float(saldo),
            "saldo_projetado": float(saldo_projetado),
            "previsao_mensagem": previsao_mensagem,
            "metas": metas_context
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
            dados = _clean_optional_dates(dados, fields=('data_competencia',))
            # Se data_competencia não informada, copiar de data
            if not dados.get('data_competencia') and dados.get('data'):
                dados['data_competencia'] = dados['data']
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


    except Exception as e:
        logger.error(f"Erro na API de receitas: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# -------------------------
# EXTRATO UNIFICADO (Gastos + Receitas)
# -------------------------
@api_view(['GET'])
def extrato(request):
    """Retorna lista unificada de gastos e receitas do usuário/família, ordenada por data decrescente."""
    try:
        user_family = get_user_family(request.user)

        # --- Gastos ---
        if user_family:
            gastos_qs = Gasto.objects.filter(
                Q(family=user_family) | Q(user=request.user, family__isnull=True)
            )
        else:
            gastos_qs = Gasto.objects.filter(user=request.user)

        gastos_qs = gastos_qs.annotate(data_efetiva=Coalesce('data_competencia', 'data'))

        # --- Receitas ---
        if user_family:
            receitas_qs = Receita.objects.filter(
                Q(family=user_family) | Q(user=request.user, family__isnull=True)
            )
        else:
            receitas_qs = Receita.objects.filter(user=request.user)

        # --- Filtros comuns ---
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')
        if mes and ano:
            try:
                mes_int = int(mes)
                ano_int = int(ano)
                from calendar import monthrange
                ultimo_dia = monthrange(ano_int, mes_int)[1]
                inicio = f"{ano_int}-{mes_int:02d}-01"
                fim = f"{ano_int}-{mes_int:02d}-{ultimo_dia}"
                gastos_qs = gastos_qs.filter(data_efetiva__range=(inicio, fim))
                receitas_qs = receitas_qs.filter(data__range=(inicio, fim))
            except (ValueError, IndexError):
                pass

        categoria = request.query_params.get('categoria')
        if categoria:
            gastos_qs = gastos_qs.filter(categoria=categoria)

        # --- Filtro por tipo ---
        tipo = request.query_params.get('tipo')
        if tipo == 'gastos':
            receitas_qs = Receita.objects.none()
        elif tipo == 'receitas':
            gastos_qs = Gasto.objects.none()

        # --- Filtro por status pago (apenas gastos) ---
        pago = request.query_params.get('pago')
        if pago is not None:
            gastos_qs = gastos_qs.filter(pago=pago.lower() in ('true', '1', 'yes', 'sim'))

        # --- Serializar ---
        gastos_qs = gastos_qs.order_by('-data_efetiva', '-criado_em')
        receitas_qs = receitas_qs.order_by('-data', '-criado_em')

        gastos_serializer = GastoSerializer(gastos_qs, many=True)
        receitas_serializer = ReceitaSerializer(receitas_qs, many=True)

        # --- Unificar com campo tipo ---
        itens = []
        for g in gastos_serializer.data:
            itens.append({
                "tipo": "gasto",
                "id": g["id"],
                "categoria": g["categoria"],
                "descricao": g["descricao"],
                "valor": g["valor"],
                "data": g.get("data_competencia") or g.get("data"),
                "pago": g["pago"],
                "data_pagamento": g.get("data_pagamento"),
                "user_name": g.get("user_name"),
                "is_group": g.get("is_group"),
                "criado_em": g.get("criado_em"),
            })
        for r in receitas_serializer.data:
            itens.append({
                "tipo": "receita",
                "id": r["id"],
                "categoria": None,
                "descricao": r["descricao"] or "Receita",
                "valor": r["valor"],
                "data": r.get("data_competencia") or r.get("data"),
                "pago": True,
                "data_pagamento": None,
                "user_name": r.get("user_name"),
                "is_group": r.get("is_group"),
                "criado_em": r.get("criado_em"),
            })

        # Ordenar por data decrescente
        itens.sort(key=lambda x: x["data"] or "", reverse=True)

        # Resumo
        total_gastos = sum(float(i["valor"]) for i in itens if i["tipo"] == "gasto")
        total_receitas = sum(float(i["valor"]) for i in itens if i["tipo"] == "receita")

        return Response({
            "itens": itens,
            "total": len(itens),
            "resumo": {
                "total_gastos": round(total_gastos, 2),
                "total_receitas": round(total_receitas, 2),
                "saldo": round(total_receitas - total_gastos, 2),
            }
        })

    except Exception as e:
        logger.error(f"Erro na API de extrato: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


try:
    from openpyxl import Workbook
    _HAS_OPENPYXL = True
except ImportError:
    _HAS_OPENPYXL = False


def _get_gastos_filtrados(request):
    """Retorna queryset de gastos do usuário/família com os mesmos filtros de /api/gastos/."""
    queryset = get_user_gastos_queryset(request.user)

    categoria = request.query_params.get('categoria')
    if categoria:
        queryset = queryset.filter(categoria=categoria)

    data_inicio = request.query_params.get('data_inicio')
    data_fim = request.query_params.get('data_fim')
    if data_inicio:
        queryset = queryset.filter(data_efetiva__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data_efetiva__lte=data_fim)

    competencia_inicio = request.query_params.get('competencia_inicio')
    competencia_fim = request.query_params.get('competencia_fim')
    if competencia_inicio:
        queryset = queryset.filter(data_competencia__gte=competencia_inicio)
    if competencia_fim:
        queryset = queryset.filter(data_competencia__lte=competencia_fim)

    pagamento_inicio = request.query_params.get('pagamento_inicio')
    pagamento_fim = request.query_params.get('pagamento_fim')
    if pagamento_inicio:
        queryset = queryset.filter(data_pagamento__gte=pagamento_inicio)
    if pagamento_fim:
        queryset = queryset.filter(data_pagamento__lte=pagamento_fim)

    pago = request.query_params.get('pago')
    if pago is not None:
        queryset = queryset.filter(pago=pago.lower() in ('true', '1', 'yes', 'sim'))

    # Suporte a filtro por mes/ano (usado pela tela de Extrato)
    mes = request.query_params.get('mes')
    ano = request.query_params.get('ano')
    if mes and ano:
        try:
            from calendar import monthrange
            mes_int = int(mes)
            ano_int = int(ano)
            ultimo_dia = monthrange(ano_int, mes_int)[1]
            inicio = f"{ano_int}-{mes_int:02d}-01"
            fim = f"{ano_int}-{mes_int:02d}-{ultimo_dia}"
            queryset = queryset.filter(data_efetiva__range=(inicio, fim))
        except (ValueError, IndexError):
            pass

    return queryset.order_by('-data_efetiva', '-criado_em')


@api_view(['GET'])
def exportar_csv(request):
    try:
        queryset = _get_gastos_filtrados(request)

        def stream_csv():
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(['data', 'categoria', 'valor', 'descricao', 'pago', 'data_competencia', 'data_pagamento', 'criado_por'])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

            for g in queryset.iterator():
                writer.writerow([
                    g.data,
                    g.get_categoria_display(),
                    str(g.valor).replace('.', ','),
                    g.descricao or '',
                    'Sim' if g.pago else 'Não',
                    g.data_competencia or '',
                    g.data_pagamento or '',
                    g.user.username
                ])
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)

        response = StreamingHttpResponse(stream_csv(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="gastos.csv"'
        return response

    except Exception as e:
        logger.error(f"Erro na exportação CSV: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def exportar_xlsx(request):
    try:
        if not _HAS_OPENPYXL:
            return Response(
                {"erro": "Biblioteca openpyxl não instalada. Contate o administrador."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        queryset = _get_gastos_filtrados(request)

        wb = Workbook()
        ws = wb.active
        ws.title = "Gastos"

        headers = ['Data', 'Categoria', 'Valor', 'Descrição', 'Pago', 'Mês Competência', 'Data Pagamento', 'Criado por']
        ws.append(headers)

        for g in queryset.iterator():
            ws.append([
                g.data,
                g.get_categoria_display(),
                float(g.valor),
                g.descricao or '',
                'Sim' if g.pago else 'Não',
                g.data_competencia or '',
                g.data_pagamento or '',
                g.user.username
            ])

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=gastos.xlsx'
        return response

    except Exception as e:
        logger.error(f"Erro na exportação XLSX: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'
        )


@api_view(['GET'])
def exportar_pdf(request):
    """Exporta extrato unificado (gastos + receitas) como PDF estilizado."""
    try:
        from datetime import datetime

        user_family = get_user_family(request.user)

        # --- Gastos ---
        if user_family:
            gastos_qs = Gasto.objects.filter(
                Q(family=user_family) | Q(user=request.user, family__isnull=True)
            )
        else:
            gastos_qs = Gasto.objects.filter(user=request.user)
        gastos_qs = gastos_qs.annotate(data_efetiva=Coalesce('data_competencia', 'data'))

        # --- Receitas ---
        if user_family:
            receitas_qs = Receita.objects.filter(
                Q(family=user_family) | Q(user=request.user, family__isnull=True)
            )
        else:
            receitas_qs = Receita.objects.filter(user=request.user)

        # --- Filtros ---
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')
        mes_int = None
        ano_int = None
        if mes and ano:
            try:
                mes_int = int(mes)
                ano_int = int(ano)
                from calendar import monthrange
                ultimo_dia = monthrange(ano_int, mes_int)[1]
                inicio = f"{ano_int}-{mes_int:02d}-01"
                fim = f"{ano_int}-{mes_int:02d}-{ultimo_dia}"
                gastos_qs = gastos_qs.filter(data_efetiva__range=(inicio, fim))
                receitas_qs = receitas_qs.filter(data__range=(inicio, fim))
            except (ValueError, IndexError):
                pass

        categoria = request.query_params.get('categoria')
        if categoria:
            gastos_qs = gastos_qs.filter(categoria=categoria)

        tipo = request.query_params.get('tipo')
        if tipo == 'gastos':
            receitas_qs = Receita.objects.none()
        elif tipo == 'receitas':
            gastos_qs = Gasto.objects.none()

        pago = request.query_params.get('pago')
        if pago is not None:
            gastos_qs = gastos_qs.filter(pago=pago.lower() in ('true', '1', 'yes', 'sim'))

        # --- Dados ---
        itens = []
        for g in gastos_qs.order_by('-data_efetiva'):
            itens.append({
                "tipo": "GASTO",
                "data": (g.data_competencia or g.data).strftime('%d/%m/%Y') if (g.data_competencia or g.data) else "",
                "categoria": g.get_categoria_display() or "",
                "descricao": g.descricao or "",
                "valor": float(g.valor),
            })
        for r in receitas_qs.order_by('-data'):
            itens.append({
                "tipo": "RECEITA",
                "data": r.data.strftime('%d/%m/%Y') if r.data else "",
                "categoria": "-",
                "descricao": r.descricao or "",
                "valor": float(r.valor),
            })

        itens.sort(key=lambda x: datetime.strptime(x["data"], '%d/%m/%Y') if x["data"] else datetime.min, reverse=True)

        total_gastos = sum(i["valor"] for i in itens if i["tipo"] == "GASTO")
        total_receitas = sum(i["valor"] for i in itens if i["tipo"] == "RECEITA")
        saldo = total_receitas - total_gastos

        # --- Helpers ---
        def fmt_brl(v):
            s = f"{abs(v):,.2f}"
            return s.replace(',', 'X').replace('.', ',').replace('X', '.')

        MESES = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        periodo_str = f"{MESES[mes_int]}/{ano_int}" if mes_int and ano_int else "Todos os registros"

        # --- Gerar PDF ---
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        elements = []
        styles = getSampleStyleSheet()

        # Cores
        C_TITLE = colors.HexColor('#10b981')
        C_HEADER_BG = colors.HexColor('#111827')
        C_HEADER_TEXT = colors.whitesmoke
        C_RECEITA_BG = colors.HexColor('#dcfce7')
        C_RECEITA_TEXT = colors.HexColor('#166534')
        C_GASTO_BG = colors.HexColor('#fee2e2')
        C_GASTO_TEXT = colors.HexColor('#991b1b')
        C_SALDO_BG = colors.HexColor('#dbeafe')
        C_SALDO_TEXT = colors.HexColor('#1e40af')
        C_SUBTITLE = colors.HexColor('#64748b')
        C_BORDER = colors.HexColor('#e5e7eb')
        C_ROW_ALT = colors.HexColor('#f8fafc')

        # Estilos customizados
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=C_TITLE,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold',
        )
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=C_SUBTITLE,
            alignment=TA_CENTER,
            spaceAfter=20,
        )
        section_title = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=C_HEADER_BG,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
        )
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=C_SUBTITLE,
            alignment=TA_CENTER,
            spaceBefore=30,
        )
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=9,
            textColor=C_SUBTITLE,
            alignment=TA_CENTER,
            spaceAfter=2,
        )
        tagline_style = ParagraphStyle(
            'Tagline',
            parent=styles['Normal'],
            fontSize=8,
            textColor=C_SUBTITLE,
            alignment=TA_CENTER,
            spaceAfter=16,
        )

        # Info topo direito
        user_name = request.user.get_full_name() or request.user.username
        now_str = datetime.now().strftime('%d/%m/%Y às %H:%M')
        info_data = [
            ['', Paragraph(f"Solicitado por: <b>{user_name}</b>", info_style)],
            ['', Paragraph(f"Gerado em: {now_str}", info_style)],
        ]
        info_table = Table(info_data, colWidths=[10*cm, 7*cm])
        info_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*cm))

        # Logo + Título + Tagline
        logo_path = str(settings.BASE_DIR.parent / 'frontend' / 'src' / 'assets' / 'logo-pdf.png')
        logger.debug(f"PDF logo path: {logo_path}")
        try:
            logo = Image(logo_path, width=4*cm, height=4*cm)
            logo.hAlign = 'CENTER'
            elements.append(logo)
        except Exception as e:
            logger.warning(f"PDF logo failed: {e}")
        elements.append(Paragraph(f"Relatório Financeiro Familiar — {periodo_str}", subtitle_style))

        # Linha divisória
        line_data = [['']]
        line_table = Table(line_data, colWidths=[17*cm])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 1, C_BORDER),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.8*cm))

        # Cards de resumo
        card_data = [
            ['Receitas', 'Gastos', 'Saldo'],
            [f'R$ {fmt_brl(total_receitas)}', f'R$ {fmt_brl(total_gastos)}', f'R$ {fmt_brl(saldo)}'],
        ]
        card_table = Table(card_data, colWidths=[5.67*cm, 5.67*cm, 5.67*cm])
        card_table.setStyle(TableStyle([
            # Headers
            ('BACKGROUND', (0, 0), (-1, 0), C_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), C_HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            # Valores
            ('BACKGROUND', (0, 1), (0, 1), C_RECEITA_BG),
            ('TEXTCOLOR', (0, 1), (0, 1), C_RECEITA_TEXT),
            ('BACKGROUND', (1, 1), (1, 1), C_GASTO_BG),
            ('TEXTCOLOR', (1, 1), (1, 1), C_GASTO_TEXT),
            ('BACKGROUND', (2, 1), (2, 1), C_SALDO_BG),
            ('TEXTCOLOR', (2, 1), (2, 1), C_SALDO_TEXT),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 12),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 14),
            ('TOPPADDING', (0, 1), (-1, 1), 14),
            # Grid
            ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(card_table)

        # Título da seção
        elements.append(Spacer(1, 0.6*cm))
        elements.append(Paragraph("Extrato Financeiro", section_title))

        # Tabela de extrato
        extrato_data = [['Data', 'Tipo', 'Categoria', 'Descrição', 'Valor']]
        for item in itens:
            tipo_label = 'Receita' if item['tipo'] == 'RECEITA' else 'Gasto'
            valor_sinal = f"+ R$ {fmt_brl(item['valor'])}" if item['tipo'] == 'RECEITA' else f"- R$ {fmt_brl(item['valor'])}"
            extrato_data.append([
                item['data'],
                tipo_label,
                item['categoria'],
                Paragraph(item['descricao'][:50], styles['Normal']),
                valor_sinal,
            ])

        extrato_table = Table(extrato_data, colWidths=[2.5*cm, 2.2*cm, 3.3*cm, 6.5*cm, 2.5*cm], repeatRows=1)
        extrato_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), C_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), C_HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            # Linhas alternadas
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, C_ROW_ALT]),
            # Alinhamento
            ('ALIGN', (0, 1), (3, -1), 'LEFT'),
            ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            # Cores por tipo
            ('TEXTCOLOR', (1, 1), (1, -1), C_RECEITA_TEXT, 'Receita'),
            ('TEXTCOLOR', (1, 1), (1, -1), C_GASTO_TEXT, 'Gasto'),
            ('TEXTCOLOR', (4, 1), (4, -1), C_RECEITA_TEXT, '+'),
            ('TEXTCOLOR', (4, 1), (4, -1), C_GASTO_TEXT, '-'),
            # Grid leve
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, C_BORDER),
            ('LINEABOVE', (0, 0), (-1, 0), 0.5, C_BORDER),
        ]))
        elements.append(extrato_table)

        # Rodapé
        elements.append(Spacer(1, 0.8*cm))
        elements.append(Paragraph("Relatório gerado automaticamente pelo Sem Aperreio.", footer_style))

        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="extrato.pdf"'
        return response

    except Exception as e:
        logger.error(f"Erro na exportação PDF: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# -------------------------

def _get_meta_status(pct):
    if pct > 100:
        return 'critical'
    elif pct > 80:
        return 'danger'
    elif pct > 50:
        return 'warning'
    return 'ok'


def _get_gasto_realizado(user, categoria, mes, ano):
    """Calcula o total gasto pelo usuário em uma categoria/mês/ano."""
    gastos = Gasto.objects.filter(
        user=user,
        data_competencia__month=mes,
        data_competencia__year=ano
    )
    if categoria:
        gastos = gastos.filter(categoria=categoria)
    total = gastos.aggregate(total=Sum('valor'))['total'] or 0
    return round(float(total), 2)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_metas(request):
    """Lista todas as metas do usuário para um mês/ano."""
    try:
        mes = int(request.query_params.get('mes', 0))
        ano = int(request.query_params.get('ano', 0))
        if not (1 <= mes <= 12 and ano > 2000):
            return Response(
                {"erro": "Mês (1-12) e ano (>2000) são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        metas_context = _build_metas_context(request.user, mes, ano)
        return Response({"metas": metas_context, "mes": mes, "ano": ano})
    except Exception as e:
        logger.error(f"Erro ao listar metas: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _get_soma_metas_categoria(user, mes, ano, exclude_pk=None):
    """Retorna a soma dos valores das metas por categoria (excluindo a meta geral)."""
    qs = MetaGasto.objects.filter(user=user, mes=mes, ano=ano, categoria__isnull=False)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    result = qs.aggregate(total=Sum('valor_meta'))
    total = result.get('total') or Decimal('0.00')
    return float(total)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_meta(request):
    """Cria uma nova meta de gasto."""
    try:
        categoria = request.data.get('categoria') or None
        mes = int(request.data.get('mes', 0))
        ano = int(request.data.get('ano', 0))
        valor_meta = float(request.data.get('valor_meta', 0))

        if not (1 <= mes <= 12 and ano > 2000):
            return Response(
                {"erro": "Mês (1-12) e ano (>2000) são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if valor_meta <= 0:
            return Response(
                {"erro": "Valor da meta deve ser maior que zero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar duplicata
        if MetaGasto.objects.filter(user=request.user, categoria=categoria, mes=mes, ano=ano).exists():
            return Response(
                {"erro": "Já existe uma meta para esta categoria neste período"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validação: meta geral é o teto
        meta_geral = MetaGasto.objects.filter(user=request.user, mes=mes, ano=ano, categoria__isnull=True).first()
        if categoria:
            # Meta por categoria: soma das categorias não pode ultrapassar a meta geral
            if meta_geral:
                soma_categorias = _get_soma_metas_categoria(request.user, mes, ano)
                if soma_categorias + valor_meta > float(meta_geral.valor_meta):
                    return Response(
                        {"erro": f"A soma das metas por categoria (R$ {soma_categorias + valor_meta:.2f}) ultrapassa a meta geral de R$ {float(meta_geral.valor_meta):.2f}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            # Meta geral: deve ser >= soma das metas por categoria existentes
            soma_categorias = _get_soma_metas_categoria(request.user, mes, ano)
            if valor_meta < soma_categorias:
                return Response(
                    {"erro": f"A meta geral (R$ {valor_meta:.2f}) não pode ser menor que a soma das metas por categoria (R$ {soma_categorias:.2f})"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        meta = MetaGasto.objects.create(
            user=request.user,
            categoria=categoria,
            mes=mes,
            ano=ano,
            valor_meta=valor_meta
        )
        serializer = MetaGastoSerializer(meta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erro ao criar meta: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_meta(request, pk):
    """Atualiza o valor de uma meta existente."""
    try:
        meta = MetaGasto.objects.get(pk=pk, user=request.user)
        valor_meta = float(request.data.get('valor_meta', 0))

        if valor_meta <= 0:
            return Response(
                {"erro": "Valor da meta deve ser maior que zero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validação: meta geral é o teto
        mes, ano = meta.mes, meta.ano
        meta_geral = MetaGasto.objects.filter(user=request.user, mes=mes, ano=ano, categoria__isnull=True).first()
        if meta.categoria:
            # Atualizando meta por categoria
            if meta_geral:
                soma_categorias = _get_soma_metas_categoria(request.user, mes, ano, exclude_pk=meta.pk)
                if soma_categorias + valor_meta > float(meta_geral.valor_meta):
                    return Response(
                        {"erro": f"A soma das metas por categoria (R$ {soma_categorias + valor_meta:.2f}) ultrapassa a meta geral de R$ {float(meta_geral.valor_meta):.2f}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            # Atualizando meta geral
            soma_categorias = _get_soma_metas_categoria(request.user, mes, ano)
            if valor_meta < soma_categorias:
                return Response(
                    {"erro": f"A meta geral (R$ {valor_meta:.2f}) não pode ser menor que a soma das metas por categoria (R$ {soma_categorias:.2f})"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        meta.valor_meta = valor_meta
        meta.save()
        serializer = MetaGastoSerializer(meta)
        return Response(serializer.data)
    except MetaGasto.DoesNotExist:
        return Response(
            {"erro": "Meta não encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Erro ao atualizar meta: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletar_meta(request, pk):
    """Deleta uma meta de gasto."""
    try:
        meta = MetaGasto.objects.get(pk=pk, user=request.user)
        meta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except MetaGasto.DoesNotExist:
        return Response(
            {"erro": "Meta não encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Erro ao deletar meta: {e}")
        return Response(
            {"erro": "Erro interno no servidor"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _build_metas_context(user, mes, ano):
    """Constrói o contexto de metas para o dashboard."""
    metas = MetaGasto.objects.filter(user=user, mes=mes, ano=ano)
    
    geral = None
    por_categoria = []
    
    for meta in metas:
        serializer = MetaGastoSerializer(meta)
        data = serializer.data
        if meta.categoria is None:
            geral = data
        else:
            por_categoria.append(data)
    
    return {"geral": geral, "por_categoria": por_categoria}


def check_budget_alert(user, gasto):
    """
    Verifica se o gasto recém-criado/atualizado ultrapassa alguma meta.
    Retorna dict com alerta ou None.
    """
    data_efetiva = gasto.data_competencia or gasto.data
    if not data_efetiva:
        return None
    
    mes = data_efetiva.month
    ano = data_efetiva.year
    
    metas = MetaGasto.objects.filter(user=user, mes=mes, ano=ano)
    if not metas.exists():
        return None
    
    for meta in metas:
        if meta.categoria:
            total_gasto = Gasto.objects.filter(
                user=user,
                data_competencia__month=mes,
                data_competencia__year=ano,
                categoria=meta.categoria
            ).aggregate(total=Sum('valor'))['total'] or 0
            categoria_nome = dict(Gasto.CATEGORIAS_CHOICES).get(meta.categoria, meta.categoria)
        else:
            total_gasto = Gasto.objects.filter(
                user=user,
                data_competencia__month=mes,
                data_competencia__year=ano
            ).aggregate(total=Sum('valor'))['total'] or 0
            categoria_nome = "Geral"
        
        if not meta.valor_meta or float(meta.valor_meta) <= 0:
            continue
        
        pct = (float(total_gasto) / float(meta.valor_meta)) * 100
        
        if pct > 100:
            return {
                "alertar": True,
                "mensagem": f"Você ultrapassou a meta de {categoria_nome} em {pct:.0f}% (R$ {float(total_gasto):.2f} / R$ {float(meta.valor_meta):.2f})",
                "categoria": categoria_nome,
                "pct": round(pct, 1),
                "status": "critical"
            }
        elif pct > 80:
            return {
                "alertar": True,
                "mensagem": f"Você atingiu {pct:.0f}% da meta de {categoria_nome} (R$ {float(total_gasto):.2f} / R$ {float(meta.valor_meta):.2f})",
                "categoria": categoria_nome,
                "pct": round(pct, 1),
                "status": "danger"
            }
    
    return None


@api_view(["DELETE"])
def flush_users(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    count = User.objects.count()
    User.objects.all().delete()
    return Response({"status": "ok", "deleted": count})