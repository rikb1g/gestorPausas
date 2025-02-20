from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Pausa, FilaEspera, ConfiguracaoPausa, ConfiguracaoPausa2
from apps.usuarios.models import Usuario




@receiver(post_save, sender=Pausa)
@receiver(post_save, sender=ConfiguracaoPausa)
@receiver(post_save, sender=ConfiguracaoPausa2)
@receiver(post_delete, sender=Pausa)
@receiver(post_delete, sender=FilaEspera)
def autorizar_proximo_intervalo(sender, instance, **kwargs):
    config = ConfiguracaoPausa.objects.last() or ConfiguracaoPausa.objects.create(capacidade_maxima=0)
    config2 = ConfiguracaoPausa2.objects.last() or ConfiguracaoPausa2.objects.create(capacidade_maxima=0)

    num_intervalos_maximos1 = config.capacidade_maxima
    num_intervalos_maximos2 = config2.capacidade_maxima

    num_intervalos_autorizados1 = Pausa.objects.filter(aprovado=True, ja_utilizou_pausa=False).count()
    num_intervalos_autorizados2 = Pausa.objects.filter(aprovado=True, ja_utilizou_pausa=True).count()

    funcionarios_primeira_pausa = Usuario.objects.filter(ja_utilizou_pausa=False)
    funcionarios_segunda_pausa = Usuario.objects.filter(ja_utilizou_pausa=True)


    while num_intervalos_autorizados1 < num_intervalos_maximos1:
        proximo = FilaEspera.objects.filter(funcionario__in=funcionarios_primeira_pausa).order_by('data_entrada').first()
        if not proximo:
            break
        pausa_existente = Pausa.objects.filter(funcionario= proximo.funcionario, aprovado=True, ja_utilizou_pausa=False).exists()

        if pausa_existente:
            proximo.delete()
        else:
            Pausa.objects.create(funcionario=proximo.funcionario, aprovado=True,data_aprovacao= timezone.now(),ja_utilizou_pausa=False)
            proximo.delete()
            num_intervalos_autorizados1 += 1
            print("Pausa autorizada e removido da fila")
        num_intervalos_autorizados1 = Pausa.objects.filter(aprovado=True, ja_utilizou_pausa=False).count()


    while num_intervalos_autorizados2 < num_intervalos_maximos2:
        proximo = FilaEspera.objects.filter(funcionario__in=funcionarios_segunda_pausa).order_by('data_entrada').first()
        if not proximo:
            break
        pausa_existente = Pausa.objects.filter(funcionario= proximo.funcionario, aprovado=True, ja_utilizou_pausa=True).exists()

        if pausa_existente:
            proximo.delete()
        else:
            Pausa.objects.create(funcionario=proximo.funcionario, aprovado=True,data_aprovacao= timezone.now(),ja_utilizou_pausa=True)
            proximo.delete()
            num_intervalos_autorizados2 += 1
            print("Pausa autorizada e removido da fila")
        num_intervalos_autorizados2 = Pausa.objects.filter(aprovado=True, ja_utilizou_pausa=True).count()



        