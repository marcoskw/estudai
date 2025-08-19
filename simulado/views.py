import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.db.models import Count, Case, When, IntegerField, Avg, Prefetch
from django.contrib import messages
from respostausuario.models import RespostaUsuario
from assunto.models import Assunto
from concurso.models import Concurso
from simulado.models import Simulado
from materia.models import Materia
from questao.models import Questao
from simulado.forms import FormularioEdicaoUsuario
from django.db.models import Sum
from django.utils import timezone


# Create your views here.
@login_required
def home(request):
    # Quantidade total de questões no sistema
    total_questoes = Questao.objects.count()
    
    context = {
        'total_questoes': total_questoes
    }

    # Se o usuário estiver autenticado, busca a média de acertos dele
    if request.user.is_authenticated:
        # Pega todas as respostas do usuário
        respostas_usuario = RespostaUsuario.objects.filter(simulado__usuario=request.user)
        
        # Calcula a média de acertos
        media_acertos = 0
        if respostas_usuario.exists():
            media_acertos = respostas_usuario.aggregate(
                avg=Avg(
                    Case(When(correta=True, then=1), default=0, output_field=IntegerField())
                )
            )['avg'] * 100
            
        context['media_acertos'] = media_acertos

        # Calcula a média de acertos por matéria
        if respostas_usuario.exists():
            medias_por_materia = respostas_usuario.values('questao__materia__nome').annotate(
                media_materia=Avg(Case(When(correta=True, then=1), default=0, output_field=IntegerField())) * 100
            ).order_by('questao__materia__nome')
        else:
            medias_por_materia = []
        
        context['medias_por_materia'] = medias_por_materia
        
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def minha_conta(request):
    if request.method == 'POST':
        # Popula o formulário com os dados enviados e os arquivos (para a foto)
        form = FormularioEdicaoUsuario(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('minha_conta')
    else:
        # Exibe o formulário preenchido com os dados atuais do usuário
        form = FormularioEdicaoUsuario(instance=request.user)
        
    return render(request, 'minha_conta.html', {'form': form})

@login_required
def listar_provas(request):
    """
    View para listar todos os concursos (provas) com filtros.
    """
    # Parâmetros de busca e filtro
    query = request.GET.get('q')
    instituicao_filtro = request.GET.get('instituicao')
    ano_filtro = request.GET.get('ano')

    concursos = Concurso.objects.annotate(
        num_questoes=Count('questao')
    ).order_by('-ano', 'nome')

    # Aplica os filtros se eles existirem
    if query:
        concursos = concursos.filter(nome__icontains=query)
    if instituicao_filtro:
        concursos = concursos.filter(instituicao=instituicao_filtro)
    if ano_filtro:
        concursos = concursos.filter(ano=ano_filtro)

    provas_info = []
    for concurso in concursos:
        materias = Materia.objects.filter(
            questao__concurso=concurso
        ).distinct().values_list('nome', flat=True)
        
        provas_info.append({
            'concurso': concurso,
            'materias': list(materias),
        })

    # Busca as opções para os filtros
    instituicoes = Concurso.objects.values_list('instituicao', flat=True).distinct().order_by('instituicao')
    anos = Concurso.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        
    context = {
        'provas': provas_info,
        'instituicoes': instituicoes,
        'anos': anos,
        'query_atual': query or "",
        'instituicao_atual': instituicao_filtro or "",
        'ano_atual': int(ano_filtro) if ano_filtro else "",
    }
    return render(request, 'listar_provas.html', context)

@login_required
def detalhes_prova(request, pk):
    """
    View para exibir os detalhes de um concurso (prova) específico.
    """
    concurso = get_object_or_404(Concurso, pk=pk)
    
    # Busca todas as questões do concurso, ordenadas por matéria
    questoes = Questao.objects.filter(concurso=concurso).order_by('materia__nome')
    
    # Agrupa as questões por matéria
    questoes_por_materia = {}
    for questao in questoes:
        materia = questao.materia.nome
        if materia not in questoes_por_materia:
            questoes_por_materia[materia] = []
        questoes_por_materia[materia].append(questao)
        
    context = {
        'concurso': concurso,
        'questoes_por_materia': questoes_por_materia,
    }
    return render(request, 'detalhes_prova.html', context)

@login_required
def historico_simulados(request):
    simulados_do_usuario = Simulado.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    historico = []
    
    for simulado in simulados_do_usuario:
        # Pega todas as respostas do simulado atual
        respostas = RespostaUsuario.objects.filter(simulado=simulado)
        
        # O campo tempo_levado é definido como 0 para evitar o AttributeError.
        # Ele só será calculado se os campos data_fim e data_inicio existirem no modelo.
        tempo_levado = 0
            
        # Calcula a nota total do simulado
        total_questoes = respostas.count()
        acertos = respostas.filter(correta=True).count()
        nota_total = (acertos / total_questoes) * 100 if total_questoes > 0 else 0
        
        # Agrupa as notas por matéria
        notas_por_materia = respostas.values('questao__materia__nome').annotate(
            total_por_materia=Count('id'),
            acertos_por_materia=Count(Case(When(correta=True, then=1), output_field=IntegerField())),
            nota_por_materia=Avg(Case(When(correta=True, then=1), default=0, output_field=IntegerField())) * 100
        )
        
        historico.append({
            'simulado': simulado,
            'tempo_levado': tempo_levado,
            'nota_total': nota_total,
            'notas_por_materia': notas_por_materia
        })
        
    return render(request, 'historico_simulados.html', {'historico': historico})

@login_required
def criar_simulado(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        duracao = request.POST.get('duracao-simulado')
        assuntos_ids = [int(key.split('-')[1]) for key, value in request.POST.items() if key.startswith('assunto-') and value == 'on']
        
        # Cria um nome para o simulado
        nome_simulado = f"Simulado em {timezone.now().strftime('%d/%m/%Y %H:%M')}"
        
        # Seleciona as questões de forma aleatória, respeitando a quantidade por matéria
        questoes_selecionadas = []
        materias_e_questoes = {key.split('-')[1]: int(value) for key, value in request.POST.items() if key.startswith('questoes-')}
        
        for materia_id, num_questoes in materias_e_questoes.items():
            assuntos_da_materia = Assunto.objects.filter(materia_id=materia_id, id__in=assuntos_ids)
            questoes_da_materia = Questao.objects.filter(assunto__in=assuntos_da_materia)
            
            # Se tiver mais questões que o desejado, sorteia
            if questoes_da_materia.count() > num_questoes:
                questoes_selecionadas.extend(random.sample(list(questoes_da_materia), num_questoes))
            else:
                questoes_selecionadas.extend(list(questoes_da_materia))
                
        if not questoes_selecionadas:
            messages.error(request, "Não foi possível gerar um simulado. Por favor, selecione assuntos que contenham questões.")
            return redirect('criar_simulado')

        # Cria o objeto Simulado
        novo_simulado = Simulado.objects.create(
            usuario=request.user,
            nome=nome_simulado,
            duracao_simulado=duracao # Adicionar este campo no modelo
        )
        novo_simulado.questoes.set(questoes_selecionadas)
        
        return redirect('iniciar_simulado', pk=novo_simulado.pk)
    
    # Se o método for GET, exibe a página de criação
    materias_com_assuntos = Materia.objects.annotate(num_questoes=Count('questao')).prefetch_related(Prefetch('assunto_set', queryset=Assunto.objects.annotate(num_questoes=Count('questao')).order_by('nome'))).order_by('nome')
    return render(request, 'criar_simulado.html', {'materias_com_assuntos': materias_com_assuntos})

@login_required
def iniciar_simulado(request, pk):
    simulado = get_object_or_404(Simulado, pk=pk, usuario=request.user)
    
    # Agrupa as questões do simulado por matéria para exibição
    questoes_por_materia = {}
    for questao in simulado.questoes.all().order_by('materia__nome', 'assunto__nome', 'id'):
        materia_nome = questao.materia.nome
        if materia_nome not in questoes_por_materia:
            questoes_por_materia[materia_nome] = []
        questoes_por_materia[materia_nome].append(questao)
        
    context = {
        'simulado': simulado,
        'questoes_por_materia': questoes_por_materia,
    }
    return render(request, 'iniciar_simulado.html', context)

@login_required
def finalizar_simulado(request, pk):
    if request.method == 'POST':
        simulado = get_object_or_404(Simulado, pk=pk, usuario=request.user)
        
        # Limpa respostas anteriores para o simulado
        RespostaUsuario.objects.filter(simulado=simulado).delete()
        
        # Processa as respostas do usuário
        for questao in simulado.questoes.all():
            alternativa_escolhida = request.POST.get(f'questao-{questao.pk}')
            if alternativa_escolhida:
                correta = (alternativa_escolhida == questao.resposta_correta)
                RespostaUsuario.objects.create(
                    simulado=simulado,
                    questao=questao,
                    alternativa_escolhida=alternativa_escolhida,
                    correta=correta
                )
        
        return redirect('resultado_simulado', pk=simulado.pk)

    # Caso seja um GET inesperado, redireciona para a home
    return redirect('home')

@login_required
def resultado_simulado(request, pk):
    simulado = get_object_or_404(Simulado, pk=pk, usuario=request.user)
    respostas = RespostaUsuario.objects.filter(simulado=simulado).select_related('questao')

    # Calcula as estatísticas gerais
    total_questoes = simulado.questoes.count()
    acertos = respostas.filter(correta=True).count()
    erros = respostas.filter(correta=False).count()
    nota_total = (acertos / total_questoes) * 100 if total_questoes > 0 else 0

    # Agrupa as notas por matéria
    notas_por_materia = respostas.values('questao__materia__nome').annotate(
        total_por_materia=Count('id'),
        acertos_por_materia=Count(Case(When(correta=True, then=1), output_field=IntegerField())),
        nota_por_materia=Avg(Case(When(correta=True, then=1), default=0, output_field=IntegerField())) * 100
    ).order_by('questao__materia__nome')

    context = {
        'simulado': simulado,
        'respostas': respostas,
        'total_questoes': total_questoes,
        'acertos': acertos,
        'erros': erros,
        'nota_total': nota_total,
        'notas_por_materia': notas_por_materia,
    }
    return render(request, 'resultado_simulado.html', context)