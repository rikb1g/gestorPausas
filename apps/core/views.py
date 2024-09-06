from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.pausas.models import Pausa,FilaEspera
# Create your views here.

@login_required
def home(request):
    data = {}
    data['user'] = request.user
    pausas = Pausa.objects.filter(funcionario= request.user.usuario, aprovado=True)
    fila = FilaEspera.objects.filter(funcionario= request.user.usuario)
    print(fila)
    print(pausas)

    if  pausas.exists() or fila.exists():
        return redirect('lista_intervalos')
        
    else:
        return redirect('index')
        