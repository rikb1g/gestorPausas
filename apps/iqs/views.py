import json
import calendar
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import ListView
from apps.iqs.models import Iqs, TipoIqs
from apps.indicador.models import NPS, FrontOfficeNPS
from django.utils import timezone


class IqsListView(ListView):
    model = Iqs
    context_object_name = 'iqs'
    template_name = 'iqs/listar_iqs.html'

    def get_queryset(self):
        funcionario = self.request.user.usuario
        return Iqs.objects.filter(funcionario=funcionario)
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['iqs/listar_iqs_partial.html']
        return ['iqs/listar_iqs.html']   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario = self.request.user.usuario

        TRANSFERIDA_FO = TipoIqs.objects.get_or_create(name='Transferida FO')[0]
        TRANSFERIDA_BO = TipoIqs.objects.get_or_create(name='Transferida BO')[0]
        NAO_TRANSFERIDA_FO = TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0]
        NAO_TRANSFERIDA_BO = TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0]

       

        hoje = timezone.now().date()
        ano, mes = hoje.year, hoje.month
        numero_dias = calendar.monthrange(ano, mes)[1]
        inicio_mes = timezone.datetime(ano, mes, 1).date()
        fim_mes = timezone.datetime(ano, mes, numero_dias).date()

        # 🔹 Query única com agregações por dia
        iqs_mes = (
            Iqs.objects.filter(funcionario=funcionario, data__range=(inicio_mes, fim_mes))
            .values('data')
            .annotate(
                transferido_fo=Count('id', filter=Q(tipo_id=TRANSFERIDA_FO.id)),
                nao_transferido_fo=Count('id', filter=Q(tipo_id=NAO_TRANSFERIDA_FO.id)),
                transferido_bo=Count('id', filter=Q(tipo_id=TRANSFERIDA_BO.id)),
                nao_transferido_bo=Count('id', filter=Q(tipo_id=NAO_TRANSFERIDA_BO.id)),
            )
        )

        # Indexar por data para lookup rápido
        iqs_por_dia = {item['data']: item for item in iqs_mes}

        dias_taxas = []
        for dia in range(1, numero_dias + 1):
            dia_data = timezone.datetime(ano, mes, dia).date()
            dados = iqs_por_dia.get(dia_data, {
                'transferido_fo': 0,
                'nao_transferido_fo': 0,
                'transferido_bo': 0,
                'nao_transferido_bo': 0,
            })

            total_fo = dados['transferido_fo'] + dados['nao_transferido_fo']
            total_resposta = total_fo + dados['transferido_bo'] + dados['nao_transferido_bo']

            taxa_iqs_dia = round(dados['transferido_fo'] / total_fo * 100, 2) if total_fo > 0 else 0
            taxa_resposta_dia = round(
                (dados['transferido_fo'] + dados['transferido_bo']) / total_resposta * 100, 2
            ) if total_resposta > 0 else 0

            dias_taxas.append({
                'dia': dia,
                'transferida_fo': dados['transferido_fo'],
                'nao_transferida_fo': dados['nao_transferido_fo'],
                'transerida_bo': dados['transferido_bo'],
                'nao_transferida_bo': dados['nao_transferido_bo'],
                'taxa_resposta_dia': taxa_resposta_dia,
                'taxa_iqs_dia': taxa_iqs_dia,
            })

        context['dias_taxas'] = dias_taxas
        context['dias'] = range(1, numero_dias + 1)

        # 🔹 Query única para os totais globais
        totais = Iqs.objects.filter(funcionario=funcionario).aggregate(
            total_transferidos_fo=Count('id', filter=Q(tipo_id=TRANSFERIDA_FO.id)),
            total_nao_transferidos_fo=Count('id', filter=Q(tipo_id=NAO_TRANSFERIDA_FO.id)),
            total_transferidos_bo=Count('id', filter=Q(tipo_id=TRANSFERIDA_BO.id)),
            total_nao_transferidos_bo=Count('id', filter=Q(tipo_id=NAO_TRANSFERIDA_BO.id)),
        )

        total_fo = totais['total_transferidos_fo'] + totais['total_nao_transferidos_fo']
        total_bo = totais['total_transferidos_bo'] + totais['total_nao_transferidos_bo']
        total_geral = total_fo + total_bo

        context['total_transferidos_fo'] = totais['total_transferidos_fo']
        context['total_nao_transferidos_fo'] = totais['total_nao_transferidos_fo']
        context['total_transferidos_bo'] = totais['total_transferidos_bo']
        context['total_nao_transferidos_bo'] = totais['total_nao_transferidos_bo']

        context['taxa_geral'] = round(
            totais['total_transferidos_fo'] / total_fo * 100, 2
        ) if total_fo > 0 else 0

        context['taxa_geral_bo'] = round(
            totais['total_transferidos_bo'] / total_bo * 100, 2
        ) if total_bo > 0 else 0

        context['taxa_resposta_geral'] = round(
            (totais['total_transferidos_fo'] + totais['total_transferidos_bo']) / total_geral * 100, 2
        ) if total_geral > 0 else 0

        return context
    
    



