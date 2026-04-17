from rest_framework.permissions import BasePermission


class EstaAutenticado(BasePermission):
    message = "Autenticação obrigatória."

    def has_permission(self, request, view):
        usuario = request.user

        return bool(
            usuario
            and getattr(usuario, "is_authenticated", False)
            and getattr(usuario, "esta_ativo", False)
        )


class IsAdmin(BasePermission):
    message = "Apenas administradores podem acessar este recurso."

    def has_permission(self, request, view):
        usuario = request.user

        return bool(
            usuario
            and getattr(usuario, "is_authenticated", False)
            and getattr(usuario, "esta_ativo", False)
            and getattr(usuario, "eh_admin", False)
        )