from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import (BackOffice, BackofficeConfig,BackofficeConfigTarde_BO,
                     BackOfficeDiario,BackOfficeFilaEspera, parse_formatted_time, formatted_time)
from apps.usuarios.models import Usuario
from apps.pausas.models import ConfiguracaoPausa, ConfiguracaoPausa2


# corrigir 
def pedir_bo(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, user=request.user)
        BackOfficeDiario.calcular_tempo_para_2_bo(usuario)
        
        usuarios_primeiro_bo = Usuario.objects.filter(ja_utilizou_bo=False)
        usuarios_segundo_bo = Usuario.objects.filter(ja_utilizou_bo=True)
        

        bo_aceites_manha = BackOffice.objects.filter(aprovado=True,funcionario__in=usuarios_primeiro_bo)
        bo_aceites_tarde = BackOffice.objects.filter(aprovado=True,funcionario__in=usuarios_segundo_bo)
        
        ultrapassou_limite = False
        
        configuracao_manha = BackofficeConfig.objects.first()
        configuracao_tarde = BackofficeConfigTarde_BO.objects.first()
        limite_bo = BackOfficeDiario.objects.filter(funcionario=usuario).first()
        if limite_bo:
            print(limite_bo)
            ultrapassou_limite = limite_bo.ultrapassou_tempo_bo_total()
        else:
            print("sem bo diario")

         #parei aqui   
        
        if not usuario.ja_utilizou_bo:
            with transaction.atomic():
                if BackOffice.objects.filter(funcionario=usuario, aprovado=True,turno_manha=True).exists() or \
                BackOfficeFilaEspera.objects.filter(funcionario= usuario).exists():
                    print("Pedido duplicado evitado")
                    return JsonResponse({"success": True, "message": "Pedido duplicado evitado."}, status=200)
                    

                if bo_aceites_manha.count() < configuracao_manha.capacidade_maxima and not ultrapassou_limite:
                    BackOffice.objects.create(funcionario=request.user.usuario,
                                            aprovado=True,data_aprovacao=timezone.now(),turno_manha= True)
                    return JsonResponse({"success": True, "message":"BackOffice Aprovado!!!"}, status=200)
                else:
                    BackOfficeFilaEspera.objects.create(funcionario=request.user.usuario, data_entrada= timezone.now())
                    return JsonResponse({"success": True,"message":"BO pedido, estás em fila de espera!"}, status=200)
        else:
            print("aqui")
            with transaction.atomic():
                if BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True,turno_manha=False).exists() or \
                        BackOfficeFilaEspera.objects.filter(funcionario=request.user.usuario).exists():
                    print("Pedido duplicado evitado")
                    return JsonResponse({"success": True, "message": "Pedido duplicado evitado."}, status=200)

                if bo_aceites_tarde.count() < configuracao_tarde.capacidade_maxima and not ultrapassou_limite:
                    print(f"boa aceites de tarde: {bo_aceites_tarde.count()}")
                    BackOffice.objects.create(funcionario=request.user.usuario, aprovado=True,
                                            data_aprovacao=timezone.now(),turno_manha=False)
                    return JsonResponse({"success": True, "message":"BackOffice Aprovado!!!"}, status=200)
                else:
                    print()
                    BackOfficeFilaEspera.objects.create(funcionario=request.user.usuario, data_entrada=timezone.now())
                    return JsonResponse({"success": True,"message":"BO pedido, estás em fila de espera!"}, status=200)
                    

    return JsonResponse({"success": False,"message": "Método não permitido"}, status=405)

