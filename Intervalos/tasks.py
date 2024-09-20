
from apps.pausas.models import Pausa, PausasDiarias,ConfiguracaoPausa, FilaEspera
from apps.backoffice.models import BackOffice, BackofficeConfig, BackOfficeDiario


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
        configuracao.capacidade_maxima = 0
        configuracao.save()
    backoffice = BackOffice.objects.all()
    for bo in backoffice:
        bo.delete()
    boconfig = BackofficeConfig.objects.last()
    if boconfig:
        boconfig.capacidade_maxima = 0
        boconfig.save()
    else:
        BackofficeConfig.objects.create(capacidade_maxima=0)


delete_old_data()