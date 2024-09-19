
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Pausa, FilaEspera, ConfiguracaoPausa




@receiver(post_save, sender=Pausa)
@receiver(post_save, sender=ConfiguracaoPausa)
@receiver(post_delete, sender=Pausa)
@receiver(post_delete, sender=FilaEspera)
def autorizar_proximo_intervalo(sender, instance, **kwargs):
    config = ConfiguracaoPausa.objects.last()
    
    if config:
        num_intervalos_maximos = config.capacidade_maxima
    
        num_intervalos_autorizados = Pausa.objects.filter(aprovado=True).count()
        while num_intervalos_autorizados < num_intervalos_maximos:
            proximo = FilaEspera.objects.order_by('data_entrada').first()
            if proximo:
                # Cria uma nova pausa para o próximo da fila
                Pausa.objects.create(funcionario=proximo.funcionario, aprovado=True)
                proximo.delete()
                num_intervalos_autorizados += 1  
                print("Pausa autorizada e removido da fila")
            else:
                print("Não há mais funcionários na fila de espera")
                break
    else:
        ConfiguracaoPausa.objects.create(capacidade_maxima=0)
