from datetime import timedelta
import json
from typing import Any
from django.db.models.query import QuerySet

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView
from django.db import transaction
from .models import Pausa, ConfiguracaoPausa, FilaEspera, PausasDiarias, ConfiguracaoPausa2
from apps.usuarios.models import Usuario
from apps.pausas.utils import montar_contexto_home



@method_decorator(login_required, name='dispatch')
class Lista_Pausas(ListView):
    model = Pausa
    context_object_name = 'lista_pausas'
    template_name = 'pausas/pausa_list.html'

    def dispatch(self, request: HttpRequest, *args, **kwargs):
       
        if request.user.usuario.supervisor:
            return redirect('home')  
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        funcionario = self.request.user.usuario
        return Pausa.objects.filter(funcionario=funcionario,aprovado=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(montar_contexto_home(self.request.user.usuario))
        return context


    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("lista par")
            return ['pausas/pausa_list_partial.html']
        return ['pausas/pausa_list.html']



@login_required
def pedir_pausa(request):
    pausas_aceites1 = Pausa.objects.filter(aprovado=True,ja_utilizou_pausa=False)
    pausas_aceites2 = Pausa.objects.filter(aprovado=True,ja_utilizou_pausa=True)
    configuracao = ConfiguracaoPausa.objects.first() or ConfiguracaoPausa.objects.create(capacidade_maxima=0)
    configuracao2 = ConfiguracaoPausa2.objects.first() or ConfiguracaoPausa2.objects.create(capacidade_maxima=0)
    pausa_utilizada = PausasDiarias.objects.filter(funcionario=request.user.usuario)
    total_pausa = timedelta()
    user = get_object_or_404(Usuario, user=request.user)
    if pausa_utilizada.exists():
        for pausa in pausa_utilizada:
            total_pausa += pausa.fim - pausa.inicio        
    
    if total_pausa > timedelta(minutes=1):
        user.ja_utilizou_pausa = True
        user.save()
        with transaction.atomic():
            if Pausa.objects.filter(funcionario=user, aprovado=True).exists() or \
                FilaEspera.objects.filter(funcionario=user).exists():
                print("Pedido duplicado evitado")
                context = montar_contexto_home(request.user.usuario)
                return JsonResponse({"success": True, "message": "Pedido duplicado evitado."}, status=200)
                
            if pausas_aceites2.count() < configuracao2.capacidade_maxima:
                Pausa.objects.create(funcionario=user,aprovado=True,data_aprovacao=timezone.now(),ja_utilizou_pausa=True)
                print(f"pausa aceite e nao criada fila no utilizador{request.user.usuario} ")
                return JsonResponse({"success": True, "message": "Boa Pausa!!!"}, status=200)
                
            else:
                FilaEspera.objects.create(funcionario= user, data_entrada= timezone.now())
                print(f"criada fila no utilizador{user}")
                return JsonResponse({"success": True, "message": "Em Fila!!!"}, status=200)
                
    else:
        user.ja_utilizou_pausa = False
        user.save()
        with transaction.atomic():
            if Pausa.objects.filter(funcionario=user, aprovado=True).exists() or \
                FilaEspera.objects.filter(funcionario=user).exists():
                print("Pedido duplicado evitado")
                return JsonResponse({"success": True, "message": "Pedido duplicado evitado."}, status=200)
                
            if pausas_aceites1.count() < configuracao.capacidade_maxima:
                Pausa.objects.create(funcionario=user,aprovado=True,data_aprovacao=timezone.now(),ja_utilizou_pausa=False)
                print(f"pausa aceite e nao criada fila no utilizador{user} ")
                return JsonResponse({"success": True, "message": "Boa Pausa!!!"}, status=200)
                
            else:
                FilaEspera.objects.create(funcionario= request.user.usuario, data_entrada= timezone.now())
                print(f"criada fila no utilizador{request.user.usuario}")
                context = montar_contexto_home(request.user.usuario)
                return JsonResponse({"success": True, "message": "Em Fila!!!"}, status=200)

    return JsonResponse({"success": False, "message": "Erro ao marcar pausa!!!"}, status=200)
                
   

    



@login_required
def iniciar_intervalo(request):
    try:
        funcionario = request.user.usuario
        intervalo = get_object_or_404(Pausa, funcionario=funcionario)
        intervalo.iniciar_pausa()
        return JsonResponse({'success': True,"message": "Boa Pausa!!!"}, status=200)
    except Exception as e:
            return JsonResponse({'success': False,"error": f"Erro interno: {str(e)}"}, status=500)

    





@login_required
def finalizar_intervalo(request):
    print(request.method)
    if request.method == 'POST':
        print("aqui")
        intervalo = get_object_or_404(Pausa,funcionario=request.user.usuario)
        if intervalo:
            intervalo.terminar_intervalo()
            return JsonResponse({'success': True,"message": "Bom Trabalho!!!"}, status=200)
        else:
            return JsonResponse({'success': False,"error": "Intervalo nao iniciado"}, status=500)

    return JsonResponse({'success': False,"error": "Método nao permitido"}, status=405)



def cancelar_intervalo(request):
    print(request.method)
    if request.method == 'POST':
        user = request.user.usuario
        print(f"user: {user}")
        if user.supervisor:
            id = request.GET.get('id') 
            print(f"id: {id}")  
            try:
                pausa = get_object_or_404(Pausa, id=id)
                print(f"pausa: {pausa}")
            except:
                pausa = get_object_or_404(FilaEspera, id=id) 
        else:
            try:
                pausa = get_object_or_404(Pausa, funcionario=user)
            except:
                pausa = get_object_or_404(FilaEspera, funcionario=user)    
        try:
            
            for pausa in Pausa.objects.filter(funcionario=pausa.funcionario):
                pausa.delete()
        except Exception as e:
            print(f"Intervalo nao existe ou: {e}")
        try:
            for fila in FilaEspera.objects.filter(funcionario=pausa.funcionario):
                fila.delete()
        except Exception as e:
            print(f"Pausa nao existe ou: {e}")


        return JsonResponse({"success": True, "message": "Intervalo Cancelado."}, status=200)
    return JsonResponse({"success": False,"error": "Método não permitido "}, status=405)



def maximo_intervalos(request,teve_intervalo):
    print(request.method)
    if request.method == 'POST':
        print("entrou")
        numero_intervalo = request.POST.get('num')
        print(numero_intervalo)
        teve_intervalo = str(teve_intervalo).lower()
        print(teve_intervalo)

        if teve_intervalo == "true":
            teve_intervalo = True
        elif teve_intervalo == "false":
            teve_intervalo = False

        if numero_intervalo:
            if teve_intervalo:
                config = ConfiguracaoPausa.objects.last() or ConfiguracaoPausa.objects.create(capacidade_maxima=0)
            else:
                config = ConfiguracaoPausa2.objects.last() or ConfiguracaoPausa2.objects.create(capacidade_maxima=0)
            
            if config:
                config.capacidade_maxima = numero_intervalo
                config.save()
                return JsonResponse({"success": True,"message":"Capacidade alterada"}, status=200)

        return JsonResponse({"success": False,"message": "Sem interalo para alterar "}, status=405)
        
    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)



def autorizar_intervalo(request):
    if request.method == 'POST':
        try:
            id= request.GET.get('id')
            print(f"id: {id}")
            funcionario = Usuario.objects.get(id=id)
            print(f"funcionario: {funcionario}")
            for fila in FilaEspera.objects.filter(funcionario= funcionario):
                fila.delete()
            Pausa.objects.create(funcionario= funcionario, aprovado=True, data_aprovacao=timezone.now(),ja_utilizou_pausa=funcionario.ja_utilizou_pausa)
            return JsonResponse({"success": True, "message": "Intervalo Autorizado."}, status=200)
        except Exception as e:
            print(f"Intervalo nao existe ou: {e}")
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)
    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)


def calcular_tempo_pausa(request, id):
    try:
        pausa = Pausa.objects.get(id=id)
        data = {
            'calcular_tempo_pausa_ao_segundo': pausa.calcular_tempo_pausa_ao_segundo(),
        }
        return JsonResponse(data)
    except Pausa.DoesNotExist:
        return JsonResponse({'error': 'Objeto não encontrado'}, status=404)








