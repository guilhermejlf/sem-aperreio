import pytest
from rest_framework import status
from api.models import MetaGasto


@pytest.mark.django_db
class TestMetas:
    def test_listar_metas(self, authenticated_client, meta_gasto):
        response = authenticated_client.get(f'/api/metas/?mes={meta_gasto.mes}&ano={meta_gasto.ano}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_criar_meta(self, authenticated_client):
        data = {
            'categoria': 'lazer',
            'mes': 5,
            'ano': 2024,
            'valor_meta': '500.00',
        }
        response = authenticated_client.post('/api/metas/criar/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert MetaGasto.objects.filter(categoria='lazer').exists()

    def test_atualizar_meta(self, authenticated_client, meta_gasto):
        data = {'valor_meta': '800.00'}
        response = authenticated_client.put(f'/api/metas/{meta_gasto.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        meta_gasto.refresh_from_db()
        assert meta_gasto.valor_meta == 800.00

    def test_deletar_meta(self, authenticated_client, meta_gasto):
        response = authenticated_client.delete(f'/api/metas/{meta_gasto.id}/deletar/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not MetaGasto.objects.filter(id=meta_gasto.id).exists()
