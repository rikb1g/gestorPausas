import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages 
from django.shortcuts import render
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from .models import FrontOfficeNPS,BackOfficeNPS,NPS ,HistoricoNPS, Interlocutores
from .forms import RechamadaUploadForm,ProvisoriosUploadForm, NpsFileUploadForm, InterlocutoresUploadForm, InterlocutoresForm
from apps.usuarios.models import Usuario, Equipas
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from datetime import datetime
import pandas as pd
from django.db import transaction




@method_decorator(login_required, name='dispatch')
class frontoffice_nps(ListView):
    model = NPS
    context_object_name= 'nps_individual'
    template_name = 'indicadores/nps_list.html'

    def get_queryset(self):
        funcionario_filter = self.request.GET.get('utilizador')
        if funcionario_filter:
            funcionario = get_object_or_404(Usuario, pk=funcionario_filter)
        else:
            funcionario = self.request.user.usuario
        return NPS.objects.filter(funcionario=funcionario)
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['indicadores/nps_list_partial.html']
        return ['indicadores/nps_list.html']     
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        funcionario = self.request.user.usuario

        funcionario_filter = self.request.GET.get('utilizador')
        if funcionario_filter:
            funcionario = get_object_or_404(Usuario,pk=funcionario_filter)
        is_supervisor = funcionario.supervisor
        print(is_supervisor)
        print("superivor ")




        equipa_utilizador = Usuario.objects.filter(equipa=funcionario.equipa)
        nps_intancia_superivor = HistoricoNPS.objects.filter(funcionario__in=equipa_utilizador).first()
    
        nps_intancia = HistoricoNPS.objects.filter(funcionario=funcionario).first()
        nps_instanca_superisor = HistoricoNPS.objects.filter().first()
        ano = datetime.now().year
        utilizadores = Usuario.objects.filter().order_by('nome')
        context['utilizadores'] = utilizadores     
        meses_nomes_ajustados = {mes: nome for mes, nome in MESES_NOMES.items()}
        context['meses'] = meses_nomes_ajustados

        if is_supervisor:
            print("supervisor")
            if nps_intancia_superivor:
                nps_por_mes_supervisor = {
                    mes: HistoricoNPS.calculo_nps_mes_supervior(mes, ano, funcionario) for mes in range(1, 13)
                }
                nps_global_mes_sup = {
                    mes: HistoricoNPS.calculo_nps_global_mensal_sup(mes, ano) for mes in range(1, 13)
                }
                nps_por_equipa_mensal = {
                    mes: HistoricoNPS.calculo_nps_global_equipa(mes, ano) for mes in range(1, 13)
                }
            else:
                print("filtrado nos supervisores")
                nps_por_mes_supervisor = {mes: "-" for mes in range(1, 13)}
                nps_global_mes_sup = {mes: "-" for mes in range(1, 13)}

            context['nps_por_mes'] = nps_por_mes_supervisor
            context['promotores_mes'] = {mes: HistoricoNPS.promotores_supervisor(mes, ano, funcionario) or 0 for mes in
                                        range(1, 13)}
            context['detratores_mes'] = {mes: HistoricoNPS.detratores_supervisor(mes, ano, funcionario) or 0 for mes
                                             in range(1, 13)}
            context['neutros_mes'] = {mes: HistoricoNPS.neutros_supervisor(mes, ano, funcionario) or 0 for mes in
                                          range(1, 13)}
            context['nps_mes_json'] = json.dumps(nps_por_mes_supervisor)
            context['nps_mes_global_json'] = json.dumps(nps_global_mes_sup)
            context['nps_equipa_json'] = json.dumps(nps_por_equipa_mensal)
            
           
        else:
            context['promotores_mes'] = {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_promotores=Sum('promotores'))['total_promotores'] or 0
                for mes in range(1, 13)
            }
            context['detratores_mes'] = {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_detratores=Sum('detratores'))['total_detratores'] or 0
                for mes in range(1, 13)
            }
            context['neutros_mes'] = {
                mes: HistoricoNPS.objects.filter(
                    funcionario=funcionario,
                    data__month=mes,
                    data__year=ano
                ).aggregate(total_neutros=Sum('neutros'))['total_neutros'] or 0
                for mes in range(1, 13)
            }
            if nps_intancia:
                nps_por_mes = {
                    mes: nps_intancia.calculo_nps_mensal(mes, ano) for mes in range(1, 13)
                }
                nps_por_mes_global = {
                    mes: nps_intancia.calculo_nps_global_mensal(mes, ano) for mes in range(1, 13)
                }
                nps_por_equipa_mensal = {
                    mes: nps_intancia.calculo_nps_global_equipa(mes, ano) for mes in range(1, 13)
                }

            else:
                nps_por_mes = {mes: "-" for mes in range(1, 13)}
                nps_por_mes_global = {mes: "-" for mes in range(1, 13)}
                nps_por_equipa_mensal = {mes: "-" for mes in range(1, 13)}

            context['nps_por_mes'] = nps_por_mes
            context['nps_por_mes_global'] = nps_por_mes_global
            context['nps_mes_json'] = json.dumps(nps_por_mes)
            context['nps_mes_global_json'] = json.dumps(nps_por_mes_global)
            context['nps_equipa_json'] = json.dumps(nps_por_equipa_mensal)

        equipa_utilizador = self.request.user.usuario.equipa

        equipas = Equipas.objects.all()
        lista_equipas = []
        lista_equipas = [{'id': equipa.lider.id, 'nome': equipa.lider.nome} for equipa in equipas]
        context['equipas'] = lista_equipas
        
        dados_nps = {}
        for equipa in equipas:
            dados_nps[equipa.lider.nome] = {
                mes : HistoricoNPS.calculo_nps_mes_supervior(mes,ano,equipa.lider) for mes in range(1,13)
            }
            
        
        context['nps_mensal_superivor'] = json.dumps(dados_nps)

        return context
    

