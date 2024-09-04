from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Pausa, ConfiguracaoPausa, FilaEspera



def iniciarIntervalo(request):
    if request.method == 'POST':
        intervalo = Pausa(funcionario=request.user.usuario, inicio=timezone.now())
        return redirect('lista_intervalos')
    return redirect('lista_intervalos')


def finalizarIntervalo(request):
    if request.method == 'POST':
        pausa_id = request.POST.get('pausa_id')
        intervalo = get_object_or_404(Pausa, id=pausa_id,funcionario=request.user.usuario, fim__isnull=True)
        intervalo.fim = timezone.now()
        intervalo.save()

        proximo_fila = FilaEspera.objects.orderby('data_entrada').first()
        if proximo_fila:
            Pausa.objects.create(funcionario= proximo_fila.funcionario, aprovado=True)

            proximo_fila.delete()
        return redirect('pedir_intervalo')


