from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import prever_gasto, gastos, gasto_detail, dashboard, receitas, receita_detail, exportar_csv, exportar_xlsx, exportar_pdf, listar_metas, criar_meta, atualizar_meta, deletar_meta, extrato
from .views_auth import (
    RegisterView, LoginView, RefreshView, UserView,
    VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView
)
from .views_family import FamilyViewSet
from .views_profile import ProfileView, PasswordChangeView
from .views_notificacoes import healthcheck, healthcheck_detailed, notificacoes_status, trigger_tasks
from .views_ai import ai_chat

router = DefaultRouter()
router.register('family', FamilyViewSet, basename='family')

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("auth/user/", UserView.as_view(), name="user"),
    path("auth/verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("auth/password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("auth/password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password/", PasswordChangeView.as_view(), name="password_change"),
    path("prever/", prever_gasto, name="prever_gasto"),
    path("export/csv/", exportar_csv, name="exportar_csv"),
    path("export/xlsx/", exportar_xlsx, name="exportar_xlsx"),
    path("export/pdf/", exportar_pdf, name="exportar_pdf"),
    path("gastos/", gastos, name="gastos_list"),
    path("gastos/<int:pk>/", gasto_detail, name="gasto_detail"),
    path("dashboard/", dashboard, name="dashboard"),
    path("receitas/", receitas, name="receitas_list"),
    path("receitas/<int:pk>/", receita_detail, name="receita_detail"),
    path("extrato/", extrato, name="extrato"),
    path("metas/", listar_metas, name="listar_metas"),
    path("metas/criar/", criar_meta, name="criar_meta"),
    path("metas/<int:pk>/", atualizar_meta, name="atualizar_meta"),
    path("metas/<int:pk>/deletar/", deletar_meta, name="deletar_meta"),
    path("health/", healthcheck, name="healthcheck"),
    path("health/detailed/", healthcheck_detailed, name="healthcheck_detailed"),
    path("notificacoes/status/", notificacoes_status, name="notificacoes_status"),
    path("tasks/trigger/", trigger_tasks, name="trigger_tasks"),
    path("ai/chat/", ai_chat, name="ai_chat"),
    path("", include(router.urls)),
]