from channels.layers import get_channel_layer
from asgiref.sync import  async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Pausa, FilaEspera


@receiver(post_save, sender=Pausa)
def notificar_proximo_na_fila(sender,instance,**kwargs):
    if instance.fim:
        proximo_fila = FilaEspera.objects.orderby('data_entrada').first()
        if proximo_fila:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{proximo_fila.funcionario.id}",
                {
                    'type': 'send_notification',
                    'message': "Seu intervalo já pode ser iniciado"
                }
            )
            proximo_fila.delete()