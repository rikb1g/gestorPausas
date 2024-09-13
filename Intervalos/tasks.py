import sys
import os


sys.path.append('/home/rikb1g/gestorPausas')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intervalos.settings')

# Configura o Django
import django
django.setup()

from apps.pausas.models import Pausa, PausasDiarias,ConfiguracaoPausa, FilaEspera
from apps.backoffice.models import BackOffice, BackofficeConfig, BackOfficeDiario, BackOfficeFilaEspera


def delete_old_data():
    try:
        pausas = Pausa.objects.all()
        for pausa in pausas:
            print(pausa)
            pausa.delete()
    except  Exception as e:
        print(f"{e}")
    try:
        pausas_diarias= PausasDiarias.objects.all()
        for pausa in pausas_diarias:
            print("pausa_diaria")
            print(pausa)
            pausa.delete()
    except  Exception as e:
        print(f"{e}")
    try:
        fila = FilaEspera.objects.all()
        for pausa in fila:
            print("fila")
            print(pausa)
            pausa.delete()
    except  Exception as e:
        print(f"{e}")

    try:
        configuracao = ConfiguracaoPausa.objects.last()
        if configuracao:
            print("tem configuração")
            configuracao.capacidade_maxima = 0
            configuracao.save()
        else:
            ConfiguracaoPausa.objects.create(capacidade_maxima=0)
    except  Exception as e:
        print(f"{e}")
    try:
        backoffice = BackOffice.objects.all()
        for bo in backoffice:
            bo.delete()
    except  Exception as e:
        print(f"{e}")
    try:
        boconfig = BackofficeConfig.objects.last()
        if boconfig:
            boconfig.capacidade_maxima = 0
            boconfig.save()
        else:
            BackofficeConfig.objects.create(capacidade_maxima=0)
    except  Exception as e:
        print(f"{e}")
    
    try:
        bodiario = BackOfficeDiario.objects.all()
        for bo in bodiario:
            bo.delete()
    except Exception as e:
        print(f"{e}")

    try:
        bo_fila = BackOfficeFilaEspera.objects.all()
        for bo in bo_fila:
            bo.delete()
    except Exception as e:
        print(f"{e}")


delete_old_data()