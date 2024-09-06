from django.db import models
from django.urls import reverse
from apps.usuarios.models import Usuario
from django.utils import timezone

class Pausa(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    aprovado = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('lista_pausas')

    def __str__(self):
        return f"{self.funcionario.nome} - Inicio: {self.inicio} - Fim: {self.fim} - 'terminada'"
    
class PausasDiarias(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)


class FilaEspera(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'{self.funcionario.nome} - Entrada na fila: {self.data_entrada}'


class ConfiguracaoPausa(models.Model):
    capacidade_maxima = models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima = {self.capacidade_maxima}"


