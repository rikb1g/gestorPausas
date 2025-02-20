
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.pausas.models import Pausa,FilaEspera,PausasDiarias, ConfiguracaoPausa,ConfiguracaoPausa2
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
    funcionarios_primeira_pausa  = Usuario.objects.filter(ja_utilizou_pausa=False)
    funcionarios_segunda_pausa = Usuario.objects.filter(ja_utilizou_pausa=True)
    

    #pausa
    data['total_pausa'] = PausasDiarias.calcular_tempo_decorrido(request.user.usuario)
    data['contador'] = range(21)
    data['pausa_autorizada_1'] = Pausa.objects.filter(aprovado=True,ja_utilizou_pausa=False)
    data['pausa_autorizada_2'] = Pausa.objects.filter(aprovado=True,ja_utilizou_pausa=True)
    data['pausas_fila_1'] = FilaEspera.objects.filter(funcionario__in=funcionarios_primeira_pausa).order_by('data_entrada')
    data['pausas_fila_2'] = FilaEspera.objects.filter(funcionario__in=funcionarios_segunda_pausa).order_by('data_entrada')
    
    #config_pausas_autorizadas
    num_pausa_autorizados_1 = ConfiguracaoPausa.objects.last()
    num_pausa_autorizados_2 = ConfiguracaoPausa2.objects.last()
    data['num_pausa_autorizados_1'] = num_pausa_autorizados_1.capacidade_maxima
    data['num_pausa_autorizados_2'] = num_pausa_autorizados_2.capacidade_maxima
    
    
    # BO
    bo = BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True)
    fila_bo = BackOfficeFilaEspera.objects.filter(funcionario = request.user.usuario)
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
        
