from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import (BackOffice, BackofficeConfig,BackofficeConfigTarde_BO,
                     BackOfficeDiario,BackOfficeFilaEspera, parse_formatted_time, formatted_time)
from apps.usuarios.models import Usuario
from apps.pausas.models import ConfiguracaoPausa, ConfiguracaoPausa2



def pedir_bo(request):
    if request.method == 'POST':
        turno = str(request.GET.get('turno')).lower()
        usuario = get_object_or_404(Usuario, user=request.user)
        if turno == "true":
            usuario.turno_manha = True
            usuario_turno = True
        elif turno == "false":
            usuario.turno_manha = False
            usuario_turno = False
        usuario.save()
        print(f"turno: {turno}")

        bo_aceites_manha = BackOffice.objects.filter(aprovado=True,turno_manha=True)
        bo_aceites_tarde = BackOffice.objects.filter(aprovado=True,turno_manha=False)
        print(f"pediu bo: {request.user} turno: {usuario_turno}")
        ultrapassou_limite = False
        if usuario_turno:
            configuracao_manha = BackofficeConfig.objects.first()
        else:
            configuracao_tarde = BackofficeConfigTarde_BO.objects.first()
        limite_bo = BackOfficeDiario.objects.filter(funcionario=usuario).first()
        if limite_bo:
            print(limite_bo)
            ultrapassou_limite = limite_bo.ultrapassou_tempo_bo_total()
        else:
            print("sem bo diario")

        if usuario_turno:
            with transaction.atomic():
                if BackOffice.objects.filter(funcionario=usuario, aprovado=True,turno_manha=True).exists() or \
                BackOfficeFilaEspera.objects.filter(funcionario= usuario).exists():
                    print("Pedido duplicado evitado")
                    

                if bo_aceites_manha.count() < configuracao_manha.capacidade_maxima and not ultrapassou_limite:
                    BackOffice.objects.create(funcionario=request.user.usuario,
                                            aprovado=True,data_aprovacao=timezone.now(),turno_manha= True)
                    return JsonResponse({"message":"BO aprovado!"}, status=200)
                else:
                    BackOfficeFilaEspera.objects.create(funcionario=request.user.usuario, data_entrada= timezone.now())
                    return JsonResponse({"message":"BO pedido, estás em fila de espera!"}, status=200)
        else:
            with transaction.atomic():
                if BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True,turno_manha=False).exists() or \
                        BackOfficeFilaEspera.objects.filter(funcionario=request.user.usuario).exists():
                    print("Pedido duplicado evitado")
                    return redirect('lista_intervalos')

                if bo_aceites_tarde.count() < configuracao_tarde.capacidade_maxima and not ultrapassou_limite:
                    print(f"boa aceites de tarde: {bo_aceites_tarde.count()}")
                    BackOffice.objects.create(funcionario=request.user.usuario, aprovado=True,
                                            data_aprovacao=timezone.now(),turno_manha=False)
                    return JsonResponse({"message":"BO aprovado!"}, status=200)
                else:
                    print()
                    BackOfficeFilaEspera.objects.create(funcionario=request.user.usuario, data_entrada=timezone.now())
                    return JsonResponse({"message":"BO pedido, estás em fila de espera!"}, status=200)

    return JsonResponse({"error": "Método não permitido"}, status=405)


