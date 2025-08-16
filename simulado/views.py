from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from respostausuario.models import RespostaUsuario
from .models import Simulado
from materia.models import Materia
from questao.models import Questao
from django.db.models import Count, Case, When, IntegerField, Avg
from django.contrib import messages
from .forms import FormularioRegistro, FormularioEdicaoUsuario

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
            media_acertos = respostas_usuario.aggregate(Avg('correta'))['correta__avg'] * 100
            
        context['media_acertos'] = media_acertos
        
    return render(request, 'home.html', context)

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
def historico_simulados(request):
    simulados = Simulado.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'historico_simulados.html', {'simulados': simulados})

@login_required
def criar_simulado(request):
    if request.method == 'POST':
        # -------------------
        # Lógica para processar o formulário
        # -------------------
        
        # 1. Capturar a duração do simulado
        duracao_simulado = request.POST.get('duracao-simulado')
        
        # 2. Capturar as matérias e quantidade de questões
        materias_e_questoes = {}
        for key, value in request.POST.items():
            if key.startswith('questoes-'):
                materia_id = key.split('-')[1]
                materias_e_questoes[materia_id] = int(value)
        
        # 3. Capturar os assuntos selecionados
        assuntos_selecionados = []
        for key, value in request.POST.items():
            if key.startswith('assunto-'):
                assunto_id = key.split('-')[1]
                assuntos_selecionados.append(int(assunto_id))
        
        # A partir daqui, você usaria esses dados para gerar o simulado
        # Por exemplo: buscar as questões, criar o objeto Simulado, etc.
        
        # Exemplo de como você pode usar os dados:
        # Você teria a lista de assuntos e a quantidade de questões por matéria.
        # Com isso, você pode montar o simulado.
        
        print(f"Duração do simulado: {duracao_simulado} minutos")
        print(f"Matérias e questões selecionadas: {materias_e_questoes}")
        print(f"Assuntos selecionados: {assuntos_selecionados}")
        
        # Neste ponto, você pode redirecionar para a página do simulado
        # Por enquanto, apenas vamos redirecionar para a home
        return redirect('home')
    
    # Se o método for GET, exibe a página de criação
    materias_com_assuntos = Materia.objects.prefetch_related('assunto_set').all().order_by('nome')
    
    return render(request, 'criar_simulado.html', {'materias_com_assuntos': materias_com_assuntos})

@login_required
def historico_simulados(request):
    simulados_do_usuario = Simulado.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    historico = []
    
    for simulado in simulados_do_usuario:
        # Pega todas as respostas do simulado atual
        respostas = RespostaUsuario.objects.filter(simulado=simulado)
        
        # Calcula o tempo total em minutos (se você for adicionar um campo de tempo no Simulado)
        tempo_levado = 0
        if simulado.data_fim and simulado.data_inicio: # Assumindo que você terá esses campos
            duracao = simulado.data_fim - simulado.data_inicio
            tempo_levado = int(duracao.total_seconds() / 60)
            
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