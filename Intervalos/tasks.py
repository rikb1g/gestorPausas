from celery import shared_task
from apps.pausas.models import Pausa, PausasDiarias,ConfiguracaoPausa, FilaEspera



@shared_task
def delete_old_data():
    pausas = Pausa.objects.all()
    for pausa in pausas:
        print(pausa)
        pausa.delete()
    pausas_diarias= PausasDiarias.objects.all()
    for pausa in pausas_diarias:
        print("pausa_diaria")
        print(pausa)
        pausa.delete()
    fila = FilaEspera.objects.all()
    for pausa in fila:
        print("fila")
        print(pausa)
        pausa.delete()
    configuracao = ConfiguracaoPausa.objects.last()
    if configuracao:
        print("tem configuração")
        configuracao.capacidade_maxima = 1
        configuracao.save()