from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from apps.usuarios.models import Usuario
from .models import BackOffice, BackofficeConfig, BackOfficeFilaEspera, BackofficeConfigTarde_BO

@receiver(post_save, sender=BackOffice)
@receiver(post_save, sender=BackofficeConfig)
@receiver(post_delete, sender=BackOffice)
@receiver(post_delete, sender=BackOfficeFilaEspera)
def autorizar_proximo_bo(sender, instance, **kwargs):
    config_manha = BackofficeConfig.objects.last()
    config_tarde = BackofficeConfigTarde_BO.objects.last()
    try:
        turno = instance.funcionario.turno_manha
    except:
        print("não encontrou funcionario")

    funcionarios_manha = Usuario.objects.filter(turno_manha=True)
    funcionarios_tarde = Usuario.objects.filter(turno_manha=False)
    if turno:
        if not config_manha:
            BackofficeConfig.objects.create(capacidade_maxima=0)
            config_manha = BackofficeConfig.objects.last()

        num_maximo_bo_manha = config_manha.capacidade_maxima
        num_bo_manha_autorizado = BackOffice.objects.filter(aprovado=True, turno_manha=True).count()
        while num_bo_manha_autorizado < num_maximo_bo_manha:
            proximo = BackOfficeFilaEspera.objects.filter(fucionario__in=
                                                          funcionarios_manha).order_by('data_entrada').first()
            if not proximo:
                break
            bo_existente = BackOffice.objects.filter(funcionario = proximo.funcionario, aprovado=True).exists()
            if bo_existente:
                proximo.delete()
            else:
                BackOffice.objects.create(funcionario=proximo.funcionario, aprovado=True,data_aprovacao=timezone.now()
                                          ,turno_manha=True)
                proximo.delete()
            num_bo_manha_autorizado = BackOffice.objects.filter(aprovado=True, turno_manha=True).count()

    else:
        if not config_tarde:
            BackofficeConfigTarde_BO.objects.create(capacidade_maxima=0)
            config_tarde = BackofficeConfigTarde_BO.objects.last()

        num_maximo_bo_tarde = config_tarde.capacidade_maxima
        num_bo_tarde_autorizado = BackOffice.objects.filter(aprovado=True, turno_manha=False).count()
        while num_bo_tarde_autorizado < num_maximo_bo_tarde:
            proximo_tarde = BackOfficeFilaEspera.objects.filter(
                funcionario__in=funcionarios_tarde).order_by('data_entrada').first()
            if not proximo_tarde:
                break
            bo_existente_tarde = BackOffice.objects.filter(funcionario=proximo_tarde.funcionario, aprovado=True).exists()
            if bo_existente_tarde:
                proximo_tarde.delete()
            else:
                BackOffice.objects.create(funcionario=proximo_tarde.funcionario, aprovado=True,
                                          data_aprovacao=timezone.now(),turno_manha=False)
                proximo_tarde.delete()
            num_bo_tarde_autorizado = BackOffice.objects.filter(aprovado=True,turno_manha=False).count()
