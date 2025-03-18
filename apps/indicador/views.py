import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages 
from django.shortcuts import render
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from .models import FrontOfficeNPS,BackOfficeNPS,NPS ,HistoricoNPS, Interlocutores
from .forms import RechamadaUploadForm,ProvisoriosUploadForm, NpsFileUploadForm, InterlocutoresUploadForm, InterlocutoresForm
from apps.usuarios.models import Usuario, TipoUsuario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
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
        nps_intancia = HistoricoNPS.objects.filter(funcionario=funcionario).first()
        ano = datetime.now().year 

        teste_nps = NPS.objects.filter(funcionario=funcionario, data__year=ano,data__month=datetime.now().month -1).count()
        print(f"teste{teste_nps}")

        
        
        
        
        meses_nomes_ajustados = {mes: nome for mes, nome in MESES_NOMES.items()}
        context['meses'] = meses_nomes_ajustados
        
        
        context['promotores_mes'] = {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_promotores=Sum('promotores'))['total_promotores'] or 0
                     for mes in range(1, 13)
                            }
        context['detratores_mes'] =  {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_detratores=Sum('detratores'))['total_detratores'] or 0
                     for mes in range(1, 13)
                            }
        context['neutros_mes'] =  {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_neutros=Sum('neutros'))['total_neutros'] or 0
                     for mes in range(1, 13)
        }
        
        if nps_intancia:
            nps_por_mes = {
                mes: nps_intancia.calculo_nps_mensal(mes,ano) for mes in range(1,13)
            }
            nps_por_mes_global = {
                mes: nps_intancia.calculo_nps_global_mensal(mes,ano) for mes in range(1,13)
            }
            nps_por_equipa_mensal = {
                mes: nps_intancia.calculo_nps_global_equipa(mes,ano) for mes in range(1,13)
            }
            

        else:
            nps_por_mes = { mes: "-" for mes in range(1,13)}
            nps_por_mes_global = { mes: "-" for mes in range(1,13)}
            nps_por_equipa_mensal = { mes: "-" for mes in range(1,13)}

        context['nps_por_mes'] = nps_por_mes
        context['nps_por_mes_global'] = nps_por_mes_global
        
        nps_values = list(nps_por_mes.values())
        #media_nps = sum(nps_por_mes.values()) / len(nps_por_mes)
        equipa_utilizador = self.request.user.usuario.equipa


        context['nps_mes_json'] = json.dumps(nps_por_mes)
        context['nps_mes_global_json'] = json.dumps(nps_por_mes_global)
        context['nps_equipa_json'] = json.dumps(nps_por_equipa_mensal)
        #context['media_nps'] = round(media_nps ,2)

        return context

@method_decorator(login_required, name='dispatch')   
class List_interacoes(ListView):
    model = NPS
    context_object_name= 'interacoes'
    template_name = 'indicador/interacoes.html'

    def get_queryset(self):
        funcionario = self.request.user.usuario
        data_month = datetime.now().month
        data_year = datetime.now().year
        return NPS.objects.filter(
            Q(funcionario=funcionario) &
            Q(data__year=data_year) &
            (Q(data__month=data_month) | Q(data__month=data_month - 1))
                ).order_by('-data')
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = [
                {
                    'interacao': interacao.interacao,
                    'funcionario': interacao.funcionario.nome,
                    'data': interacao.data,
                    'nota': interacao.nota
                }
                for interacao in context['interacoes']

            ]
            return JsonResponse({'resultados': data})
        return super().render_to_response(context, **response_kwargs)

    

def get_nps_context(ano):
    for funcionario in Usuario.objects.all():
        for mes in range(1, 13):
            historico_nps = HistoricoNPS.objects.filter(
                funcionario=funcionario, data__month=mes, data__year=ano
            ).first()

            # Calcula os totais do mês para o funcionário
            totais = NPS.objects.filter(funcionario=funcionario).first()

            if not totais:
                continue
            else:
                promotores_mes = totais.calculo_promotores_mes(mes,ano) or 0
                detratores_mes = totais.calculo_detratores_mes(mes,ano) or 0
                neutros_mes = totais.calculo_neutros_mes(mes,ano) or 0

            if historico_nps:
                # Se já existe, soma os novos valores aos antigos
                historico_nps.promotores += promotores_mes
                historico_nps.detratores += detratores_mes
                historico_nps.neutros += neutros_mes
                historico_nps.save()
            else:
                # Se não existe, cria um novo registro com os totais
                HistoricoNPS.objects.create(
                    funcionario=funcionario,
                    promotores=promotores_mes,
                    detratores=detratores_mes,
                    neutros=neutros_mes,
                    data=datetime(ano, mes, 1)  # Define o primeiro dia do mês
                )



