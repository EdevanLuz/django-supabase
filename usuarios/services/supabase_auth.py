import requests
from jose import jwt
from jose.exceptions import JWTError

from django.conf import settings


_cache_jwks = None


def obter_chaves_publicas_supabase():
    global _cache_jwks

    if _cache_jwks is None:
        url_chaves = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        resposta = requests.get(url_chaves, timeout=10)
        resposta.raise_for_status()
        _cache_jwks = resposta.json()

    return _cache_jwks


def obter_chave_por_kid(kid: str):
    jwks = obter_chaves_publicas_supabase()

    for chave in jwks.get("keys", []):
        if chave.get("kid") == kid:
            return chave

    return None


def validar_token_supabase(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise ValueError("Não foi possível ler o cabeçalho do token.") from exc

    kid = header.get("kid")
    if not kid:
        raise ValueError("Token sem 'kid' no cabeçalho.")

    chave_publica = obter_chave_por_kid(kid)
    if not chave_publica:
        raise ValueError("Chave pública do token não encontrada.")

    try:
        payload = jwt.decode(
            token,
            chave_publica,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=f"{settings.SUPABASE_URL}/auth/v1",
        )
    except JWTError as exc:
        raise ValueError("Token inválido ou expirado.") from exc

    return payload