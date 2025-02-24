from django.db import models
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from apps.usuarios.models import Usuario



class NPS(models.Model):
    funcionario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    data = models.DateField()
    nota= models.IntegerField(validators=[MinValueValidator(0)])
    interacao = models.CharField(max_length=50,blank=True, null=True)
    def calculo_nps_mes(self,mes):
        detrator = self.calculo_detratores_mes(mes)
        neutro = self.calculo_neutros_mes(mes)
        promotor= self.calculo_promotores_mes(mes)
        nps = calculo_nps(promotor,detrator,neutro)
        nps = calculo_nps(promotor,detrator,neutro)
        return nps
    
    def calculo_nps_global_mes(self,mes):
        detrator_FO = FrontOfficeNPS.objects.filter(nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=timezone.now().year -1).count()
        detrator_BO = BackOfficeNPS.objects.filter(nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=timezone.now().year -1).count()
        detrator = detrator_FO + detrator_BO
        neutro_FO = FrontOfficeNPS.objects.filter(nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=timezone.now().year -1).count()
        neutro_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=timezone.now().year -1).count()
        neutro = neutro_FO + neutro_BO
        promotor_FO = FrontOfficeNPS.objects.filter(nota__gte=9,nota__lte=10,
                                      data__month=mes,data__year=2024).count()
    
        promotor_BO = BackOfficeNPS.objects.filter(nota__gte=9,nota__lte=10, 
                                      data__month=mes,data__year=2024).count()
        promotor= promotor_FO + promotor_BO
        nps = calculo_nps(promotor,detrator,neutro)
        return nps

    def calculo_promotores_mes(self,mes):
        promotor_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=8,nota__lt=11,
                                      data__month=mes,data__year=2024).count()
        promotor_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=8,nota__lt=11, 
                                      data__month=mes,data__year=2024).count()
        promotor= promotor_FO + promotor_BO
        return promotor
    def calculo_neutros_mes(self,mes):
        neutro_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=timezone.now().year -1).count()
        neutro_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gt=6,nota__lt=9,
                                    data__month=mes,data__year=timezone.now().year -1).count()
        neutro = neutro_FO + neutro_BO
        return neutro
        
    def calculo_detratores_mes(self,mes):
        detrator_FO = FrontOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=timezone.now().year -1).count()
        detrator_BO = BackOfficeNPS.objects.filter(funcionario=self.funcionario,nota__gte=0,nota__lt=7,
                                      data__month=mes, data__year=timezone.now().year -1).count()
        detrator = detrator_FO + detrator_BO
        return detrator



    
class BackOfficeNPS(NPS):
    class Meta:
        verbose_name = "BackOffice NPS"
        verbose_name_plural = "BackOffice NPS"
    
    def calculo_nps_FO(self):
        pass




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
    data = models.DateField(auto_now_add=True, blank=True, null=True)


    def calculo_nps(self):
        total = self.promotores + self.detratores + self.neutros
        if total == 0:
            return 0
        else:
            nps = (self.promotores - self.detratores) / total
        return round(nps * 100,2)

    def __str__(self):
        return f"{self.funcionario} nps de {self.data.month}" #self.funcionario
    
class ExcelFile(models.Model):
    nome = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to="uploads/")
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome