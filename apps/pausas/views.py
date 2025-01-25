from typing import Any
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView
from django.contrib import messages
from django.db import transaction
from .models import Pausa, ConfiguracaoPausa, FilaEspera, PausasDiarias
from apps.backoffice.models import BackOffice, BackOfficeDiario, BackOfficeFilaEspera
from apps.usuarios.models import Usuario



@method_decorator(login_required, name='dispatch')
class Lista_Pausas(ListView):
    model = Pausa
    context_object_name = 'lista_pausas'

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        # Lógica para redirecionar caso o tipo do usuário seja 'Assistente'
        if request.user.usuario.tipo.tipo == "Supervisor":
            return redirect('home')  # Substitua 'lista_intervalos' pela URL correta

        # Se não for 'Assistente', continua com a execução normal
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        funcionario = self.request.user.usuario
        return Pausa.objects.filter(funcionario=funcionario,aprovado=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        funcionario = self.request.user.usuario
        context = super().get_context_data(**kwargs)
        context['pausa_aprovada'] = Pausa.objects.filter(funcionario=funcionario,aprovado=True)
        context['pausa_nao_aprovada'] = FilaEspera.objects.filter(funcionario=funcionario)

        context['fila'] = FilaEspera.objects.order_by('data_entrada').first()
        context['fila_total'] = FilaEspera.objects.count()
        fila_object= FilaEspera.objects.order_by('data_entrada')
        index_fila = None       
        for index, fila in enumerate(fila_object):
            if fila.funcionario == self.request.user.usuario:
                index_fila = index
                print(index)
                break
        context['index'] = index_fila
        context['pausa_iniciada'] = Pausa.objects.filter(funcionario= funcionario,inicio__isnull=False ,aprovado=True)
        total_pausa = PausasDiarias()
        tota_horas= total_pausa.calcular_tempo_decorrido(funcionario)
        context['total_pausa'] = tota_horas
        context['alerta_pausa']  = Pausa.calcular_tempo_ate_aviso(funcionario)
        context['alerta_bo'] = BackOffice.calcular_tempo_ate_aviso(funcionario)




        # BO

        context['bo_aprovado'] = BackOffice.objects.filter(funcionario=funcionario, aprovado=True, pausa=False)
        context['bo_nao_aprovado'] = BackOfficeFilaEspera.objects.filter(funcionario=funcionario)
        context['fila_bo'] = BackOfficeFilaEspera.objects.order_by('data_entrada').first()
        if self.request.user.usuario.turno_manha:
            usuarios_manha = Usuario.objects.filter(turno_manha=True)
            fila_bo_object = BackOfficeFilaEspera.objects.filter(funcionario__in=usuarios_manha).order_by('data_entrada')
        elif not self.request.user.usuario.turno_manha:
            usuarios_tarde = Usuario.objects.filter(turno_manha=False)
            fila_bo_object = BackOfficeFilaEspera.objects.filter(funcionario__in=usuarios_tarde).order_by('data_entrada')

        
        idex_fila_bo = None
        for index_bo, fila_bo in enumerate(fila_bo_object):
            if fila_bo.funcionario == self.request.user.usuario:
                idex_fila_bo = index_bo

        context['index_bo'] = idex_fila_bo
        context['bo_iniciado'] = BackOffice.objects.filter(
            Q(funcionario= funcionario),
            Q(inicio__isnull=False) | Q(pausa=True),
            Q(aprovado=True))
        total_bo = BackOfficeDiario()
        total_tempo_bo = total_bo.calcular_tempo_decorrido_bo(funcionario)
        context['bo_total_tempo'] = total_tempo_bo


        return context




def pedir_pausa(request):
    pausas_aceites = Pausa.objects.filter(aprovado=True)
    configuracao = ConfiguracaoPausa.objects.first()
    if not configuracao:
        configuracao = ConfiguracaoPausa.objects.create(capacidade_maxima=0)
    with transaction.atomic():
        if Pausa.objects.filter(funcionario=request.user.usuario, aprovado=True).exists() or \
            FilaEspera.objects.filter(funcionario=request.user.usuario).exists():
            print("Pedido duplicado evitado")
            return redirect('lista_intervalos')
        if pausas_aceites.count() < configuracao.capacidade_maxima:
            Pausa.objects.create(funcionario=request.user.usuario,aprovado=True,data_aprovacao=timezone.now())
            print("pausa aceite e nao criada fila")
            return redirect('lista_intervalos')
        else:
            FilaEspera.objects.create(funcionario= request.user.usuario, data_entrada= timezone.now())
            print("criada fila ")
            return redirect('lista_intervalos')



def iniciarIntervalo(request):
    if request.method == 'POST':
        try:
            funcionario = request.user.usuario
            intervalo = get_object_or_404(Pausa, funcionario=funcionario)
            intervalo.iniciar_pausa()
            return JsonResponse({"message": "Boa Pausa!!!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)






def finalizarIntervalo(request):
    if request.method == 'POST':
        print("aqui")
        intervalo = get_object_or_404(Pausa,funcionario=request.user.usuario)
        if intervalo:
            intervalo.terminar_intervalo()
        return redirect('home')

    return redirect('home')



def cancelar_intervalo(request):
    if request.method == 'POST':
        try:
            intervalo = Pausa.objects.filter(funcionario=request.user.usuario)
            print(intervalo)
            for pausa in intervalo:
                pausa.delete()
        except Exception as e:
            print(f"Intervalo nao existe ou: {e}")
        try:
            pausa= FilaEspera.objects.filter(funcionario=request.user.usuario)
            for fila in pausa:
                fila.delete()
        except Exception as e:
            print(f"Pausa nao existe ou: {e}")

        return JsonResponse({"message": "Intervalo Cancelado."}, status=200)
    return JsonResponse({"error": "Método não permitido"}, status=405)


def maximo_intervalos(request):
    numero_intervalo = request.GET.get('num')

    if numero_intervalo:
        config= ConfiguracaoPausa.objects.last()
        if config:
            config.capacidade_maxima = numero_intervalo
            config.save()
            

        else:
            ConfiguracaoPausa.objects.create(capacidade_maxima = numero_intervalo)
            

        return redirect('home')

    return redirect('home')

def cancelar_intervalo_sup(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    try:
        fila = FilaEspera.objects.get(funcionario=funcionario)
        if fila:
            fila.delete()
    except:
        pass

    if funcionario:
        pausa = Pausa.objects.filter(funcionario=funcionario)
        for intervalo in pausa:
            if intervalo.inicio is None:
                intervalo.delete()
            else:
                print("aqui errado")
                intervalo.fim = timezone.now()
                intervalo.save()
                arquivar = PausasDiarias(funcionario=intervalo.funcionario, inicio=intervalo.inicio, fim=intervalo.fim)
                arquivar.save()
                intervalo.delete()

            return redirect('home')

    return redirect('home')

def autorizar_intervalo_sup(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    fila  = FilaEspera.objects.get(funcionario= funcionario)
    fila.delete()
    Pausa.objects.create(funcionario= funcionario, aprovado=True, data_aprovacao=timezone.now())
    return redirect('home')


def calcular_tempo_pausa(request, id):
    try:
        pausa = Pausa.objects.get(id=id)
        data = {
            'calcular_tempo_pausa_ao_segundo': pausa.calcular_tempo_pausa_ao_segundo(),
        }
        return JsonResponse(data)
    except Pausa.DoesNotExist:
        return JsonResponse({'error': 'Objeto não encontrado'}, status=404)








