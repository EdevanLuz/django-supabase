from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from .models import Usuario
from .services.supabase_auth import validar_token_supabase


class AutenticacaoSupabase(BaseAuthentication):
    def authenticate(self, request):
        cabecalho_autorizacao = request.headers.get("Authorization")

        if not cabecalho_autorizacao:
            return None

        if not cabecalho_autorizacao.startswith("Bearer "):
            return None

        token = cabecalho_autorizacao.split(" ", 1)[1].strip()

        if not token:
            return None

        try:
            payload = validar_token_supabase(token)
        except ValueError as exc:
            raise exceptions.AuthenticationFailed(str(exc)) from exc

        id_supabase = payload.get("sub")
        email = payload.get("email")
        metadados_usuario = payload.get("user_metadata") or {}
        nome = metadados_usuario.get("name")

        if not id_supabase:
            raise exceptions.AuthenticationFailed("Token sem identificador de usuário.")

        if not email:
            raise exceptions.AuthenticationFailed("Token sem e-mail do usuário.")

        usuario, _ = Usuario.objects.get_or_create(
            id_supabase=id_supabase,
            defaults={
                "email": email,
                "nome": nome,
            },
        )

        houve_alteracao = False

        if usuario.email != email:
            usuario.email = email
            houve_alteracao = True

        if nome and usuario.nome != nome:
            usuario.nome = nome
            houve_alteracao = True

        if houve_alteracao:
            usuario.save(update_fields=["email", "nome", "atualizado_em"])

        if not usuario.esta_ativo:
            raise exceptions.AuthenticationFailed("Usuário desativado.")

        return (usuario, payload)