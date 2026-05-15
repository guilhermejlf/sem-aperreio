import pytest
from rest_framework import status
from api.models import Receita


@pytest.mark.django_db
class TestReceitas:
    def test_lista_receitas(self, authenticated_client, receita):
        response = authenticated_client.get('/api/receitas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_criar_receita(self, authenticated_client):
        from datetime import date
        hoje = date.today().isoformat()
        data = {
            'valor': '2500.00',
            'descricao': 'Salário',
            'data': hoje,
        }
        response = authenticated_client.post('/api/receitas/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Receita.objects.filter(descricao='Salário').exists()

    def test_atualizar_receita(self, authenticated_client, receita):
        from datetime import date
        hoje = date.today().isoformat()
        data = {
            'valor': '3000.00',
            'descricao': 'Atualizado',
            'data': hoje,
        }
        response = authenticated_client.put(f'/api/receitas/{receita.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        receita.refresh_from_db()
        assert receita.valor == 3000.00

    def test_deletar_receita(self, authenticated_client, receita):
        response = authenticated_client.delete(f'/api/receitas/{receita.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Receita.objects.filter(id=receita.id).exists()
