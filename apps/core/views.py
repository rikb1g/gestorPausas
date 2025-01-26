
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.pausas.models import Pausa,FilaEspera,PausasDiarias, ConfiguracaoPausa
from apps.backoffice.models import (BackOffice, BackOfficeDiario, BackOfficeFilaEspera, BackofficeConfig,
                                    BackofficeConfigTarde_BO)
from apps.usuarios.models import Usuario

# Create your views here.

@login_required
def home(request):
    data = {}
    data['user'] = request.user
    pausas = Pausa.objects.filter(funcionario= request.user.usuario, aprovado=True)
    fila = FilaEspera.objects.filter(funcionario= request.user.usuario)
    

    #pausa
    data['total_pausa'] = PausasDiarias.calcular_tempo_decorrido(request.user.usuario)
    data['contador'] = range(21)
    data['pausa_autorizada'] = Pausa.objects.filter(aprovado=True)
    data['intervalos_fila'] = FilaEspera.objects.order_by('data_entrada')
    bo = BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True)
    fila_bo = BackOfficeFilaEspera.objects.filter(funcionario = request.user.usuario)
    num_pausa_autorizados = ConfiguracaoPausa.objects.last()
    data['num_pausa_autorizados'] = num_pausa_autorizados.capacidade_maxima
    
    
    # BO
    funcionarios_manha = Usuario.objects.filter(turno_manha=True)
    funcionarios_tarde = Usuario.objects.filter(turno_manha= False)
    data['total_bo'] = BackOfficeDiario.calcular_tempo_decorrido_bo(request.user.usuario)
    data['bo_autorizado_manha'] = BackOffice.objects.filter(funcionario__in=funcionarios_manha,aprovado=True)
    data['bo_autorizado_tarde'] = BackOffice.objects.filter(funcionario__in=funcionarios_tarde,aprovado=True)
    data['bo_fila_manha'] = BackOfficeFilaEspera.objects.filter(
        funcionario__in=funcionarios_manha).order_by('data_entrada')
    data['bo_fila_tarde'] = BackOfficeFilaEspera.objects.filter(
        funcionario__in=funcionarios_tarde).order_by('data_entrada')

    num_bo_autorizado_manha = BackofficeConfig.objects.last()
    num_bo_autorizado_tarde = BackofficeConfigTarde_BO.objects.last()
    data['num_bo_autorizado_manha'] = num_bo_autorizado_manha.capacidade_maxima
    data['num_bo_autorizado_tarde'] = num_bo_autorizado_tarde.capacidade_maxima




        
    if pausas.exists() or fila.exists() or bo.exists() or fila_bo.exists():
        return redirect('lista_intervalos')
    if request.user.usuario.tipo.tipo == "Assistente":
        return redirect('lista_intervalos')

        
    return render(request=request,template_name='core/index.html',context=data)
        
