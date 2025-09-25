from datetime import datetime
from django.db.models import Count
from django.db import transaction
import sys
import os
from django.utils import timezone




sys.path.append('/home/rikb1g/gestorPausas')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intervalos.settings')

# Configura o Django
import django
django.setup()

from apps.pausas.models import Pausa, PausasDiarias,ConfiguracaoPausa, FilaEspera, ConfiguracaoPausa2
from apps.backoffice.models import BackOffice, BackofficeConfig, BackOfficeDiario, BackOfficeFilaEspera,BackofficeConfigTarde_BO
from apps.usuarios.models import Usuario
from apps.indicador.models import NPS
from apps.iqs.models import Iqs


def delete_old_data():
    try:
        users = Usuario.objects.all()
        for user in users:
            user.ja_utilizou_pausa = False
            user.ultrapassou_tempo_bo = False

            user.save()
    except  Exception as e:
        print(f"{e}")
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
            configuracao.capacidade_maxima = 1
            configuracao.save()
        else:
            ConfiguracaoPausa.objects.create(capacidade_maxima=1)
    except  Exception as e:
        print(f"{e}")
    try:
        configuracao_2 = ConfiguracaoPausa2.objects.last()
        if configuracao_2:
            configuracao_2.capacidade_maxima = 0
            configuracao_2.save()
        else:
            ConfiguracaoPausa2.objects.create(capacidade_maxima=1)
    except  Exception as e:
        print(f"{e}")
    try: 
        configuracao_tarde = BackofficeConfigTarde_BO.objects.last()
        if configuracao_tarde:
            configuracao_tarde.capacidade_maxima = 0
            configuracao_tarde.save()
        else:
            BackofficeConfigTarde_BO.objects.create(capacidade_maxima=0)
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

    try:
        backoffice = BackOffice.objects.all()
        for bo in backoffice:
            bo.delete()
    except  Exception as e:
        print(f"{e}")


delete_old_data()

def eliminar_interacoes_duplicadas(
    confirm=False,
    dry_run=True,
    keep='first',
    chunk_size=1000,
    ignore_null_interacao=False
        ):
    
    qs_values = ["funcionario", "data", "nota", "interacao"]
    qs = (
        NPS.objects
        .values(*qs_values)
        .annotate(total=Count("id"))
        .filter(total__gt=1)
    )

    if ignore_null_interacao:
        qs = qs.exclude(interacao__isnull=True)

    total_a_apagar = 0
    to_delete_ids = []

    for d in qs:
        filtro = {
            "funcionario": d["funcionario"],
            "data": d["data"],
            "nota": d["nota"],
            "interacao": d["interacao"],
        }
        order = "id" if keep == "first" else "-id"
        group_qs = NPS.objects.filter(**filtro).order_by(order)
        ids = list(group_qs.values_list("id", flat=True))
        ids_para_apagar = ids[1:]  # mantém o primeiro ou último

        if ids_para_apagar:
            print(
                f"Grupo: {filtro} -> apagaria {len(ids_para_apagar)} ids: "
                f"{ids_para_apagar[:10]}{'...' if len(ids_para_apagar) > 10 else ''}"
            )
            if confirm and not dry_run:
                NPS.objects.filter(id__in=ids_para_apagar).delete()
                print(
                    f"Grupo: {filtro} -> apagou {len(ids_para_apagar)} ids: "
                    f"{ids_para_apagar[:10]}{'...' if len(ids_para_apagar) > 10 else ''}"
                )
            total_a_apagar += len(ids_para_apagar)
            to_delete_ids.extend(ids_para_apagar)

    print(f"Total a apagar (estimado): {total_a_apagar}")

    if dry_run:
        print("Dry run ativo — nada foi apagado.")
        return total_a_apagar

    if not confirm:
        print("Passa confirm=True e dry_run=False para apagar de verdade.")
        return total_a_apagar

    # efetuar as deleções em transação e em chunks
    with transaction.atomic():
        deleted = 0
        for i in range(0, len(to_delete_ids), chunk_size):
            chunk = to_delete_ids[i:i + chunk_size]
            NPS.objects.filter(id__in=chunk).delete()
            deleted += len(chunk)
        print(f"Foram apagados aproximadamente {deleted} registos.")
    return deleted

from datetime import datetime, date
eliminar_interacoes_duplicadas(confirm=True, dry_run=True)

from datetime import date
from dateutil.relativedelta import relativedelta
def eliminar_iqs_mes_anterior():
    hoje = date.today()
    mes_anterior = hoje - relativedelta(months=1)

    ano = mes_anterior.year
    mes = mes_anterior.month

    # apaga apenas registos do mês anterior
    Iqs.objects.filter(data__year=ano, data__month=mes).delete()
    

eliminar_iqs_mes_anterior()

