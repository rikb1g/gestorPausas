import json
import calendar
from django.http import JsonResponse
from django.views.generic import ListView
from apps.iqs.models import Iqs, TipoIqs
from django.utils import timezone


class IqsListView(ListView):
    model = Iqs
    context_object_name = 'iqs'
    template_name = 'iqs/listar_iqs.html'


    def get_queryset(self):
        funcionario = self.request.user.usuario
        return Iqs.objects.filter(funcionario=funcionario)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario = self.request.user.usuario
        
        hoje = timezone.now().date()
        ano, mes = hoje.year, hoje.month
        numero_dias = calendar.monthrange(ano, mes)[1]

        dias_taxas = []
        for dia in range(1, numero_dias + 1):
            dia = timezone.datetime(ano, mes, dia).date()
            transferido_fo = Iqs.calcular_quantidade_transferido_dia_fo(funcionario,dia)
            nao_transferido_fo = Iqs.calcular_quantidade_nao_transferido_dia_fo(funcionario,dia)
            transferido_bo = Iqs.calcular_quantidade_transferido_dia_bo(funcionario,dia)
            nao_transferido_bo = Iqs.calcular_quantidade_nao_transferido_dia_bo(funcionario,dia)
            taxa_resposta_dia = Iqs.calcular_taxa_resposta_dia(funcionario,dia)
            taxa_iqs_dia = Iqs.calcular_taxa_dia_fo(funcionario,dia)

            
            dias_taxas.append({
                'dia': dia.day,
                'transferida_fo': transferido_fo,
                'nao_transferida_fo': nao_transferido_fo,
                'transerida_bo': transferido_bo,
                'nao_transferida_bo':nao_transferido_bo,
                'taxa_resposta_dia': taxa_resposta_dia,
                'taxa_iqs_dia': taxa_iqs_dia,
            })
        context['dias_taxas'] = dias_taxas
        context['dias'] = range(1, numero_dias + 1)

        #taxas gerais
        context['taxa_geral'] = Iqs.calcular_taxa_transferencia_fo(funcionario)
        context['taxa_resposta_geral'] = Iqs.calcular_taxa_resposta_geral(funcionario)
        context['taxa_geral_bo'] = Iqs.calcular_taxa_transferencia_bo(funcionario)
        context['total_transferidos_fo'] = Iqs.total_iqs_transferidos_fo(funcionario)
        context['total_nao_transferidos_fo'] = Iqs.total_iqs_nao_transferidos_fo(funcionario)
        context['total_transferidos_bo'] = Iqs.total_iqs_transferidos_bo(funcionario)
        context['total_nao_transferidos_bo'] = Iqs.total_iqs_nao_transferidos_bo(funcionario)
        
        return context
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['iqs/listar_iqs_partial.html']
        return ['iqs/listar_iqs.html']




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

    

    