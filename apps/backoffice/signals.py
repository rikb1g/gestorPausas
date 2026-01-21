from django.db.models.signals import post_save, post_delete
from django.db.models import Case, When, IntegerField
from django.dispatch import receiver
from django.utils import timezone
from django.apps import AppConfig
from apps.usuarios.models import Usuario
from .models import BackOffice, BackofficeConfig, BackOfficeFilaEspera, BackofficeConfigTarde_BO


class MinhaAppConfig(AppConfig):
    name = 'apps.backoffice'
    verbose_name = 'BackOffice'
    def ready(self):
        from .models import BackofficeConfigTerceiroBO
        if not BackofficeConfigTerceiroBO.objects.exists():
            BackofficeConfigTerceiroBO.objects.create(capacidade_maxima=0)




@receiver(post_save, sender=BackOffice)
@receiver(post_save, sender=BackofficeConfig)
@receiver(post_save, sender=BackofficeConfigTarde_BO)
@receiver(post_delete, sender=BackOffice)
@receiver(post_delete, sender=BackOfficeFilaEspera)
def autorizar_proximo_bo(sender, instance, **kwargs):
    config_manha = BackofficeConfig.objects.last()
    config_tarde = BackofficeConfigTarde_BO.objects.last()

    primeiro_bo = Usuario.objects.filter(ja_utilizou_bo=False)
    segundo_bo = Usuario.objects.filter(ja_utilizou_bo=True)
    if config_manha:
        num_maximo_bo_manha = config_manha.capacidade_maxima
        num_bo_autorizado_manha = BackOffice.objects.filter(funcionario__in=primeiro_bo, aprovado=True).count()
        print(f"Nº máximo de manha autorizados: {num_maximo_bo_manha}")
        print(f"Nº de BO manha aprovados: {num_bo_autorizado_manha}")
        while num_bo_autorizado_manha < num_maximo_bo_manha:
            proximo = BackOfficeFilaEspera.objects.filter(
                funcionario__in=primeiro_bo
                ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada').first()


            if not proximo:
                break
            bo_existente = BackOffice.objects.filter(funcionario= proximo.funcionario,aprovado=True).exists()
            if bo_existente:
                proximo.delete()
            else:
                if proximo.funcionario.ultrapassou_tempo_bo:
                    break
                else:
                    BackOffice.objects.create(funcionario=proximo.funcionario, aprovado=True,
                                              data_aprovacao=timezone.now())
                    proximo.delete()
            num_bo_autorizado_manha = BackOffice.objects.filter(funcionario__in=primeiro_bo, aprovado=True).count()
            
    else:
        BackofficeConfig.objects.create(capacidade_maxima=0)

    if config_tarde:
        num_maximo_bo_tarde= config_tarde.capacidade_maxima
        num_bo_autorizado_tarde= BackOffice.objects.filter(funcionario__in=segundo_bo,
                                                           aprovado=True).count()
        print(f"Nº máximo de BO tarde autorizados: {num_maximo_bo_tarde}")
        print(f"Nº de BO tarde autorizados: {num_bo_autorizado_tarde}")
        while num_bo_autorizado_tarde < num_maximo_bo_tarde:
            proximo_tarde = BackOfficeFilaEspera.objects.filter(
                funcionario__in=segundo_bo
                ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada').first()

            if not proximo_tarde:
                 break
            bo_existente_tarde= BackOffice.objects.filter(funcionario=proximo_tarde.funcionario,
                                                          aprovado=True).exists()
            if bo_existente_tarde:
                proximo_tarde.delete()
            else:
                if proximo_tarde.funcionario.ultrapassou_tempo_bo:
                    print("BO nao autorizado devido a ter tempo ultrapassado")
                    break
                else:
                    print("BO autorizado")
                    BackOffice.objects.create(funcionario=proximo_tarde.funcionario,
                                              aprovado=True,data_aprovacao=timezone.now())
                    proximo_tarde.delete()
            
            num_bo_autorizado_tarde = BackOffice.objects.filter(funcionario__in=segundo_bo,
                                                           aprovado=True).count()
    else:
        BackofficeConfigTarde_BO.objects.create(capacidade_maxima=0)