def pesquisar_interacoes(request):
    query = request.GET.get('pesquisaInteracoes', '').strip()
    funcionario = request.user.usuario  # Obtém o usuário autenticado
    data_month = datetime.now().month
    data_year = datetime.now().year

    if query:
        # Filtrar apenas pelas interações do funcionário logado
        interacoes = NPS.objects.filter(
            Q(funcionario=funcionario) & Q(interacao__icontains=query)
        )
    else:
        
        interacoes = NPS.objects.filter(
            Q(funcionario=funcionario) &
            Q(data__year=data_year) &
            (Q(data__month=data_month) | Q(data__month=data_month - 1))
        ).order_by('-data')

    
    data = [
        {
            'interacao': interacao.interacao,
            'funcionario': interacao.funcionario.nome,
            'data': interacao.data.strftime('%d/%m/%Y'),
            'nota': interacao.nota,  
        }
        for interacao in interacoes
    ]

    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'resultados': data})

    # Renderiza a página normalmente para requisições padrão
    return render(request, 'interacoes.html', {'resultados': data})

MESES_NOMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
def ler_excel_interlucutores(file):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
       processar_interlucotores(row, 'AT', 'Destinatarios', 'CC', Interlocutores)

def pesquisar_interlocutores(request):
    query_at = request.GET.get('pesquisar_at','').strip()
    

    if query_at:
        interlocutores = Interlocutores.objects.filter(
            at__icontains=query_at)
        print(interlocutores)
        
    else:
        interlocutores = Interlocutores.objects.all()
    data = []
    for interlocutor in interlocutores:
        data.append({
            'id': interlocutor.id,
            'at': interlocutor.at,  # Certifique-se de que o nome do campo está correto
            'destinatarios': interlocutor.destinatarios,
            'cc': interlocutor.cc
        })
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'resultados': data})
    return render(request, 'pesquisar_interlocutores.html',context={'resultados':data})





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
                for funcionario in Usuario.objects.all():
                    nps = NPS.objects.filter(funcionario=funcionario).first()
                    for mes in range(1,23):
                        if nps is not None:
                            nps.atualizar_nps(mes,2025)

                
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
        elif form_type == 'interlocutores':
            form_interlocutores = InterlocutoresUploadForm(request.POST, request.FILES)
            if form_interlocutores.is_valid():
                ficheiro = form_interlocutores.cleaned_data['arquivo']
                ler_excel_interlucutores(ficheiro)
                messages.success(request, 'Ficheiro Interlocutores carregado com sucesso!')
            else:
                messages.error(request, 'Erro ao carregar o ficheiro Interlocutores.')
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
    return data_value.year
    
    

def ler_excel_nps(file):
    df = pd.read_excel(file)
    

    # Processar FrontOfficeNPS
    for _, row in df.iterrows():
        processar_nps(row, 'ID_INTERACAO', 'DATA', 'Valioso', 'VALOR', FrontOfficeNPS)
        
    for _, row in df.iterrows():
        processar_nps(row, 'ID_INTERACAO.1', 'DATA.1', 'Valioso.1', 'VALOR.1', BackOfficeNPS)
    
    




def processar_interlucotores(row, AT, Destinatarios, CC, modelo_interlocutores):
    at = row.get(AT)
    destinatarios = row.get(Destinatarios)
    cc = row.get(CC)
    if not at or str(at).strip() == '':
        return
    
    if modelo_interlocutores.objects.filter(at=at).exists():
        modelo = modelo_interlocutores.objects.get(at=at)
        modelo.destinatarios = destinatarios
        if not cc or str(cc).strip() == '':
            cc = ""
        modelo.cc = cc
        modelo.save()
        return

    modelo_interlocutores.objects.create(at=at, destinatarios=destinatarios, cc=cc)

def editar_interlocutores(request):
    if request.method == 'POST':
        interlocutor_id = request.POST.get('id')
        at = request.POST.get('at')
        destinatarios = request.POST.get('destinatarios')
        cc = request.POST.get('cc')

        interlocutores = get_object_or_404(Interlocutores, at=at)
        interlocutores.at = at
        interlocutores.destinatarios = destinatarios
        interlocutores.cc = cc
        interlocutores.save()

        return JsonResponse({'success': True})
    return JsonResponse({'status':'error'},status=400)


class InterlocutoresCreate(CreateView):
    model = Interlocutores
    form_class = InterlocutoresForm
    template_name = 'indicador/interlocutores_create.html'
    success_url = reverse_lazy('pesquisar_interlocutores')


def eliminar_interlocutores(request, id):
    interlocutores = get_object_or_404(Interlocutores, pk=id)
    interlocutores.delete()
    return redirect('pesquisar_interlocutores')