import pytest
from datetime import date
from rest_framework import status
from api.models import Gasto

HOJE = date.today().isoformat()


@pytest.mark.django_db
class TestGastosList:
    def test_lista_gastos_autenticado(self, authenticated_client, gasto):
        response = authenticated_client.get('/api/gastos/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_lista_gastos_nao_autenticado(self, api_client):
        response = api_client.get('/api/gastos/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGastosCreate:
    def test_criar_gasto_valido(self, authenticated_client, user, family):
        data = {
            'valor': '150.00',
            'categoria': 'mercado',
            'descricao': 'Compras do mês',
            'data': HOJE,
            'pago': False,
        }
        response = authenticated_client.post('/api/gastos/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Gasto.objects.filter(descricao='Compras do mês').exists()

    def test_criar_gasto_valor_negativo(self, authenticated_client):
        data = {
            'valor': '-50.00',
            'categoria': 'mercado',
            'data': HOJE,
        }
        response = authenticated_client.post('/api/gastos/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_criar_gasto_categoria_invalida(self, authenticated_client):
        data = {
            'valor': '50.00',
            'categoria': 'inexistente',
            'data': HOJE,
        }
        response = authenticated_client.post('/api/gastos/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGastosDetail:
    def test_obter_gasto_existente(self, authenticated_client, gasto):
        response = authenticated_client.get(f'/api/gastos/{gasto.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == gasto.id

    def test_obter_gasto_inexistente(self, authenticated_client):
        response = authenticated_client.get('/api/gastos/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_atualizar_gasto(self, authenticated_client, gasto):
        data = {
            'valor': '200.00',
            'categoria': 'mercado',
            'data': HOJE,
            'descricao': 'Atualizado',
            'pago': True,
        }
        response = authenticated_client.put(f'/api/gastos/{gasto.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        gasto.refresh_from_db()
        assert gasto.valor == 200.00

    def test_deletar_gasto(self, authenticated_client, gasto):
        response = authenticated_client.delete(f'/api/gastos/{gasto.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Gasto.objects.filter(id=gasto.id).exists()

    def test_deletar_gasto_de_outro_usuario(self, authenticated_client):
        from django.contrib.auth.models import User
        from api.models import Gasto
        outro_user = User.objects.create_user(username='outro', password='teste123')
        outro_gasto = Gasto.objects.create(user=outro_user, valor=100, categoria='mercado', data=HOJE)
        response = authenticated_client.delete(f'/api/gastos/{outro_gasto.id}/')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
