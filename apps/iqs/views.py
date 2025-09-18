import json
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
        context['tipo_iqs'] = TipoIqs.objects.all()
        return context
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['iqs/listar_iqs_partial.html']
        return ['iqs/listar_iqs.html']




def iqs_front_office_submit(request, data=None): 
    print("aqe")
    transferido = TipoIqs.objects.get_or_create(name='Transferida FO')[0]
    nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0]
    print(transferido)
    print(nao_transferido)
    iqs = request.GET.get('iqs')
    print(iqs)
    try:
        funcionario = request.user.usuario
        if data is None:
            data = timezone.now()
        if iqs == 'true':       
            Iqs.objects.create(tipo=transferido,data=timezone.now(),funcionario=funcionario)
        elif iqs == 'false':
            Iqs.objects.create(tipo=nao_transferido,data=timezone.now(),funcionario=funcionario)

        return JsonResponse({'success': True})

    except Exception as e:
        print(f"erro as {e}")
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)
    

def iqs_back_office_submit(request, data=None):
    transferido = TipoIqs.objects.get_or_create(name='Transferida BO')[0]
    nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido BO')[0]
    iqs = request.GET.get('iqs')
    print(iqs)
    try:
        funcionario = request.user.usuario
        if data is None:
            data = timezone.now()
        if iqs == 'true':       
            Iqs.objects.create(tipo=transferido,data=timezone.now(),funcionario=funcionario)
        elif iqs == 'false':
            Iqs.objects.create(tipo=nao_transferido,data=timezone.now(),funcionario=funcionario)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)
    
def eliminar_iqs_fo(request):
    tipo = request.GET.get('iqs')
    data = timezone.now().date()
    try:
        if tipo == 'true':
            transferido = TipoIqs.objects.get_or_create(name='Transferida FO')[0]
            iqs = Iqs.objects.filter(tipo=transferido,funcionario=request.user.usuario, data =data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
        elif tipo == 'false':
            nao_transferido = TipoIqs.objects.get_or_create(name='Nao Transferido FO')[0]
            iqs = Iqs.objects.filter(tipo=nao_transferido,funcionario=request.user.usuario, data =data).last()
            if iqs: 
                iqs.delete()
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)
    

def eliminar_iqs_bo(request):
    tipo = request.GET.get('iqs')
    data = timezone.now().date()
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

    

    