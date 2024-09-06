from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from .models import Pausa, ConfiguracaoPausa, FilaEspera, PausasDiarias




class Lista_Pausas(ListView):
    model = Pausa
    context_object_name = 'lista_pausas'

    def get_queryset(self) -> QuerySet[Any]:
        funcionario = self.request.user.usuario
        return Pausa.objects.filter(funcionario=funcionario,aprovado=True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        funcionario = self.request.user.usuario
        context= super().get_context_data(**kwargs)
        context['nao_aprovado'] = Pausa.objects.filter(funcionario=funcionario,aprovado=False)
        context['fila'] = FilaEspera.objects.order_by().first()
        context['iniciado'] = Pausa.objects.filter(funcionario= funcionario,inicio__isnull=False ,aprovado=True)
        return context




def pedir_pausa(request):
    pausas_aceites = Pausa.objects.filter(aprovado=True)
    configuracao = ConfiguracaoPausa.objects.first()
    if not configuracao:
        configuracao = ConfiguracaoPausa.objects.create(capacidade_maxima=1)
    if pausas_aceites.count() <= configuracao.capacidade_maxima:
        pausa= Pausa.objects.create(funcionario=request.user.usuario,aprovado=True)
        print("pausa aceite e nao criada fila")
        return redirect('lista_intervalos')
    else:
        fila = FilaEspera.objects.create(funcionario= request.user.usuario, data_entrada= timezone.now())
        print("criada fila ")
        return redirect('lista_intervalos')




def iniciarIntervalo(request):
    if request.method == 'POST':
        intervalo = Pausa.objects.filter(funcionario=request.user.usuario)
        for inter in intervalo:
            inter.inicio = timezone.now()
            inter.save()
            print(intervalo)
        return redirect('lista_intervalos')
    return redirect('lista_intervalos')
   




def finalizarIntervalo(request, pk):
    intervalo = get_object_or_404(Pausa,pk=pk)
    intervalo.fim = timezone.now()
    intervalo.save()
    arquivar = PausasDiarias(funcionario=intervalo.funcionario, inicio=intervalo.inicio, fim=intervalo.fim)
    arquivar.save()
    intervalo.delete()

    proximo_fila = FilaEspera.objects.order_by('data_entrada').first()
    if proximo_fila:
        Pausa.objects.create(funcionario= proximo_fila.funcionario, aprovado=True)

        proximo_fila.delete()
    return reverse_lazy('home')


