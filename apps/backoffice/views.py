from typing import Any
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from .models import BackOffice, BackofficeConfig, BackOfficeDiario,BackOfficeFilaEspera, parse_formatted_time, formatted_time
from apps.usuarios.models import Usuario



def pedir_bo(request):
    bo_aceites = BackOffice.objects.filter(aprovado=True)
    configuracao = BackofficeConfig.objects.first()
    if not configuracao:
        configuracao = BackofficeConfig.objects.create(capacidade_maxima=0)
    if bo_aceites.count() < configuracao.capacidade_maxima:
        BackOffice.objects.create(funcionario=request.user.usuario, aprovado=True,data_aprovacao=timezone.now())
        return redirect('lista_intervalos')
    else:
        BackOfficeFilaEspera.objects.create(funcionario=request.user.usuario, data_entrada= timezone.now())
        return redirect('lista_intervalos')

def iniciar_bo(request):
    if request.method == 'POST':
        bo_funcionario = BackOffice.objects.filter(funcionario=request.user.usuario)
        for bo in bo_funcionario:
            bo.inicio = timezone.now()
            bo.save()

        return redirect('lista_intervalos')
    return redirect('lista_intervalos')

def finalizar_bo(request):
    if request.method == 'POST':
        bo_funcionario = BackOffice.objects.get(funcionario=request.user.usuario)
        if bo_funcionario:
            bo_funcionario.fim = timezone.now()
            bo_funcionario.save()
            BackOfficeDiario.objects.create(funcionario=bo_funcionario.funcionario, inicio=bo_funcionario.inicio,fim=bo_funcionario.fim)
            bo_funcionario.delete()
    return redirect('home')


def cancelar_bo(request):
    if request.method == 'POST':
        try:
            bo = BackOffice.objects.get(funcionario=request.user.usuario)
            if bo:
                bo.delete()
        except Exception as e:
            print(f"Back office não existente ou: {e}")
        try:
            fila = BackOfficeFilaEspera.objects.get(funcionario = request.user.usuario)
            if fila:
                fila.delete()
        except Exception as e:
            print(f"Bo não esta na fila ou {e}")

        return redirect('home')
    return redirect('home')


def maximo_bo_autorizados(request):
    numero_bo_aceite = request.GET.get('num-bo')

    if numero_bo_aceite:
        config = BackofficeConfig.objects.last()
        if config:
            config.capacidade_maxima = numero_bo_aceite
            config.save()
            messages.success(request,f"O número de intervalos autorizados foi alterado para {numero_bo_aceite}")

        else:
            numero_bo_aceite.objects.create
            messages.success(request,f"O número de intervalos autorizados foi alterado para {numero_bo_aceite}")(capacidade_maxima= numero_bo_aceite)
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
        
    return redirect('home')


def autorizar_bo_supervisor(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    fila = BackOfficeFilaEspera.objects.get(funcionario=funcionario)
    fila.delete()
    BackOffice.objects.create(funcionario=funcionario,aprovado=True, data_aprovacao=timezone.now())
    return redirect('home')

def iniciar_bo_supervisor(request):
    nome = request.GET.get('nome')
    funcionario = Usuario.objects.get(nome=nome)
    bo = BackOffice.objects.get(funcionario=funcionario, aprovado=True)
    if bo:   
        bo.inicio= timezone.now()
        bo.save()
    return redirect('home')


def pausar_bo(request,id):
    bo = BackOffice.objects.get(id=id)
    bo.pausa = True
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
    return redirect('lista_intervalos')

def pausar_bo_sup(request):
    id = request.GET.get('id')
    bo = BackOffice.objects.get(id=id)
    bo.pausa = True
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
    return redirect('home')


def despausar_bo_sup(request):
    id = request.GET.get('id')
    bo = BackOffice.objects.get(id=id)
    bo.inicio = timezone.now()
    bo.termo_pausa = timezone.now()
    bo.pausa = False
    bo.save()
    return redirect('home')


def despausar_bo(request,id):
    bo = BackOffice.objects.get(id=id)
    bo.inicio = timezone.now()
    bo.termo_pausa = timezone.now()
    bo.pausa = False
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




            

