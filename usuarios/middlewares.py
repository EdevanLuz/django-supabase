# usuarios/middlewares.py

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .services.supabase_auth import validar_token
from .models import Usuario


class MiddlewareAutenticacaoSupabase(MiddlewareMixin):

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            request.usuario = None
            return

        try:
            token = auth_header.split(" ")[1]
            payload = validar_token(token)

            id_supabase = payload["sub"]
            email = payload.get("email")

            usuario, _ = Usuario.objects.get_or_create(
                id_supabase=id_supabase,
                defaults={"email": email}
            )

            request.usuario = usuario

        except Exception:
            return JsonResponse({"erro": "Token inválido"}, status=401)