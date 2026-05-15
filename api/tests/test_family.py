import pytest
from rest_framework import status
from api.models import Family, FamilyMembership


@pytest.mark.django_db
class TestFamily:
    def test_criar_family(self, authenticated_client):
        data = {'name': 'Minha Família'}
        response = authenticated_client.post('/api/family/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Family.objects.filter(name='Minha Família').exists()

    def test_listar_families(self, authenticated_client, family):
        response = authenticated_client.get('/api/family/')
        assert response.status_code == status.HTTP_200_OK

    def test_entrar_family_com_codigo(self, authenticated_client):
        from django.contrib.auth.models import User
        # Criar outro usuário e family
        outro = User.objects.create_user(username='criador', password='teste123')
        family = Family.objects.create(name='Existente', created_by=outro)
        data = {'code': family.code}
        response = authenticated_client.post('/api/family/join/', data, format='json')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

    def test_sair_da_family(self, authenticated_client, family):
        response = authenticated_client.post('/api/family/leave/')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
