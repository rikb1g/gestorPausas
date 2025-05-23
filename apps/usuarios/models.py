from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.PROTECT,null=True,blank=True)
    identificador = models.CharField(max_length=50,blank=True,null=True)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.PROTECT)
    turno_manha = models.BooleanField(default=True)
    ja_utilizou_pausa = models.BooleanField(default=False)
    quantidade_pausas = models.IntegerField(default=0)
    pausa_aceite = models.BooleanField(default=False)
    ultrapassou_tempo_bo = models.BooleanField(default=False)
    equipa = models.ForeignKey('Equipas',on_delete=models.PROTECT,blank=True,null=True)


    def is_supervisor(self):
        if self.tipo.tipo == "Supervisor":
            return True
        else:
            return False

    def is_ultrapassou_tempo_bo(self):
        if self.ultrapassou_tempo_bo:
            return True
        else:
            return False

    def __str__(self):
        return self.nome




class Equipas(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.ForeignKey(Usuario, on_delete=models.PROTECT,limit_choices_to={'tipo__tipo': "Supervisor"})

    def __str__(self):
        return self.nome
    







