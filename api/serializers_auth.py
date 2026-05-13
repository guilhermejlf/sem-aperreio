import secrets
import logging
import threading
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import UserProfile
from .tasks import send_email

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirmar senha")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuário já existe.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("A senha deve conter pelo menos uma letra minúscula.")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("A senha deve conter pelo menos um número.")
        if not any(c in '@!#$%^&*()_+-=[]{}|;:,.<>?' for c in value):
            raise serializers.ValidationError("A senha deve conter pelo menos um caractere especial.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        token = secrets.token_urlsafe(32)
        UserProfile.objects.create(
            user=user,
            email_verified=True,  # Auto-verified for testing
            verification_token=token,
            verification_token_expires=timezone.now() + timedelta(hours=48)
        )
        # Enviar email de verificação em background (não bloquear resposta)
        def _send_verification_email():
            try:
                from django.conf import settings
                verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
                send_email(
                    subject="Confirme seu email - Sem Aperreio",
                    to_email=user.email,
                    template_name="email_verification",
                    context={"user": user, "verify_url": verify_url}
                )
            except Exception as e:
                logger.error(f"Falha ao enviar email de verificação para {user.email}: {e}")

        threading.Thread(target=_send_verification_email, daemon=True).start()

        return user
