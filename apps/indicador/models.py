from datetime import datetime
from django.db import models
from django.utils import timezone
from django.db import models
from django.db.models import Count,Sum
from django.core.validators import MinValueValidator
from apps.usuarios.models import Usuario



class NPS(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data = models.DateField()
    nota= models.IntegerField(validators=[MinValueValidator(0)])
    interacao = models.CharField(max_length=50,blank=True, null=True)
    def calculo_nps_mes(self,mes,ano):
        detrator = self.calculo_detratores_mes(mes,ano)
        neutro = self.calculo_neutros_mes(mes,ano)
        promotor= self.calculo_promotores_mes(mes,ano)
        nps = calculo_nps(promotor,detrator,neutro)
        nps = calculo_nps(promotor,detrator,neutro)
        return nps
    
    def calculo_nps_global_mes(self,mes,ano):
        detrator_FO = FrontOfficeNPS.objects.filter(nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=ano).count()
        detrator_BO = BackOfficeNPS.objects.filter(nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=ano).count()
        detrator = detrator_FO + detrator_BO
        neutro_FO = FrontOfficeNPS.objects.filter(nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=ano).count()
        neutro_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=ano).count()
        neutro = neutro_FO + neutro_BO
        promotor_FO = FrontOfficeNPS.objects.filter(nota__gte=9,nota__lte=10,
                                      data__month=mes,data__year=ano).count()
    
        promotor_BO = BackOfficeNPS.objects.filter(nota__gte=9,nota__lte=10, 
                                      data__month=mes,data__year=ano).count()
        promotor= promotor_FO + promotor_BO
        nps = calculo_nps(promotor,detrator,neutro)
        return nps

    def calculo_promotores_mes(self,mes,ano):
        promotor_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=8,nota__lt=11,
                                      data__month=mes,data__year=ano).count()
        promotor_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=8,nota__lt=11, 
                                      data__month=mes,data__year=ano).count()
        promotor= promotor_FO + promotor_BO
        return promotor
    def calculo_neutros_mes(self,mes,ano):
        neutro_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=ano).count()
        neutro_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=ano).count()
        neutro = neutro_FO + neutro_BO
        return neutro
        
    def calculo_detratores_mes(self,mes,ano):
        detrator_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=ano).count()
        detrator_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=ano).count()
        detrator = detrator_FO + detrator_BO
        return detrator
    
    

        
    def atualizar_nps(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        dados_nps = NPS.objects.filter(funcionario=self.funcionario
                                       ,data__month=mes,data__year=ano).values("nota").annotate(total=Count("nota"))
        if dados_nps:
            promotores = sum(item["total"] for item in dados_nps if item["nota"] >=9)
            neutros = sum(item["total"] for item in dados_nps if item["nota"] >6 and item["nota"] < 9)
            detratores = sum(item["total"] for item in dados_nps if item["nota"] >=0 and item["nota"] < 7)
            data_registo = datetime(ano, mes, 1)

            historico , created = HistoricoNPS.objects.get_or_create(
                funcionario=self.funcionario,
                    data = data_registo,
                    defaults={
                        "promotores": promotores,
                        "detratores": detratores,
                        "neutros": neutros,
                    },
                )
            if not created:
                historico.promotores = promotores
                historico.detratores = detratores
                historico.neutros = neutros
                historico.save()
        



    
class BackOfficeNPS(NPS):
    class Meta:
        verbose_name = "BackOffice NPS"
        verbose_name_plural = "BackOffice NPS"
    
    




class FrontOfficeNPS(NPS):
    class Meta:
        verbose_name = "FrontOffice NPS"
        verbose_name_plural = "FrontOffice NPS"
    

def calculo_nps(promotor,detrator,neutro):
    total = promotor + detrator + neutro
    if total == 0:
        return 0
    else:
        nps = (promotor - detrator) / total
    return round(nps * 100,2)

class HistoricoNPS(models.Model):
    funcionario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promotores = models.IntegerField()
    detratores = models.IntegerField()
    neutros = models.IntegerField()
    data = models.DateField()


    def calculo_nps_mensal(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        try:
            object_nps = HistoricoNPS.objects.get(funcionario=self.funcionario,data__month=mes,data__year=ano)
            promotores = object_nps.promotores
            detratores = object_nps.detratores
            neutros = object_nps.neutros
            return calculo_nps(promotores,detratores,neutros)
        except:
            return 0
        
    
    @staticmethod
    def calculo_nps_global_mensal_sup(mes,ano):
        try:
            promotores= HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(promotores=Sum('promotores'))
            detratores = HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(detratores=Sum('detratores'))
            neutros = HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(neutros=Sum('neutros'))
            promotores_total =promotores['promotores']
            detratores_total = detratores['detratores']
            neutros_total = neutros['neutros']
            return calculo_nps(promotores_total,detratores_total,neutros_total)
        except:
            return 0


    def calculo_nps_global_mensal(self,mes, ano=None):
        if ano is None:
            ano = timezone.now().year
        try:
            promotores = HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(promotores=Sum('promotores'))
            detratores = HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(detratores=Sum('detratores'))
            neutros = HistoricoNPS.objects.filter(data__month=mes,data__year=ano).aggregate(neutros=Sum('neutros'))
            promotores_total =promotores['promotores']
            detratores_total = detratores['detratores']
            neutros_total = neutros['neutros']
            return calculo_nps(promotores_total,detratores_total,neutros_total)
        except:
            return 0
    @staticmethod
    def calculo_nps_mes_supervior(mes,ano,supervisor):
        if ano is None:
            ano = timezone.now().year
        try:
            elementos_equipa = Usuario.objects.filter(equipa=supervisor.equipa)
            promotores = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(promotores=Sum('promotores'))
            detratores = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(detratores=Sum('detratores'))
            neutros = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(neutros=Sum('neutros'))
            promotores_total =promotores['promotores']
            detratores_total = detratores['detratores']
            neutros_total = neutros['neutros']
            return calculo_nps(promotores_total,detratores_total,neutros_total)
        except:
            return 0
    @staticmethod
    def promotores_supervisor(mes,ano,supervisor):
        
        try:
            elementos_equipa = Usuario.objects.filter(equipa=supervisor.equipa)
            promotores = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(promotores=Sum('promotores'))
            promotores_total =promotores['promotores']
            return promotores_total
        except: 
            return 0
        

    @staticmethod
    def neutros_supervisor(mes,ano,supervisor):
        try:
            elementos_equipa = Usuario.objects.filter(equipa=supervisor.equipa)
            neutros = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(neutros=Sum('neutros'))
            neutros_total = neutros['neutros']  
            return neutros_total
        except:
            return 0
        
    @staticmethod
    def detratores_supervisor(mes,ano,supervisor):
        try:
            elementos_equipa = Usuario.objects.filter(equipa=supervisor.equipa)
            neutros = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(detratores=Sum('detratores'))
            detratores_total = neutros['detratores']
            return detratores_total
        except:
            return 0
        
    def calculo_nps_global_equipa(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        try:
            elementos_equipa = Usuario.objects.filter(equipa=self.funcionario.equipa)
            promotores = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(promotores=Sum('promotores'))
            detratores = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(detratores=Sum('detratores'))
            neutros = HistoricoNPS.objects.filter(funcionario__in=elementos_equipa,data__month=mes,data__year=ano).aggregate(neutros=Sum('neutros'))
            promotores_total =promotores['promotores']
            detratores_total = detratores['detratores']
            neutros_total = neutros['neutros']
            return calculo_nps(promotores_total,detratores_total,neutros_total)
        except:
            return 0
    
    def calculo_promotores_mes(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        return HistoricoNPS.objects.filter(funcionario=self.funcionario,data__month=mes,data__year=ano).count().promotores
    
    def calculo_neutros_mes(self,mes,ano=None):
        if  ano is None:
            ano = timezone.now().year
        return HistoricoNPS.objects.filter(funcionario=self.funcionario,data__month=mes,data__year=ano).count().neutros
    
    def calculo_detratores_mes(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        return HistoricoNPS.objects.filter(funcionario=self.funcionario,data__month=mes,data__year=ano).count().detratores

                               
        


    def calculo_nps(self):
        total = self.promotores + self.detratores + self.neutros
        if total == 0:
            return 0
        else:
            nps = (self.promotores - self.detratores) / total
        return round(nps * 100,2)

    def __str__(self):
        return f"{self.funcionario} nps de {self.data.month} de {self.data.year}"
    
class ExcelFile(models.Model):
    nome = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to="uploads/")
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data_upload} - {self.arquivo}" #self.nome
    

class Interlocutores(models.Model):
    at = models.CharField(max_length=100,default="")
    destinatarios = models.CharField(max_length=255,blank=True,null=True,default="")
    cc = models.CharField(max_length=255,blank=True,null=True,default="")

    def __str__(self):
        return self.at
    

