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
    almoco = models.BooleanField(default=False)
    tempo_ate_pausar = models.CharField(null= True,blank=True, max_length=100)
    inicio_pausa = models.DateTimeField(null=True, blank=True)
    termo_pausa = models.DateTimeField(null=True, blank=True)
    bo_ja_em_pausa = models.BooleanField(default=False)
    turno_manha = models.BooleanField(default=True)

    

    def calcular_tempo_decorrido_bo(self):
        bo_funcionario = BackOfficeDiario.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        for bo in bo_funcionario:
            if bo.inicio and bo.fim:
                tempo_total += (bo.fim - bo.inicio)      
        return formatted_time(tempo_total)
    
    
    def calcular_tempo_ate_aviso(self): 
        try:
            bo = BackOffice.objects.get(funcionario=self.funcionario, aprovado=True)
            if bo.inicio and not bo.pausa and not bo.inicio_pausa:
                tempo_decorrido = timezone.now() - bo.inicio
                if tempo_decorrido > timedelta(minutes=1):
                    return True
                else:
                    return False
            elif bo.inicio and not bo.pausa and bo.inicio_pausa:
                tempo_acumulado = bo.tempo_ate_pausar
                tempo_acumulado_formated = parse_formatted_time(tempo_acumulado)
                tempo_decorrido = (timezone.now() - bo.inicio) + tempo_acumulado_formated
                if tempo_decorrido > timedelta(minutes=1):
                    return True
                else:
                    return False

        except:
            return False
    
    def calcular_tempo_bo_ao_segundo(self):       
        if self.inicio and not self.pausa and not self.inicio_pausa:
            tempo_decorrido = timezone.now() - self.inicio
            return formatted_time(tempo_decorrido)
        elif self.pausa:
                return self.tempo_ate_pausar
        elif self.inicio and not self.pausa and self.inicio_pausa:
            tempo_acumulado = self.tempo_ate_pausar
            tempo_acumulado_formated = parse_formatted_time(tempo_acumulado)
            tempo_decorrido = (timezone.now() - self.inicio) + tempo_acumulado_formated
            return formatted_time(tempo_decorrido)
        return "00:00:00"


    
    def calcular_tempo_decorrido_aprovacao(self):
        if self.aprovado and self.data_aprovacao:
            agora = timezone.now()
            tempo_decorrido = agora - self.data_aprovacao  
            return formatted_time(tempo_decorrido)

    def pausar_bo(self,isPAuse):
        is_pause = str(isPAuse).lower() == 'true'
        if is_pause:
            self.pausa = True
            print(f"{self.funcionario.nome} pausou back office")
        else:
            self.almoco = True
            self.pausa = True
            print(f"{self.funcionario.nome} pausou back office para almoço")
        self.inicio_pausa = timezone.now()
        self.save()
        if self.tempo_ate_pausar:
            tempo_decorrido = self.inicio_pausa - self.inicio
            pausa_acumulada = parse_formatted_time(self.tempo_ate_pausar)
            total = tempo_decorrido + pausa_acumulada
            self.tempo_ate_pausar = formatted_time(total)
            self.save()
        else:
            tempo_decorrido = self.inicio_pausa - self.inicio
            self.tempo_ate_pausar = formatted_time(tempo_decorrido)
            self.save()
        BackOfficeDiario.objects.create(funcionario=self.funcionario, inicio=self.inicio,
                                        fim=self.inicio_pausa)

    def despausar_bo(self):
        if not self.bo_ja_em_pausa:
            self.inicio = timezone.now()
            self.termo_pausa = timezone.now()
            self.pausa = False
            self.bo_ja_em_pausa = False
            self.almoco = False
            self.save()
        else:
            self.bo_ja_em_pausa = False
            self.save()

    








    
    
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
        return formatted_time(tempo_total)
    
    def __str__(self) -> str:
        return f"BO-{self.funcionario}- Inicio: {self.inicio} - Fim: {self.fim}"


class BackOfficeFilaEspera(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(default=timezone.now)


    def calcular_tempo_decorrido_entrada_fila_bo(self):
        pausas = BackOfficeFilaEspera.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        hora_atual = timezone.now()
        for pausa in pausas:
            if pausa.data_entrada:
                tempo_total += (hora_atual - pausa.data_entrada)     
        return formatted_time(tempo_total)

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
    capacidade_maxima = models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima_BO = {self.capacidade_maxima}"



class BackofficeConfigTarde_BO(models.Model):
    capacidade_maxima = models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima_BO_tarde = {self.capacidade_maxima}"
    



def formatted_time(time):
    if time is None:
        return "00:00:00"
    total_seconds = time.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
    return formatted


def parse_formatted_time(formatted_time):
    hours, minutes, seconds = map(int, formatted_time.split(":"))
    time_delta = timedelta(hours=hours, minutes=minutes,seconds=seconds)
    return time_delta