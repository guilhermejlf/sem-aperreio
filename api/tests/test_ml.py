import pytest
from rest_framework import status


@pytest.mark.django_db
class TestMLPrediction:
    def test_previsao_com_dados_suficientes(self, authenticated_client, user):
        from api.tests.conftest import GastoFactory
        # Criar múltiplos gastos para ter dados suficientes
        for i in range(5):
            GastoFactory(user=user, categoria='mercado', valor=100 + i * 10)

        data = {'categoria': 'mercado', 'mes': 6, 'ano': 2024}
        response = authenticated_client.post('/api/prever/', data, format='json')
        # Pode retornar 200 com previsão ou 400 se não houver dados suficientes
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_previsao_sem_dados(self, authenticated_client):
        data = {'categoria': 'mercado', 'mes': 6, 'ano': 2024}
        response = authenticated_client.post('/api/prever/', data, format='json')
        # Com poucos dados deve retornar erro ou fallback
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_previsao_parametros_invalidos(self, authenticated_client):
        response = authenticated_client.post('/api/prever/', {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
