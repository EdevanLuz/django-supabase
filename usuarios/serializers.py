from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "id_supabase",
            "email",
            "nome",
            "eh_admin",
            "esta_ativo",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = fields