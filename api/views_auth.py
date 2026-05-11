from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from .serializers_auth import RegisterSerializer
from .models import UserProfile


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Usuário criado com sucesso",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "erro": "Dados inválidos",
            "detalhes": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('identifier', '')
        password = attrs.get('password', '')

        # Buscar usuário por email ou username
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError("Credenciais inválidas.", code='authorization')
        else:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                raise serializers.ValidationError("Credenciais inválidas.", code='authorization')

        # Verificar senha
        if not user.check_password(password):
            raise serializers.ValidationError("Credenciais inválidas.", code='authorization')

        # Verificar email confirmado
        try:
            profile = user.profile
            if not profile.email_verified:
                raise serializers.ValidationError(
                    "Confirme seu email antes de entrar. Verifique sua caixa de entrada.",
                    code='authorization'
                )
        except UserProfile.DoesNotExist:
            pass  # Usuários antigos sem profile podem logar

        attrs['username'] = user.username
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
