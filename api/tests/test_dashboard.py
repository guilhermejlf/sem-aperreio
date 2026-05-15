import pytest
from datetime import date
from rest_framework import status


@pytest.mark.django_db
class TestDashboard:
    def test_dashboard_retorna_dados(self, authenticated_client, gasto, receita):
        mes = date.today().month
        ano = date.today().year
        response = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        assert response.status_code == status.HTTP_200_OK
        assert 'saldo' in response.data
        assert 'total_mes' in response.data
        assert 'total_receitas' in response.data

    def test_dashboard_com_periodo(self, authenticated_client, gasto, receita):
        mes = gasto.data.month
        ano = gasto.data.year
        response = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        assert response.status_code == status.HTTP_200_OK

    def test_dashboard_nao_autenticado(self, api_client):
        response = api_client.get('/api/dashboard/?mes=5&ano=2024')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dashboard_vazio(self, authenticated_client):
        mes = date.today().month
        ano = date.today().year
        response = authenticated_client.get(f'/api/dashboard/?mes={mes}&ano={ano}')
        assert response.status_code == status.HTTP_200_OK