def iniciar_bo(request):
    print(request.method)
    if request.method == 'POST':
        try:
            user = request.user.usuario
            if user.supervisor:
                id = request.GET.get('id')
                print(f"id: {id}")
                bo = get_object_or_404(BackOffice, id=id)
                bo.inicio = timezone.now()
                bo.save()
                print(f"BO iniciado {bo.funcionario} por {request.user.usuario}")
                return JsonResponse({"success": True,"message":"BO Iniciado"}, status=200)
            else:    
                bo = get_object_or_404(BackOffice, funcionario= user)
                bo.inicio = timezone.now()
                bo.save()
                print(f"BO iniciado {user} por {user}")
                return JsonResponse({"success": True,"message":"BO Iniciado"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)

def finalizar_bo(request):
    if request.method == 'POST':
        bo_funcionario = BackOffice.objects.get(funcionario=request.user.usuario)
        try:
            if bo_funcionario:
                bo_funcionario.fim = timezone.now()
                bo_funcionario.save()
                if not bo_funcionario.pausa:
                    print(f"BO finalizado {bo_funcionario.funcionario} por {request.user.usuario}")
                    BackOfficeDiario.objects.create(funcionario=bo_funcionario.funcionario, inicio=bo_funcionario.inicio,fim=bo_funcionario.fim)
                bo_funcionario.delete()
                print(f"{bo_funcionario.funcionario} Finalizou BO")
                BackOfficeDiario.calcular_tempo_para_2_bo(request.user.usuario)
                return JsonResponse({"success": True,"message":"BO Finalizado"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)
    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)


def cancelar_bo(request):
    if request.method == 'POST':
        user = request.user.usuario
        try:
            if user.supervisor:
                id = request.GET.get('id')
                print(f"id: {id}")
                bo = BackOffice.objects.filter(id=id).first()
                if bo is not None:
                    bo.fim = timezone.now()
                    bo.save()
                    BackOfficeDiario.objects.create(funcionario=bo.funcionario, inicio= bo.inicio, fim = bo.fim)
                    BackOfficeDiario.calcular_tempo_para_2_bo(bo.funcionario)
                    bo.delete()
                    return JsonResponse({"success": True,"message":"BO Cancelado"}, status=200)
               
                else:
                    bo = BackOfficeFilaEspera.objects.get(id=id) 
                    for backoffice in BackOfficeFilaEspera.objects.filter(funcionario=bo.funcionario):
                        print("fila")
                        backoffice.delete()
                        print(f"{backoffice.funcionario} teve BO cancelado por {user}")
                    return JsonResponse({"success": True,"message":"BO Cancelado"}, status=200)
            else:
                bo = BackOffice.objects.filter(funcionario=user)
                if bo is not None:
                    for backoffice in BackOffice.objects.filter(funcionario=user):
                        backoffice.delete()
                        print(f"{backoffice.funcionario} teve BO cancelado por {user}")

                bo_fila = BackOfficeFilaEspera.objects.filter(funcionario=user)
                if bo_fila is not None:
                    for backoffice in bo_fila:
                        backoffice.delete()
                        print(f"{backoffice.funcionario} teve BO cancelado por {user}")
                return JsonResponse({"success": True,"message":"BO Cancelado"}, status=200)
        
        except Exception as e:
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)
        
    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)


def maximo_bo_autorizados(request, turno):
    if request.method == 'POST':
        numero_bo_aceite = request.POST.get('num')
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
                return JsonResponse({"success": True,"message":"Capacidade alterada"}, status=200)

            else:
                numero_bo_aceite.objects.create(capacidade_maxima= numero_bo_aceite)
                print(f"criado BO: {numero_bo_aceite}")
            return JsonResponse({"success": True,"message":"Capacidade alterada"}, status=200)

        return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)

def autorizar_bo(request):
    if request.method == 'POST':
        try:
            id = request.GET.get('id')
            funcionario = get_object_or_404(Usuario, id=id)
            for bo in BackOfficeFilaEspera.objects.filter(funcionario=funcionario):
                bo.delete()
        except Exception as e:
            print(f"Bo nao esta na fila ou: {e}")
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)
        try:
            if funcionario.turno_manha:
                BackOffice.objects.create(funcionario=funcionario,aprovado=True,turno_manha=True, data_aprovacao=timezone.now())
            else:
                BackOffice.objects.create(funcionario=funcionario,aprovado=True,turno_manha=False, data_aprovacao=timezone.now())
            print(f"{funcionario} teve BO autorizado por {request.user.usuario}")
            return JsonResponse({"success": True,"message":"BO Autorizado"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)
    return JsonResponse({"success": False,"error": "Método não permitido"}, status=405)




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
        if request.user.usuario.supervisor:
            return JsonResponse({"success": True,"message":"BO Pausado","supervisor": True}, status=200)
        else:
            return JsonResponse({"success": True,"message":"BO Pausado","supervisor": False}, status=200)
    except Exception as e:
        print(f"erro a pausar : {e}")
        return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)




def despausar_bo(request,id):
    try:
        bo = BackOffice.objects.get(id=id)
        bo.inicio = timezone.now()
        bo.termo_pausa = timezone.now()
        bo.pausa = False
        bo.almoco = False
        bo.save()
        if request.user.usuario.supervisor:
            return JsonResponse({"success": True,"message":"BO Despausado","supervisor": True}, status=200)
        else:
            return JsonResponse({"success": True,"message":"BO Despausado","supervisor": False}, status=200)
    except Exception as e:
        return JsonResponse({"success": False,"error": f"Erro interno: {str(e)}"}, status=500)


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