def frontoffice_nps_json(request):
    funcionario_filter = request.GET.get('utilizador')
    print(funcionario_filter)
    if funcionario_filter:
        funcionario = get_object_or_404(Usuario, pk=funcionario_filter)
    else:
        funcionario = request.user.usuario

    ano = datetime.now().year
    meses_nomes_ajustados = {mes: nome for mes, nome in MESES_NOMES.items()}

    promotores_mes = {
        mes: HistoricoNPS.objects.filter(funcionario=funcionario, data__month=mes, data__year=ano)
            .aggregate(total_promotores=Sum('promotores'))['total_promotores'] or 0
        for mes in range(1, 13)
    }
    neutros_mes = {
        mes: HistoricoNPS.objects.filter(funcionario=funcionario, data__month=mes, data__year=ano)
            .aggregate(total_neutros=Sum('neutros'))['total_neutros'] or 0
        for mes in range(1, 13)
    }
    detratores_mes = {
        mes: HistoricoNPS.objects.filter(funcionario=funcionario, data__month=mes, data__year=ano)
            .aggregate(total_detratores=Sum('detratores'))['total_detratores'] or 0
        for mes in range(1, 13)
    }
    nps_por_mes = {}
    nps_intancia = HistoricoNPS.objects.filter(funcionario=funcionario).first()
    if nps_intancia:
        nps_por_mes = {mes: nps_intancia.calculo_nps_mensal(mes, ano) for mes in range(1, 13)}
        nps_por_mes_global = {mes: nps_intancia.calculo_nps_global_mensal(mes, ano) for mes in range(1, 13)}
        nps_equipa_por_mes = {mes: nps_intancia.calculo_nps_global_equipa(mes, ano) for mes in range(1, 13)}
    else:
        nps_por_mes = {mes: "-" for mes in range(1, 13)}
        nps_por_mes_global = {mes: "-" for mes in range(1, 13)}
        nps_equipa_por_mes = {mes: "-" for mes in range(1, 13)}
    
   
    return JsonResponse({
        "meses": meses_nomes_ajustados,
        "promotores_mes": promotores_mes,
        "neutros_mes": neutros_mes,
        "detratores_mes": detratores_mes,
        "nps_por_mes": nps_por_mes,
        "nps_global_por_mes": nps_por_mes_global,
        "nps_equipa_por_mes": nps_equipa_por_mes,

    })

