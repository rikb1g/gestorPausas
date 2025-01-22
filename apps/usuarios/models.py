from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.PROTECT)
    turno_manha = models.BooleanField(default=True)

    def __str__(self):
        return self.nome







