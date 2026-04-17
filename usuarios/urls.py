from django.urls import path

from .views import MeuPerfilView, PainelAdminView, TesteTokenView

urlpatterns = [
    path('me/', MeuPerfilView.as_view(), name='meu_perfil'),
    path('admin-painel/', PainelAdminView.as_view(), name='painel_admin'),
    path('teste-token/', TesteTokenView.as_view(), name='teste_token'),
]