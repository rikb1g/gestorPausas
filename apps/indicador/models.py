from django.db import models
from django.utils import timezone
from django.db import models
from django.db.models import Count
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
    data = models.DateField(auto_now_add=True, blank=True, null=True)



    def atualizar_nps(self,mes,ano=None):
        if ano is None:
            ano = timezone.now().year
        dados_nps = NPS.objects.filter(funcionario=self.funcionario
                                       ,data__month=mes,data__year=ano).values("nota").annotate(total=Count("nota"))
        promotores = sum(item["total"] for item in dados_nps if item["nota"] >=9)
        neutros = sum(item["total"] for item in dados_nps if item["nota"] >6 and item["nota"] < 9)
        detratores = sum(item["total"] for item in dados_nps if item["nota"] >=0 and item["nota"] < 7)

        historico , created = HistoricoNPS.objects.get_or_create(
            funcionario=self.funcionario,
            data__month=mes,
            data__year=ano,
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
    

