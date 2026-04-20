from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "nome",
        "eh_admin",
        "esta_ativo",
        "criado_em",
    )
    list_filter = ("eh_admin", "esta_ativo", "criado_em")
    search_fields = ("email", "nome")
    ordering = ("-criado_em",)