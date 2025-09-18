from django.db import models
from django.db.models import Q
from apps.indicador.models import FrontOfficeNPS, BackOfficeNPS
from django.utils import timezone
from apps.usuarios.models import Usuario
class TipoIqs(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name


from django.db import models
from django.utils import timezone
from django.db.models import Q

class Iqs(models.Model):
    tipo = models.ForeignKey(TipoIqs, on_delete=models.PROTECT)
    data = models.DateField(default=timezone.now)
    funcionario = models.ForeignKey(Usuario, on_delete=models.PROTECT)



    @classmethod
    def calcular_taxa_resposta_geral(cls, funcionario, mes=None, ano=None):
        if ano is None and mes is None:
            mes = timezone.now().month
            ano = timezone.now().year
        iqs = cls.objects.filter(
            Q(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0]) | Q(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0]),
            data__month=mes,
            data__year=ano
        ).count()
        total_iqs_respondidos = (
            FrontOfficeNPS.objects.filter(data__month=mes, data__year=ano, funcionario=funcionario).count()
            + BackOfficeNPS.objects.filter(data__month=mes, data__year=ano, funcionario=funcionario).count()
        )
        return round((iqs / total_iqs_respondidos * 100) if total_iqs_respondidos > 0 else 0, 2)

    @classmethod
    def calcular_taxa_resposta_BO(cls, funcionario):
        ano = timezone.now().year
        mes = timezone.now().month
        iqs = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_iqs_respondidos = BackOfficeNPS.objects.filter(data__month=mes, data__year=ano).count()
        return round((iqs / total_iqs_respondidos * 100) if total_iqs_respondidos > 0 else 0,2)

    @classmethod
    def calcular_taxa_resposta_FO(cls, funcionario, mes=None, ano=None):
        if ano is None:
            ano = timezone.now().date().year
            mes = timezone.now().date().month
        iqs = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_iqs_respondidos = FrontOfficeNPS.objects.filter(data__month=mes, data__year=ano).count()
        return round((iqs / total_iqs_respondidos * 100) if total_iqs_respondidos > 0 else 0,2)

    @classmethod
    def calcular_taxa_transferencia_fo(cls, funcionario, mes=None, ano=None):
        if ano is None and mes is None:
            ano = timezone.now().year
            mes = timezone.now().month
        total_iqs_transferidos_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_nao_transferido_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_chamadas = total_iqs_transferidos_fo + total_nao_transferido_fo
        return round((total_iqs_transferidos_fo / total_chamadas * 100) if total_chamadas > 0 else 0,2)

    @classmethod
    def calcular_taxa_transferencia_bo(cls, funcionario):
        ano = timezone.now().year
        mes = timezone.now().month
        total_iqs_transferidos_bo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida BO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_nao_transferidos_bo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida BO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_processados = total_iqs_transferidos_bo + total_nao_transferidos_bo
        return round((total_iqs_transferidos_bo / total_processados * 100) if total_processados > 0 else 0,2)

    @classmethod
    def calcular_previsao_para_objetivo_fo(cls, funcionario):
        mes = timezone.now().date().month
        ano = timezone.now().date().year
        total_iqs_transferidos_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0],data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_nao_transferidos_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0],data__month=mes, data__year=ano, funcionario=funcionario).count()
        return total_iqs_transferidos_fo - (total_nao_transferidos_fo * 4)

    @classmethod
    def calcular_previsao_para_objetivo_bo(cls, funcionario):
        data = timezone.now()
        mes = data.month
        ano = data.year
        total_iqs_transferidos_bo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        total_nao_transferidos_bo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida FO')[0], data__month=mes, data__year=ano, funcionario=funcionario).count()
        return (total_iqs_transferidos_bo - (total_nao_transferidos_bo * 0.68)) // 1
    @classmethod
    def calcular_taxa_dia_fo(cls, funcionario):
        data = timezone.now().date()
        total_iqs_transferidos_fo = cls.objects.filter(tipo= TipoIqs.objects.get_or_create(name='Transferida FO')[0],data=data, funcionario=funcionario).count()
        total_nao_transferidos_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0], funcionario=funcionario, data=data).count()
        total_chamadas = total_iqs_transferidos_fo + total_nao_transferidos_fo
        return round((total_iqs_transferidos_fo / total_chamadas * 100) if total_chamadas > 0 else 0,2)
    @classmethod
    def calcular_taxa_dia_bo(cls, funcionario):
        data = timezone.now().date()
        total_iqs_transferidos_fo = cls.objects.filter(tipo= TipoIqs.objects.get_or_create(name='Transferida BO')[0],data=data, funcionario=funcionario).count()
        total_nao_transferidos_fo = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0], funcionario=funcionario, data=data).count()
        total_chamadas = total_iqs_transferidos_fo + total_nao_transferidos_fo
        return round((total_iqs_transferidos_fo / total_chamadas * 100) if total_chamadas > 0 else 0,2)
    @classmethod
    def calcular_quantidade_transferido_dia_fo(cls, funcionario, data=None):
        if data is None:
            data = timezone.now().date()
        return cls.objects.filter(tipo= TipoIqs.objects.get_or_create(name='Transferida FO')[0],data=data, funcionario=funcionario).count()

    @classmethod
    def calcular_quantidade_nao_transferido_dia_fo(cls, funcionario, data=None):   
        if data is None:
            data = timezone.now().date() 
        numero = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0], funcionario=funcionario, data=data).count()
        return numero
    
    @classmethod
    def calcular_quantidade_transferido_dia_bo(cls, funcionario, data=None):
        if data is None:
            data = timezone.now().date()
        return cls.objects.filter(tipo= TipoIqs.objects.get_or_create(name='Transferida BO')[0],data=data, funcionario=funcionario).count()

    @classmethod
    def calcular_quantidade_nao_transferido_dia_bo(cls, funcionario, data=None):   
        if data is None:
            data = timezone.now().date() 
        numero = cls.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0], funcionario=funcionario, data=data).count()
        return numero

    def __str__(self):
        return f"{self.funcionario} - {self.tipo} - {self.data}"