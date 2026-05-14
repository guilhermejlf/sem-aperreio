from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        family = None
        try:
            family = user.family_memberships.first().family
            family_name = family.name
            family_id = family.id
        except Exception:
            family_name = None
            family_id = None

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined.isoformat() if user.date_joined else None,
            "family": {
                "id": family_id,
                "name": family_name,
            } if family_name else None,
        })

    def patch(self, request):
        user = request.user
        data = request.data

        first_name = data.get('first_name')
        username = data.get('username')

        if first_name is not None:
            user.first_name = first_name.strip()

        if username is not None:
            username = username.strip()
            if username != user.username and User.objects.filter(username=username).exists():
                return Response(
                    {"erro": "Este nome de usuário já está em uso."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.username = username

        user.save()

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data

        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            return Response(
                {"erro": "Todos os campos são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {"erro": "Senha atual incorreta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"erro": "As senhas não coincidem."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {"erro": "A senha deve ter pelo menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not any(c.isupper() for c in new_password):
            return Response(
                {"erro": "A senha deve conter pelo menos uma letra maiúscula."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not any(c.islower() for c in new_password):
            return Response(
                {"erro": "A senha deve conter pelo menos uma letra minúscula."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not any(c.isdigit() for c in new_password):
            return Response(
                {"erro": "A senha deve conter pelo menos um número."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not any(c in '@!#$%^&*()_+-=[]{}|;:,.<>?' for c in new_password):
            return Response(
                {"erro": "A senha deve conter pelo menos um caractere especial."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({"mensagem": "Senha alterada com sucesso!"})
