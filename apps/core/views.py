
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.pausas.models import ConfiguracaoPausa, Pausa,FilaEspera,PausasDiarias
from apps.backoffice.models import BackOffice, BackofficeConfig, BackOfficeDiario, BackOfficeFilaEspera

# Create your views here.

@login_required
def home(request):
    data = {}
    data['user'] = request.user
    pausas = Pausa.objects.filter(funcionario= request.user.usuario, aprovado=True)
    fila = FilaEspera.objects.filter(funcionario= request.user.usuario)
    data['total_pausa'] = PausasDiarias.calcular_tempo_decorrido(request.user.usuario)
    data['contador'] = range(11)
    data['pausa_autorizada'] = Pausa.objects.filter(aprovado=True)
    print(data['pausa_autorizada'])
    data['intervalos_fila'] = FilaEspera.objects.order_by('data_entrada')
    bo = BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True)
    fila_bo = BackOfficeFilaEspera.objects.filter(funcionario = request.user.usuario)

        
    if pausas.exists() or fila.exists() or bo.exists() or fila_bo.exists():
        return redirect('lista_intervalos')
        
    return render(request=request,template_name='core/index.html',context=data)
        
