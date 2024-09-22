from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import BackOffice, BackofficeConfig, BackOfficeFilaEspera



@receiver(post_save, sender=BackOffice)
@receiver(post_save, sender=BackofficeConfig)
@receiver(post_delete, sender=BackOffice)
@receiver(post_delete, sender=BackOfficeFilaEspera)
def autorizar_proximo_bo(sender, instance, **kwargs):
    config = BackofficeConfig.objects.last()

    if config:
        num_maximo_bo = config.capacidade_maxima
        num_bo_autorizado = BackOffice.objects.filter(aprovado=True).count()
        while num_bo_autorizado < num_maximo_bo:
            proximo = BackOfficeFilaEspera.objects.order_by('data_entrada').first()
            if proximo:
                bo_existente = BackOffice.objects.filter(funcionario= proximo.funcionario, aprovado=True).exists()
                if bo_existente:
                    proximo.delete()
                else:
                    BackOffice.objects.create(funcionario=proximo.funcionario, aprovado=True,data_aprovacao=timezone.now())
                    proximo.delete()
                    num_bo_autorizado += 1
            else:
                break

    else:
        BackofficeConfig.objects.create(capacidade_maxima=0)