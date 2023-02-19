from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TIPO_USUARIO(models.TextChoices):
    ADMIN = 'A', _('Admin')
    TECNICO = 'T', _('Tecnico')


class Usuario(models.Model):
    user = models.OneToOneField(
        User, related_name='usuarios', on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=1, choices=TIPO_USUARIO.choices)

    def __str__(self):
        return f'{self.user.username}'
