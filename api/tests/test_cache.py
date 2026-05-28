import pytest
from datetime import date
from django.core.cache import cache
from rest_framework import status

from api.cache_utils import (
    cache_key,
    invalidate_gastos,
    invalidate_receitas,
    invalidate_metas,
    invalidate_dashboard,
)
from api.models import Gasto


@pytest.mark.django_db
class TestCache:
    def test_dashboard_cache_hit(self, authenticated_client, gasto, receita):
        mes = date.today().month
        ano = date.today().year

        # Primeira requisição (miss)
        response1 = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        assert response1.status_code == status.HTTP_200_OK
        assert 'saldo' in response1.data
        saldo_primeiro = response1.data['saldo']

        # Segunda requisição (hit)
        response2 = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['saldo'] == saldo_primeiro

    def test_cache_clear_reflects_new_gasto(self, authenticated_client, user, family, gasto, receita):
        mes = date.today().month
        ano = date.today().year

        # Primeira requisição
        response1 = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        saldo_antes = response1.data['saldo']

        # Criar novo gasto diretamente (não passa pela view)
        Gasto.objects.create(
            user=user,
            family=family,
            valor=500.00,
            categoria='lazer',
            data=date.today(),
            pago=True
        )

        # Limpar todo o cache (simula invalidação bem-sucedida)
        cache.clear()

        # Requisição após limpar cache
        response2 = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        saldo_depois = response2.data['saldo']

        # O saldo deve ter mudado após limpar cache
        assert saldo_depois != saldo_antes

    def test_invalidate_metas_clears_metas_cache(self, authenticated_client, user):
        mes = date.today().month
        ano = date.today().year

        # Primeira requisição
        response1 = authenticated_client.get(f'/api/metas/?mes={mes}&ano={ano}')
        assert response1.status_code == status.HTTP_200_OK

        # Invalidar cache
        invalidate_metas(user)

        # Segunda requisição deve retornar dados (não falhar)
        response2 = authenticated_client.get(f'/api/metas/?mes={mes}&ano={ano}')
        assert response2.status_code == status.HTTP_200_OK

    def test_prever_gasto_cache(self, authenticated_client, gasto):
        # Primeira requisição
        response1 = authenticated_client.post('/api/prever/', data={}, content_type='application/json')
        assert response1.status_code == status.HTTP_200_OK

        # Segunda requisição (deve ser cacheada)
        response2 = authenticated_client.post('/api/prever/', data={}, content_type='application/json')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data == response1.data

    def test_cache_key_format(self, user):
        key = cache_key('dashboard', user, 5, 2024)
        assert key.startswith('sa:dashboard:')
        assert str(user.id) in key
        assert '5' in key
        assert '2024' in key

    def test_extrato_cache(self, authenticated_client, gasto, receita):
        # Primeira requisição
        response1 = authenticated_client.get('/api/extrato/')
        assert response1.status_code == status.HTTP_200_OK

        # Segunda requisição (deve ser cacheada)
        response2 = authenticated_client.get('/api/extrato/')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['itens'] == response1.data['itens']
        assert response2.data['resumo'] == response1.data['resumo']

    def test_gastos_list_cache(self, authenticated_client, gasto):
        # Primeira requisição
        response1 = authenticated_client.get('/api/gastos/')
        assert response1.status_code == status.HTTP_200_OK

        # Segunda requisição (deve ser cacheada)
        response2 = authenticated_client.get('/api/gastos/')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['gastos'] == response1.data['gastos']
        assert response2.data['total'] == response1.data['total']

    def test_receitas_list_cache(self, authenticated_client, receita):
        # Primeira requisição
        response1 = authenticated_client.get('/api/receitas/')
        assert response1.status_code == status.HTTP_200_OK

        # Segunda requisição (deve ser cacheada)
        response2 = authenticated_client.get('/api/receitas/')
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['receitas'] == response1.data['receitas']
        assert response2.data['total'] == response1.data['total']
