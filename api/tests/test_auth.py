import pytest
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestAuthRegister:
    def test_registro_com_dados_validos(self, api_client):
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'Senha123!',
            'password2': 'Senha123!',
            'first_name': 'Test'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='testuser').exists()

    def test_registro_username_duplicado(self, api_client, user):
        data = {
            'username': user.username,
            'email': 'outro@test.com',
            'password': 'Teste123!',
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registro_sem_password(self, api_client):
        data = {'username': 'semSenha', 'email': 'test@test.com'}
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAuthLogin:
    def test_login_com_credenciais_validas(self, api_client, user):
        user.set_password('senha123')
        user.save()
        data = {'username': user.username, 'password': 'senha123'}
        response = api_client.post('/api/auth/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_com_senha_incorreta(self, api_client, user):
        user.set_password('senha123')
        user.save()
        data = {'username': user.username, 'password': 'errada'}
        response = api_client.post('/api/auth/login/', data, format='json')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST]

    def test_login_usuario_inexistente(self, api_client):
        data = {'username': 'naoexiste', 'password': 'qualquer'}
        response = api_client.post('/api/auth/login/', data, format='json')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST]


@pytest.mark.django_db
class TestAuthRefresh:
    def test_refresh_token_valido(self, api_client, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        data = {'refresh': str(refresh)}
        response = api_client.post('/api/auth/refresh/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_refresh_token_invalido(self, api_client):
        data = {'refresh': 'token-invalido'}
        response = api_client.post('/api/auth/refresh/', data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuthUser:
    def test_user_autenticado_retorna_dados(self, authenticated_client, user):
        response = authenticated_client.get('/api/auth/user/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_user_nao_autenticado_retorna_401(self, api_client):
        response = api_client.get('/api/auth/user/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
