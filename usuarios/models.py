from django.db import models


class Usuario(models.Model):
    id_supabase = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    eh_admin = models.BooleanField(default=False)
    esta_ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.email