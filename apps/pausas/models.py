from django.db import models
from django.urls import reverse
from apps.usuarios.models import Usuario
from django.utils import timezone
from datetime import timedelta
from apps.backoffice.models import formatted_time, BackOffice


class Pausa(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)
    aprovado = models.BooleanField(default=False)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    pausa = models.BooleanField(default=False)
    ja_utilizou_pausa = models.BooleanField(default=False)


    def pedir_pausa(self):
        pausas_aceites = Pausa.objects.filter(aprovado=True)
        ja_teve_pausa = PausasDiarias.objects.filter(funcionario=self.funcionario).exists()
        tempo_total = timedelta()
        if ja_teve_pausa:
            for pausa in ja_teve_pausa:
                if pausa.inicio and pausa.fim:
                    tempo_total += (pausa.fim - pausa.inicio)
                return formatted_time(tempo_total)
            if tempo_total > timedelta(minutes=1):
                self.ja_utilizou_pausa = True
            else:
                self.ja_utilizou_pausa = False
        



    
    def calcular_tempo_ate_aviso(self):
        try:
            pausa = Pausa.objects.get(funcionario=self.funcionario, aprovado=True)
            print("encontrou pausa")
            if pausa.inicio:
                agora = timezone.now()
                tempo_decorrido = agora - pausa.inicio
                if tempo_decorrido > timedelta(minutes=20):
                    print("tempo decorrido")
                    return True
                else:
                    return False
        except:
            return False

    def calcular_tempo_decorrido_pausa(self):
        pausas = PausasDiarias.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        for pausa in pausas:
            if pausa.inicio and pausa.fim:
                tempo_total += (pausa.fim - pausa.inicio)


        return formatted_time(tempo_total)

    def calcular_tempo_desde_aprovacao(self):
        if self.aprovado and self.data_aprovacao:
            agora = timezone.now()
            tempo_decorrido = agora - self.data_aprovacao

            return formatted_time(tempo_decorrido)
        return "Pausa ainda não foi aprovada."

    def calcular_tempo_pausa_ao_segundo(self):
        if self.inicio and self.aprovado:
            tempo_decorrido = timezone.now() - self.inicio
            return formatted_time(tempo_decorrido)
        
    def iniciar_pausa(self):
        try:
            bo_funcionario = BackOffice.objects.get(funcionario=self.funcionario)
            if bo_funcionario.inicio and not bo_funcionario.pausa:
                bo_funcionario.pausar_bo('true')
                print(f"{bo_funcionario.funcionario} pediu pausa e bo foi pausado")
            elif bo_funcionario.inicio and bo_funcionario.pausa:
                bo_funcionario.bo_ja_em_pausa = True
                bo_funcionario.save()
                print(f"{bo_funcionario.funcionario} pediu pausa e ja estava com BO em pausa!")
        except:
            print(f"{self.funcionario} Pediu Pausa e não está em BO! ")
        self.inicio = timezone.now()
        self.save()

    def terminar_intervalo(self):
        try:
            bo_funcionario = BackOffice.objects.get(funcionario=self.funcionario)
            bo_funcionario.despausar_bo()
        except:
            print("Sem BO para despausar!")
        self.fim = timezone.now()
        self.save()
        PausasDiarias.objects.create(funcionario=self.funcionario, inicio=self.inicio, fim=self.fim)
             
        self.delete()

    


        
        



    def get_absolute_url(self):
        return reverse('lista_intervalos')

    def __str__(self):
        return f"{self.funcionario.nome} - Inicio: {self.inicio} - Fim: {self.fim} - 'terminada'"

class PausasDiarias(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    inicio = models.DateTimeField(null=True,blank=True)
    fim = models.DateTimeField(null=True, blank=True)

    @classmethod
    def calcular_tempo_decorrido(cls,funcionario):
        pausas = PausasDiarias.objects.filter(funcionario=funcionario)
        tempo_total = timedelta()
        for pausa in pausas:
            if pausa.inicio and pausa.fim:
                tempo_total += (pausa.fim - pausa.inicio)

        return formatted_time(tempo_total)



    def __str__(self) -> str:
        return f"{self.funcionario}- Inicio: {self.inicio} - Fim: {self.fim}"




class FilaEspera(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data_entrada = models.DateTimeField(default=timezone.now)

    def calcular_tempo_decorrido_entrada_fila(self):
        pausas = FilaEspera.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        hora_atual = timezone.now()
        for pausa in pausas:
            if pausa.data_entrada:
                tempo_total += (hora_atual - pausa.data_entrada)
        return formatted_time(tempo_total)

    def calcular_tempo_decorrido_pausa(self):
        pausas = PausasDiarias.objects.filter(funcionario=self.funcionario)
        tempo_total = timedelta()
        for pausa in pausas:
            if pausa.inicio and pausa.fim:
                tempo_total += (pausa.fim - pausa.inicio)
        return formatted_time(tempo_total)

    def __str__(self):
        return f'{self.funcionario.nome} - Entrada na fila: {self.data_entrada}'


class ConfiguracaoPausa(models.Model):
    capacidade_maxima = models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima = {self.capacidade_maxima}"
    
class ConfiguracaoPausa2(models.Model):
    capacidade_maxima = models.IntegerField()

    def __str__(self):
        return f"Capacidade_maxima = {self.capacidade_maxima}"





