from django.urls import path
from .views import prever_gasto, gastos, gasto_detail
from .views_auth import RegisterView, LoginView, RefreshView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("prever/", prever_gasto, name="prever_gasto"),
    path("gastos/", gastos, name="gastos_list"),
    path("gastos/<int:pk>/", gasto_detail, name="gasto_detail"),
]