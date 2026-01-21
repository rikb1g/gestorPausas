
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.pausas.models import Pausa,FilaEspera,PausasDiarias, ConfiguracaoPausa,ConfiguracaoPausa2
from apps.backoffice.models import (BackOffice, BackOfficeDiario, BackOfficeFilaEspera, BackofficeConfig,
                                    BackofficeConfigTarde_BO)
from apps.usuarios.models import Usuario
from apps.pausas.utils import montar_contexto_home

# Create your views here.

@login_required
def home(request):
    data = {}
    data['user'] = request.user
    data['supervisor'] = request.user.usuario.supervisor
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
    data['num_pausa_autorizada_1'] = data['pausas_fila_1'].count()
    data['num_pausa_autorizada_2'] = data['pausas_fila_2'].count()
    
    #config_pausas_autorizadas
    num_pausa_autorizados_1 = ConfiguracaoPausa.objects.last()
    num_pausa_autorizados_2 = ConfiguracaoPausa2.objects.last()
    data['num_pausa_autorizados_1'] = num_pausa_autorizados_1.capacidade_maxima
    data['num_pausa_autorizados_2'] = num_pausa_autorizados_2.capacidade_maxima
    
    
    # BO
    bo = BackOffice.objects.filter(funcionario=request.user.usuario, aprovado=True)
    fila_bo = BackOfficeFilaEspera.objects.filter(funcionario = request.user.usuario)
    funcionarios_manha = Usuario.objects.filter(ja_utilizou_bo=False)
    funcionarios_tarde = Usuario.objects.filter(ja_utilizou_bo= True)
    data['total_bo'] = BackOfficeDiario.calcular_tempo_decorrido_bo(request.user.usuario)
    data['bo_autorizado_manha'] = BackOffice.objects.filter(funcionario__in=funcionarios_manha,aprovado=True)
    data['bo_autorizado_tarde'] = BackOffice.objects.filter(funcionario__in=funcionarios_tarde,aprovado=True)
    data['bo_fila_manha'] = BackOfficeFilaEspera.objects.filter(
                funcionario__in=funcionarios_manha
                ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada')

    data['bo_fila_tarde'] = BackOfficeFilaEspera.objects.filter(
                funcionario__in=funcionarios_tarde
                ).order_by('funcionario__ultrapassou_tempo_bo', 'data_entrada')

    num_bo_autorizado_manha = BackofficeConfig.objects.last()
    num_bo_autorizado_tarde = BackofficeConfigTarde_BO.objects.last()
    data['num_bo_autorizado_manha'] = num_bo_autorizado_manha.capacidade_maxima
    data['num_bo_autorizado_tarde'] = num_bo_autorizado_tarde.capacidade_maxima




        
    if (pausas.exists() or fila.exists() or bo.exists() or fila_bo.exists()) and  not request.user.usuario.supervisor:
        print("redirect pausas")
        return redirect('lista_intervalos')
    
    if not request.user.usuario.supervisor:
        print("redirect assistente")
        return redirect('lista_intervalos')


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('HX-Request') == 'true':
        if  request.user.usuario.supervisor:
            print("core/index_partial.html")
            return render(request,template_name='core/index_partial.html',context=data)
        else:
            context = {}
            context = montar_contexto_home(request.user.usuario)
            print("pausas/pausa_list_partial.html")
            return render(request,template_name='pausas/pausa_list_partial.html',context=context)
    else:
        if request.user.usuario.supervisor:
            print("core/index.html")
            return render(request,template_name='core/index.html',context=data)
        else:
            context = {}
            context = montar_contexto_home(request.user.usuario)
            print("pausas/pausa_list.html")
            return render(request,template_name='pausas/pausa_list.html',context=context)
        
        
    
        
