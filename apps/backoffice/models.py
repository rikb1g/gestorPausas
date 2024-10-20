from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario
from datetime import timedelta


class BackOffice(models.Model):
    funcionario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    aprovado = models.BooleanField(default=False)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    pausa = models.BooleanField(default=False)
    

    def calcular_tempo_decorrido_bo(self):
        bo_funcionario = BackOfficeDiario.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        for bo in bo_funcionario:
            if bo.inicio and bo.fim:
                tempo_total += (bo.fim - bo.inicio)

        total_seconds = tempo_total.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
        return formatted
    
    def calcular_tempo_decorrido_aprovacao(self):
        if self.aprovado and self.data_aprovacao:
            agora = timezone.now()
            tempo_decorrido = agora - self.data_aprovacao
            total_seconds = tempo_decorrido.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder,60)
            formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"   
            return formatted
    
    def get_absolute_url(self):
        return reverse('lista_pausas')

    def __str__(self):
        return f"BO-{self.funcionario.nome} - Inicio: {self.inicio} - Fim: {self.fim} - 'terminada'"
    

class BackOfficeDiario(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)

    @classmethod
    def calcular_tempo_decorrido_bo(cls,funcionario):
        bo_funcionario = BackOfficeDiario.objects.filter(funcionario=funcionario)
        tempo_total = timedelta()
        for bo in bo_funcionario:
            if bo.inicio and bo.fim:
                tempo_total += (bo.fim - bo.inicio)

        total_seconds = tempo_total.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
        return formatted
    
    def __str__(self) -> str:
        return f"BO-{self.funcionario}- Inicio: {self.inicio} - Fim: {self.fim}"


class BackOfficeFilaEspera(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(default=timezone.now())

    def calcular_tempo_decorrido_entrada_fila_bo(self):
        pausas = BackOfficeFilaEspera.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        hora_atual = timezone.now()
        for pausa in pausas:
            if pausa.data_entrada:
                tempo_total += (hora_atual - pausa.data_entrada)

        total_seconds = tempo_total.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
        return formatted

    def calcular_tempo_decorrido_bo(self):
        bo_funcionario = BackOfficeDiario.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        for bo in bo_funcionario:
            if bo.inicio and bo.fim:
                tempo_total += (bo.fim - bo.inicio)

        total_seconds = tempo_total.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
        return formatted

    def __str__(self):
        return f'BO-{self.funcionario.nome} - Entrada na fila: {self.data_entrada}'
    
class BackofficeConfig(models.Model):
    capacidade_maxima= models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima_BO = {self.capacidade_maxima}"