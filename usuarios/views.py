from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissoes import EstaAutenticado, IsAdmin
from .serializers import UsuarioSerializer


class MeuPerfilView(APIView):
    permission_classes = [EstaAutenticado]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

from usuarios.autenticacao import AutenticacaoSupabase
class PainelAdminView(APIView):
    authentication_classes = [AutenticacaoSupabase]
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response(
            {"mensagem": "Acesso liberado para administrador."},
            status=status.HTTP_200_OK,
        )
        
# usuarios/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .permissoes import EstaAutenticado


class TesteTokenView(APIView):
    permission_classes = [EstaAutenticado]

    def get(self, request):
        return Response(
            {
                "mensagem": "Token válido",
                "usuario": {
                    "id": request.user.id,
                    "id_supabase": request.user.id_supabase,
                    "email": request.user.email,
                    "nome": request.user.nome,
                    "eh_admin": request.user.eh_admin,
                },
                "payload_token": request.auth,
            },
            status=status.HTTP_200_OK,
        )