@method_decorator(login_required, name='dispatch')   
class List_interacoes(ListView):
    model = NPS
    context_object_name= 'interacoes'
    template_name = 'indicadores/interacoes.html'

    def get_queryset(self, **kwargs):
        if self.request.user.usuario.supervisor:
            supervisor = self.request.user.usuario
            equipa = Usuario.objects.filter(equipa=supervisor.equipa)
            data_month = datetime.now().month
            data_year = datetime.now().year
            if supervisor:
                return NPS.objects.filter(
                    Q(funcionario__in=equipa) &
                    Q(data__year=data_year) &
                    (Q(data__month=data_month) | Q(data__month=data_month - 1)) &
                    (Q(nota__lt=7))
                        ).order_by('-data')[:300]
        else:
            funcionario = self.request.user.usuario
            data_month = datetime.now().month
            data_year = datetime.now().year
            return NPS.objects.filter(
                Q(funcionario=funcionario) &
                Q(data__year=data_year) &
                (Q(data__month=data_month) | Q(data__month=data_month - 1))
                     ).order_by('-data')[:300]
    
    def get_template_names(self):
        if self.request.headers.get('HX-Request') or self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['indicadores/interacoes_partial.html']
        return ['indicadores/interacoes.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['utilizadores'] = Usuario.objects.filter().order_by('nome')
        return context
    
def pesquisar_interacoes_json(request):
    id_utilizador = request.GET.get('utilizador')
    nota_get = request.GET.get('nota')
    resultados =[]
    if id_utilizador:
        queryset = NPS.objects.filter(funcionario_id=id_utilizador)

        if nota_get and nota_get != "0":
            if nota_get == "1":
                queryset = queryset.filter(nota__gte=9)
            elif nota_get == "2":
                queryset = queryset.filter(nota__gte=7, nota__lt=9)
            elif nota_get == "3":
                queryset = queryset.filter(nota__lt=7)
        for resultado in queryset:
            resultados.append({
                'interacao': resultado.interacao,
                'funcionario': resultado.funcionario.nome,
                'data': resultado.data,
                'nota': resultado.nota,
            })

        return JsonResponse({'success': True,'resultados': resultados})
    return JsonResponse({'success': True,'resultados': [{'id': request.user.usuario.id }]})


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
    funcionario = request.user.usuario.nome 
    data_month = datetime.now().month
    data_year = datetime.now().year

    if query:
        # Filtrar apenas pelas interações do funcionário logado
        interacoes = NPS.objects.filter(interacao__icontains=query)
    else: 
        interacoes = NPS.objects.filter(
            Q(funcionario=funcionario) &
            Q(data__year=data_year) &
            (Q(data__month=data_month) | Q(data__month=data_month - 1))
        ).order_by('-data')[:300]

    
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
    
    if query_at:
        return JsonResponse({"success": True ,'resultados': data})
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'indicadores/pesquisar_interlocutores_partial.html',context={'resultados':data})
    return render(request, 'indicadores/pesquisar_interlocutores.html',context={'resultados':data})





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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'indicadores/upload_partial.html', contex)
    return render(request, 'indicadores/upload.html', contex)


            

def processar_nps(row, interacao_col, data_col, valioso_col, valor_col, existentes, usuarios_cache, modelo_nps):
    valor_interacao = row.get(interacao_col)
    data_value = row.get(data_col)
    valioso = row.get(valioso_col)
    

    # Validar campos obrigatórios
    if not valor_interacao or not str(valor_interacao).strip():
        return None
    if not valioso or not str(valioso).strip():
        return None

    # Converter data
    if isinstance(data_value, str):
        try:
            data_value = datetime.fromisoformat(data_value)
        except ValueError:
            return None
    elif not isinstance(data_value, datetime):
        return None

    # Checar duplicados em memória
    key = (valor_interacao, valioso)
    if key in existentes:
        return None

    # Buscar ou criar usuário em memória
    usuario = usuarios_cache.get(valioso)
    if not usuario:
        usuario, _ = Usuario.objects.get_or_create(
            identificador=valioso,
            defaults={"nome": valioso, "supervisor": False}
        )
        usuarios_cache[valioso] = usuario

    existentes.add(key)

    # Criar objeto (não salva ainda)
    return modelo_nps(
        funcionario=usuario,
        nota=row.get(valor_col, 0),
        data=data_value,
        interacao=valor_interacao
    )

def ler_excel_nps(file):
    # Lê as duas folhas (índices 0 e 1 → primeira e segunda)
    sheets = pd.read_excel(file, sheet_name=['STS', 'BJ'])
    print(sheets.keys())

    # Cache de usuários
    usuarios_cache = {u.identificador: u for u in Usuario.objects.all()}

    existentes_front = set(
        FrontOfficeNPS.objects.values_list('interacao', 'funcionario__identificador')
    )
    existentes_back = set(
        BackOfficeNPS.objects.values_list('interacao', 'funcionario__identificador')
    )

    front_objs, back_objs = [], []

    # Percorre cada folha (df é um DataFrame)
    for df in sheets.values():
   

        for row in df.itertuples(index=False):
            row_dict = dict(zip(df.columns, row))

            # Encontra o campo assistente
            campo_valioso = None
            for candidato in ['Valioso', 'Agente de Beja']:
                if candidato in row_dict:
                    campo_valioso = candidato
                    break

            if not campo_valioso:
                print("Nenhuma coluna encontrada para Valioso/Agente de Beja")
                continue  # salta esta linha se não houver nenhum campo válido

            # Processa Front
            obj_front = processar_nps(
                row_dict,
                'ID_INTERACAO',
                'DATA',
                campo_valioso,       
                'VALOR',
                existentes_front,
                usuarios_cache,
                FrontOfficeNPS
            )
            if obj_front:
                front_objs.append(obj_front)

            # Processa Back
            obj_back = processar_nps(
                row_dict,
                'ID_INTERACAO.1',
                'DATA.1',
                'Valioso.1',
                'VALOR.1',
                existentes_back,
                usuarios_cache,
                BackOfficeNPS
            )
            if obj_back:
                back_objs.append(obj_back)

    # Salvar objetos linha a linha
    with transaction.atomic():
        for obj in front_objs:
            obj.save()
        for obj in back_objs:
            obj.save()

    return {
        "frontoffice_inseridos": len(front_objs),
        "backoffice_inseridos": len(back_objs)
    }




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