def iqs_front_office_submit(request, data=None): 
    print("aqe")
    transferido = TipoIqs.objects.get_or_create(name='Transferida FO')[0]
    nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0]
    iqs = request.GET.get('iqs')
    dia = request.GET.get('dia')
    if dia is None:
        data = timezone.now().date()
    else:
        date = timezone.now()
        ano, mes, dia = date.year, date.month, int(dia)
        data = timezone.datetime(ano, mes, dia).date()
    try:
        funcionario = request.user.usuario
        if data is None:
            data = timezone.now()
        if iqs == 'true':       
            Iqs.objects.create(tipo=transferido,data=data,funcionario=funcionario)
        elif iqs == 'false':
            Iqs.objects.create(tipo=nao_transferido,data=data,funcionario=funcionario)

        return JsonResponse({'success': True})

    except Exception as e:
        print(f"erro as {e}")
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)
    

def iqs_back_office_submit(request):
    transferido = TipoIqs.objects.get_or_create(name='Transferida BO')[0]
    nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0]
    iqs = request.GET.get('iqs')
    dia = request.GET.get('dia')
    funcionario = request.user.usuario
    if dia is None:
        data = timezone.now().date()
    else:
        date = timezone.now()
        ano, mes, dia = date.year, date.month,int(dia)
        data = timezone.datetime(ano, mes, dia).date()
    if iqs:
        try:
            if iqs == 'true':       
                Iqs.objects.create(tipo=transferido,data=data,funcionario=funcionario)
            elif iqs == 'false':
                Iqs.objects.create(tipo=nao_transferido,data=data,funcionario=funcionario)

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)

    
def eliminar_iqs_fo(request):
    tipo = request.GET.get('iqs')
    dia = request.GET.get('dia')
    if dia is None:
        data = timezone.now().date()
    else:
        date = timezone.now()
        ano, mes, dia = date.year, date.month, int(dia)
        data = timezone.datetime(ano, mes, dia).date()
    try:
        if tipo == 'true':
            transferido = TipoIqs.objects.get_or_create(name='Transferida FO')[0]
            iqs = Iqs.objects.filter(tipo=transferido,funcionario=request.user.usuario, data= data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
        elif tipo == 'false':
            nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0]
            iqs = Iqs.objects.filter(tipo=nao_transferido,funcionario=request.user.usuario, data= data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)
    

def eliminar_iqs_bo(request):
    tipo = request.GET.get('iqs')
    dia = request.GET.get('dia')
    if dia is None:
        data = timezone.now().date()
    else:
        date = timezone.now()
        ano, mes, dia = date.year, date.month, int(dia)
        data = timezone.datetime(ano, mes, dia).date()
    try:
        if tipo == 'true':
            iqs = Iqs.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Transferida BO')[0],funcionario=request.user.usuario, data =data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
        elif tipo == 'false':
            iqs = Iqs.objects.filter(tipo=TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0],funcionario=request.user.usuario, data =data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)

    

    