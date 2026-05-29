import secrets
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.utils import timezone

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
        identifier = attrs.get('identifier') or attrs.get('username', '')
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

        # Verificar email
        try:
            profile = user.profile
            if not profile.email_verified:
                raise serializers.ValidationError(
                    "Confirme seu email antes de entrar. Verifique sua caixa de entrada.",
                    code='email_not_verified'
                )
        except UserProfile.DoesNotExist:
            pass

        attrs['username'] = user.username
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Mapear identifier -> username para compatibilidade com o serializer base
        data = request.data.copy()
        if 'identifier' in data:
            data['username'] = data.pop('identifier')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"erro": "Token não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = UserProfile.objects.get(verification_token=token)
            if profile.verification_token_expires and profile.verification_token_expires < timezone.now():
                return Response({"erro": "Token expirado."}, status=status.HTTP_400_BAD_REQUEST)

            profile.email_verified = True
            profile.verification_token = None
            profile.verification_token_expires = None
            profile.save()

            return Response({"mensagem": "Email confirmado com sucesso! Você já pode fazer login."})
        except UserProfile.DoesNotExist:
            return Response({"erro": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('identifier') or request.data.get('email')
        if not identifier:
            return Response({"erro": "Informe seu email ou usuário."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            return Response({"mensagem": "Se o usuário existir, você receberá um email de verificação."})

        try:
            profile = user.profile
            if profile.email_verified:
                return Response({"mensagem": "Este email já foi confirmado. Você pode fazer login."})

            # Gerar novo token
            token = secrets.token_urlsafe(32)
            profile.verification_token = token
            profile.verification_token_expires = timezone.now() + timedelta(hours=48)
            profile.save()

            from django.conf import settings
            verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
            from .tasks import send_email
            try:
                send_email(
                    subject="Confirme seu email - Sem Aperreio",
                    to_email=user.email,
                    template_name="email_verification",
                    context={"user": user, "verify_url": verify_url}
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Falha ao reenviar email de verificação para {user.email}: {e}")

            return Response({"mensagem": "Email de verificação reenviado! Verifique sua caixa de entrada."})
        except UserProfile.DoesNotExist:
            return Response({"mensagem": "Se o usuário existir, você receberá um email de verificação."})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"erro": "Email não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.reset_token = token
            profile.reset_token_expires = timezone.now() + timedelta(hours=24)
            profile.save()

            from django.conf import settings
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            from .tasks import send_email
            try:
                send_email(
                    subject="Redefinição de senha - Sem Aperreio",
                    to_email=user.email,
                    template_name="password_reset",
                    context={"user": user, "reset_url": reset_url}
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Falha ao enviar email de reset para {user.email}: {e}")
        except User.DoesNotExist:
            pass  # Não revelar se email existe

        return Response({"mensagem": "Se o email estiver cadastrado, você receberá um link de redefinição."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response({"erro": "Token e nova senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = UserProfile.objects.get(reset_token=token)
            if profile.reset_token_expires and profile.reset_token_expires < timezone.now():
                return Response({"erro": "Token expirado."}, status=status.HTTP_400_BAD_REQUEST)

            # Validar força da senha
            if len(new_password) < 8:
                return Response({"erro": "A senha deve ter pelo menos 8 caracteres."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(c.isupper() for c in new_password):
                return Response({"erro": "A senha deve conter pelo menos uma letra maiúscula."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(c.islower() for c in new_password):
                return Response({"erro": "A senha deve conter pelo menos uma letra minúscula."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(c.isdigit() for c in new_password):
                return Response({"erro": "A senha deve conter pelo menos um número."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(c in '@!#$%^&*()_+-=[]{}|;:,.<>?' for c in new_password):
                return Response({"erro": "A senha deve conter pelo menos um caractere especial."}, status=status.HTTP_400_BAD_REQUEST)

            user = profile.user
            user.set_password(new_password)
            user.save()

            profile.reset_token = None
            profile.reset_token_expires = None
            profile.email_verified = True
            profile.save()

            return Response({"mensagem": "Senha redefinida com sucesso! Você já pode fazer login."})
        except UserProfile.DoesNotExist:
            return Response({"erro": "Token inválido."}, status=status.HTTP_400_BAD_REQUEST)


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


class OnboardingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile

        group_created = hasattr(user, 'membership') and user.membership is not None
        first_expense = user.gastos.exists()
        first_revenue = user.receitas.exists()
        first_goal = user.metas.exists()

        completed_count = sum([group_created, first_expense, first_revenue, first_goal])
        progress = int((completed_count / 4) * 100)

        return Response({
            "group_created": group_created,
            "first_expense": first_expense,
            "first_revenue": first_revenue,
            "first_goal": first_goal,
            "progress": progress,
            "completed": profile.onboarding_completed,
            "seen_family_tooltip": profile.seen_family_tooltip,
            "seen_budget_tooltip": profile.seen_budget_tooltip,
            "seen_bene_tooltip": profile.seen_bene_tooltip,
            "seen_statement_tooltip": profile.seen_statement_tooltip,
        })

    def post(self, request):
        user = request.user
        profile = user.profile
        action = request.data.get('action')

        if action == 'complete':
            profile.onboarding_completed = True
            profile.save()
            return Response({"mensagem": "Onboarding concluído."})

        if action == 'reset':
            profile.onboarding_completed = False
            profile.save()
            return Response({"mensagem": "Onboarding reiniciado."})

        if action == 'dismiss_tooltip':
            tooltip = request.data.get('tooltip')
            if tooltip == 'family':
                profile.seen_family_tooltip = True
            elif tooltip == 'budget':
                profile.seen_budget_tooltip = True
            elif tooltip == 'bene':
                profile.seen_bene_tooltip = True
            elif tooltip == 'statement':
                profile.seen_statement_tooltip = True
            profile.save()
            return Response({"mensagem": "Tooltip marcado como visto."})

        return Response({"erro": "Ação inválida."}, status=status.HTTP_400_BAD_REQUEST)
