import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.shortcuts import render
from .models import FrontOfficeNPS,BackOfficeNPS,NPS ,HistoricoNPS
from .forms import RechamadaUploadForm,ProvisoriosUploadForm, NpsFileUploadForm
from apps.usuarios.models import Usuario, TipoUsuario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from datetime import datetime
import pandas as pd



@method_decorator(login_required, name='dispatch')
class frontoffice_nps(ListView):
    model = NPS
    context_object_name= 'nps_individual'

    def get_queryset(self):
        funcionario = self.request.user.usuario
        return NPS.objects.filter(funcionario=funcionario)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        funcionario = self.request.user.usuario
        nps_intancia = NPS.objects.filter(funcionario=funcionario).first()
        ano = datetime.now().year 
        
        
        
        meses_nomes_ajustados = {mes: nome for mes, nome in MESES_NOMES.items()}
        context['meses'] = meses_nomes_ajustados
        historico_nps = get_nps_context(funcionario,datetime.now().year)
        context['promotores_mes'] = {mes: historico_nps['promotores_mes'][mes] for mes in range(1, 13)}
        context['detratores_mes'] = {mes: historico_nps['detratores_mes'][mes] for mes in range(1, 13)}
        context['neutros_mes'] = {mes: historico_nps['neutros_mes'][mes] for mes in range(1, 13)}
        
        if nps_intancia:
            nps_por_mes = {
                mes: nps_intancia.calculo_nps_mes(mes,ano) for mes in range(1,13)
            }
            nps_por_mes_global = {
                mes: nps_intancia.calculo_nps_global_mes(mes,ano) for mes in range(1,13)
            }

        else:
            nps_por_mes = { mes: "-" for mes in range(1,13)}
            nps_por_mes_global = { mes: "-" for mes in range(1,13)}

        context['nps_por_mes'] = nps_por_mes
        context['nps_por_mes_global'] = nps_por_mes_global
        nps_values = list(nps_por_mes.values())
        media_nps = sum(nps_por_mes.values()) / len(nps_por_mes)
        
        context['nps_mes_json'] = json.dumps(nps_por_mes)
        context['nps_mes_global_json'] = json.dumps(nps_por_mes_global)
        context['media_nps'] = round(media_nps ,2)
        

        
        
        


        return context
    

def get_nps_context(funcionario, ano):
    historico_nps ={h.data.month: h for h in HistoricoNPS.objects.filter(funcionario=funcionario, data__year=ano)}
    promotores_mes = {}
    detratores_mes = {}
    neutros_mes = {}
    for mes in range(1, 13):
        if mes in historico_nps:
            historico = historico_nps[mes]
            promotores_mes[mes] = historico.promotores
            detratores_mes[mes] = historico.detratores
            neutros_mes[mes] = historico.neutros
        else:
            nps_instance = NPS.objects.filter(funcionario=funcionario, data__month=mes, data__year=ano).first()
            if nps_instance:
                promotores_mes[mes] = nps_instance.calculo_promotores_mes(mes,ano)
                detratores_mes[mes] = nps_instance.calculo_detratores_mes(mes,ano)
                neutros_mes[mes] = nps_instance.calculo_neutros_mes(mes,ano)
            else:
                promotores_mes[mes] = 0
                detratores_mes[mes] = 0
                neutros_mes[mes] = 0
    return {
        'promotores_mes': promotores_mes,
        'detratores_mes': detratores_mes,
        'neutros_mes': neutros_mes
    }




def pesquisar_interacoes(request):
    query = request.GET.get('pesquisaInteracoes').strip()
    if query:
        interacoes = NPS.objects.get(interacao__icontains=query)
        print(interacoes)
    else:
        interacoes = NPS.objects.none()
    data = [{
        'interacao': interacoes.interacao,
        'nome': interacoes.funcionario.nome,
        'data': interacoes.data,
        'nota': interacoes.nota,
        }]
    return JsonResponse({'resultados': data})

MESES_NOMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def user_directory_path(instance, filename):
    return f'uploads/{instance.funcionario}/{filename}'


def upload_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'nps':
            form_nps = NpsFileUploadForm(request.POST, request.FILES)
            if form_nps.is_valid():
                ficheiro =form_nps.cleaned_data['arquivo']
                ler_excel_nps(ficheiro)
                messages.success(request, 'Ficheiro NPS carregado com sucesso!')
            else:
                messages.error(request, 'Erro ao carregar o ficheiro NPS.')
            return redirect('upload_view')
        elif form_type == 'rechamada':
            form_rechamada = RechamadaUploadForm(request.POST, request.FILES)
            if form_rechamada.is_valid():
                messages.success(request, 'Ficheiro Rechamada carregado com sucesso!')
            else:
                messages.error(request, 'Erro ao carregar o ficheiro Rechamada.')
            return redirect('upload_view')
        elif form_type == 'provisorios':
            form_provisorios = ProvisoriosUploadForm(request.POST, request.FILES)
            if form_provisorios.is_valid():
                messages.success(request, 'Ficheiro Provisorios carregado com sucesso!')
            else:
                messages.error(request, 'Erro ao carregar o ficheiro Provisorios.')
            return redirect('upload_view')
    else:
        form_nps = NpsFileUploadForm()
        form_rechamada = RechamadaUploadForm()
        form_provisorios = ProvisoriosUploadForm()
    
    contex = {
        "form_NpsFileUploadForm": form_nps,
        "form_RechamadaUploadForm": form_rechamada,
        "form_ProvisoriosUploadForm": form_provisorios,
    }
    return render(request, 'indicador/upload.html', contex)


            

def processar_nps(row, interacao_col, data_col, valioso_col, valor_col, modelo_nps):
    
    
    valor_interacao = row.get(interacao_col)
    data_value = row.get(data_col)
    valioso = row.get(valioso_col)

    # Ignorar linhas inválidas
    if not valor_interacao or str(valor_interacao).strip() == '':
        return  
    if not valioso or str(valioso).strip() == '':
        return  # Ignora se o campo "Valioso" estiver vazio
    
    # Tratamento de data
    if isinstance(data_value, str):
        try:
            data_value = datetime.fromisoformat(data_value)
        except ValueError:
            return  # Ignora datas inválidas
    elif not isinstance(data_value, datetime):
        return  # Ignora se não for string nem datetime

    # Verificar se a interação já existe
    if modelo_nps.objects.filter(interacao=valor_interacao).exists():
        return  # Evita duplicação de NPS

    # Buscar ou criar o usuário sem duplicações
    assistente, _ = TipoUsuario.objects.get_or_create(tipo="Assistente")
    usuario, criado = Usuario.objects.get_or_create(
        identificador=valioso,
        defaults={"nome": valioso, "tipo": assistente}
    )

    # Criar o objeto NPS
    modelo_nps.objects.create(
        funcionario=usuario,
        nota=row.get(valor_col, 0),  # Se não houver nota, assume 0
        data=data_value,
        interacao=valor_interacao
    )

def ler_excel_nps(file):
    df = pd.read_excel(file)

    # Processar FrontOfficeNPS
    for _, row in df.iterrows():
        processar_nps(row, 'ID_INTERACAO', 'DATA', 'Valioso', 'VALOR', FrontOfficeNPS)
    


    # Processar BackOfficeNPS
    for _, row in df.iterrows():
        processar_nps(row, 'ID_INTERACAO.1', 'DATA.1', 'Valioso.1', 'VALOR.1', BackOfficeNPS)
        