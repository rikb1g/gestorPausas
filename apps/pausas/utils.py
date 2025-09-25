from apps.pausas.models import Pausa, FilaEspera, PausasDiarias
from apps.backoffice.models import BackOffice, BackOfficeFilaEspera, BackOfficeDiario
from apps.iqs.models import Iqs
from apps.usuarios.models import Usuario
from django.shortcuts import get_object_or_404
from django.db.models.query_utils import Q

def montar_contexto_home(funcionario):
    context = {}

    context['pausa_aprovada'] = Pausa.objects.filter(funcionario=funcionario, aprovado=True)
    context['pausa_nao_aprovada'] = FilaEspera.objects.filter(funcionario=funcionario)
    context['fila'] = FilaEspera.objects.order_by('data_entrada').first()
    
    context['pausa_iniciada'] = Pausa.objects.filter(funcionario=funcionario, inicio__isnull=False, aprovado=True)

    total_pausa = PausasDiarias()
    context['total_pausa'] = total_pausa.calcular_tempo_decorrido(funcionario)

    try:
        pausa_object = get_object_or_404(Pausa, funcionario=funcionario)
        context['alerta_pausa'] = pausa_object.calcular_tempo_ate_aviso()
    except:
        context['alerta_pausa'] = False

    try:
        bo_object = get_object_or_404(BackOffice, funcionario=funcionario)
        context['alerta_bo'] = bo_object.calcular_tempo_ate_aviso()
    except:
        context['alerta_bo'] = False

    # fila pausas
    if funcionario.ja_utilizou_pausa:
        user_pausa1 = Usuario.objects.filter(ja_utilizou_pausa=True)
        fila_pausa_object = FilaEspera.objects.filter(funcionario__in=user_pausa1).order_by('data_entrada')
    else:
        user_pausa2 = Usuario.objects.filter(ja_utilizou_pausa=False)
        fila_pausa_object = FilaEspera.objects.filter(funcionario__in=user_pausa2).order_by('data_entrada')

    context['index_pausa'] = next((i for i, f in enumerate(fila_pausa_object) if f.funcionario == funcionario), None)
    context['fila_total'] = fila_pausa_object.count()

    # BO
    context['bo_aprovado'] = BackOffice.objects.filter(funcionario=funcionario, aprovado=True, pausa=False)
    context['bo_nao_aprovado'] = BackOfficeFilaEspera.objects.filter(funcionario=funcionario)

    if funcionario.turno_manha:
        usuarios_manha = Usuario.objects.filter(turno_manha=True)
        fila_bo_object = BackOfficeFilaEspera.objects.filter(
            funcionario__in=usuarios_manha
        ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada')
    else:
        usuarios_tarde = Usuario.objects.filter(turno_manha=False)
        fila_bo_object = BackOfficeFilaEspera.objects.filter(
            funcionario__in=usuarios_tarde
        ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada')

    context['fila_bo'] = fila_bo_object
    context['index_bo'] = next((i for i, f in enumerate(fila_bo_object) if f.funcionario == funcionario), None)

    context['bo_iniciado'] = BackOffice.objects.filter(
        Q(funcionario=funcionario),
        Q(inicio__isnull=False) | Q(pausa=True),
        Q(aprovado=True)
    )
    total_bo = BackOfficeDiario()
    context['bo_total_tempo'] = total_bo.calcular_tempo_decorrido_bo(funcionario)


    # IQS FO
    context['total_dia_transferido'] = Iqs.calcular_quantidade_transferido_dia_fo(funcionario=funcionario)
    context['total_dia_nao_transferido'] = Iqs.calcular_quantidade_nao_transferido_dia_fo(funcionario=funcionario)
    context['taxa_dia_fo'] = Iqs.calcular_taxa_dia_fo(funcionario)
    context['iqs_falta_mes'] = Iqs.calcular_previsao_para_objetivo_fo(funcionario=funcionario)
    context['taxa_mes_fo'] = Iqs.calcular_taxa_transferencia_fo(funcionario=funcionario)
    context['taxa_resposta_geral'] = Iqs.calcular_taxa_resposta_FO(funcionario=funcionario)

    #IQS BO

    context['total_dia_trasnferido_bo']= Iqs.calcular_quantidade_transferido_dia_bo(funcionario=funcionario)
    context['total_dia_nao_transferido_bo'] = Iqs.calcular_quantidade_nao_transferido_dia_bo(funcionario=funcionario)
    context['taxa_dia_bo'] = Iqs.calcular_taxa_dia_bo(funcionario)
    context['iqs_falta_mes_bo'] = Iqs.calcular_previsao_para_objetivo_bo(funcionario=funcionario)
    context['taxa_mes_bo'] = Iqs.calcular_taxa_transferencia_bo(funcionario=funcionario)
    context['taxa_resposta_bo'] = Iqs.calcular_taxa_resposta_BO(funcionario=funcionario)

    
  
    return context