def iniciar_bo(request):
    if request.method == 'POST':
        try:
            funcionario = request.user.usuario
            bo = get_object_or_404(BackOffice, funcionario= funcionario)
            bo.inicio = timezone.now()
            bo.save()
            print(f"BO iniciado {funcionario} por {request.user.usuario}")
            return JsonResponse({"message":"BO Iniciado"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)

def finalizar_bo(request):
    if request.method == 'POST':
        bo_funcionario = BackOffice.objects.get(funcionario=request.user.usuario)
        if bo_funcionario:
            bo_funcionario.fim = timezone.now()
            bo_funcionario.save()
            BackOfficeDiario.objects.create(funcionario=bo_funcionario.funcionario, inicio=bo_funcionario.inicio,fim=bo_funcionario.fim)
            bo_funcionario.delete()
            print(f"{bo_funcionario.funcionario} Finalizou BO")
    return redirect('home')


def cancelar_bo(request):
    if request.method == 'POST':
        try:
            bo = BackOffice.objects.filter(funcionario=request.user.usuario)
            for backoffice in bo:
                backoffice.delete()
                print(f"{backoffice.funcionario} teve BO cancelado por {request.user.usuario}")
        except Exception as e:
            print(f"Back office não existente ou: {e}")
        try:
            fila = BackOfficeFilaEspera.objects.filter(funcionario= request.user.usuario)
            for bo in fila:
                print(f"{bo.funcionario} teve BO cancelado por {request.user.usuario}")
                bo.delete()
        except Exception as e:
            print(f"Bo não esta na fila ou {e}")

        return JsonResponse({"message":"BO Cancelado"}, status=200)
    return JsonResponse({"error": "Método não permitido"}, status=405)


def maximo_bo_autorizados(request, turno):
    
    numero_bo_aceite = request.GET.get('num-bo')
    print(numero_bo_aceite)
    bo_turno = str(turno).lower()
    print(bo_turno)

    if bo_turno == "true":
        bo_turno = True
    elif bo_turno == "false":
        bo_turno = False  

    if numero_bo_aceite:
        if bo_turno:
            config = BackofficeConfig.objects.last()
        else:
            config = BackofficeConfigTarde_BO.objects.last()
        if config:
            config.capacidade_maxima = numero_bo_aceite
            print(f"alterado num de bo:{config.capacidade_maxima}, turno:{bo_turno}, por: {request.user.usuario}")
            config.save()
            return redirect('home')

        else:
            numero_bo_aceite.objects.create(capacidade_maxima= numero_bo_aceite)
            print(f"criado BO: {numero_bo_aceite}")
        return redirect('home')

    return redirect('home')

def cancelar_bo_supervisor(request):
    nome= request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    try:
        fila = BackOfficeFilaEspera.objects.get(funcionario =funcionario)
        if fila:
            fila.delete()
    except Exception as e:
        print(f"Funcionario sem bo em fila ou: {e}")
    if funcionario:
        bo_aceite = BackOffice.objects.filter(funcionario=funcionario)

        for bo in bo_aceite:
            if bo.inicio is None:
                bo.delete()
            else:
                bo.fim = timezone.now()
                bo.save()
                BackOfficeDiario.objects.create(funcionario=bo.funcionario, inicio=bo.inicio, fim=bo.fim)
                bo.delete()
                print(f"BO cancelado de {bo.funcionario} por {request.user.usuario}")
        

    return redirect('home')


def autorizar_bo_supervisor(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    fila = BackOfficeFilaEspera.objects.get(funcionario=funcionario)
    fila.delete()
    if funcionario.turno_manha:
        BackOffice.objects.create(funcionario=funcionario,aprovado=True,turno_manha=True, data_aprovacao=timezone.now())
    else:
        BackOffice.objects.create(funcionario=funcionario,aprovado=True,turno_manha=False, data_aprovacao=timezone.now())
    print(f"BO autorizado de {funcionario} turno:{funcionario.turno_manha} por :{request.user.usuario}")
    return redirect('home')

def iniciar_bo_supervisor(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    bo = BackOffice.objects.get(funcionario=funcionario, aprovado=True)
    if bo:
        bo.inicio= timezone.now()
        bo.save()
        print(f"Bo de {bo.funcionario} foi iniciado por {request.user.usuario}.")
    
    return redirect('home')


def pausar_bo(request,id,isPause):

    try:
        bo = get_object_or_404(BackOffice, id=id)
        is_pause = str(isPause).lower()== 'true'
        if is_pause:
            bo.pausa = True
            print("Pausa ativada")
        else:
            bo.almoco = True
            bo.pausa = True
            print("Almoço ativado")
        
        bo.inicio_pausa = timezone.now()
        bo.save()
        if bo.tempo_ate_pausar:
            tempo_decorrido = bo.inicio_pausa - bo.inicio
            pausa_acumulada = parse_formatted_time(bo.tempo_ate_pausar)
            total = tempo_decorrido + pausa_acumulada
            bo.tempo_ate_pausar = formatted_time(total)
            bo.save()
        else:
            tempo_decorrido = bo.inicio_pausa - bo.inicio
            bo.tempo_ate_pausar = formatted_time(tempo_decorrido)
            bo.save()
        BackOfficeDiario.objects.create(funcionario=bo.funcionario, inicio=bo.inicio, fim=bo.inicio_pausa)
        if request.user.usuario.tipo.tipo == "Supervisor":
            return redirect('home')
        else:
            return redirect('lista_intervalos')
    except Exception as e:
        print(f"erro a pausar : {e}")
        redirect('home')




def despausar_bo_sup(request):
    id = request.GET.get('id')
    bo = BackOffice.objects.get(id=id)
    bo.inicio = timezone.now()  
    bo.termo_pausa = timezone.now()
    bo.pausa = False
    bo.almoco = False
    bo.save()
    return redirect('home')


def despausar_bo(request,id):
    bo = BackOffice.objects.get(id=id)
    bo.inicio = timezone.now()
    bo.termo_pausa = timezone.now()
    bo.pausa = False
    bo.almoco = False
    bo.save()
    return redirect('lista_intervalos')


def tempo_bo(request, id):
    try:
        bo = BackOffice.objects.get(id=id)
        data = {
            'calcular_tempo_bo_ao_segundo': bo.calcular_tempo_bo_ao_segundo(),
        }
        return JsonResponse(data)
    except BackOffice.DoesNotExist:
        return JsonResponse({'error': 'Objeto não encontrado'}, status=404)
    
def maximos_autorizados(request):
    maximo_intervalos = ConfiguracaoPausa.objects.last()
    maximo_intervalos2= ConfiguracaoPausa2.objects.last()
    maximo_bo_manha = BackofficeConfig.objects.last()
    maximo_bo_tarde = BackofficeConfigTarde_BO.objects.last()


    data = {
        'maximo_intervalos1': maximo_intervalos.capacidade_maxima,
        'maximo_intervalos2': maximo_intervalos2.capacidade_maxima,
        'maximo_bo_manha': maximo_bo_manha.capacidade_maxima,
        'maximo_bo_tarde': maximo_bo_tarde.capacidade_maxima,
    }
    return JsonResponse(data)











