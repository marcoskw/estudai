from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Simulado
from materia.models import Materia
from questao.models import Questao

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def criar_simulado(request):
    if request.method == 'POST':
        # A lógica de processamento do formulário virá aqui.
        return redirect('historico_simulados')
    
    # Busca todas as matérias e seus assuntos relacionados
    materias_com_assuntos = Materia.objects.prefetch_related('assunto_set').all().order_by('nome')
    
    return render(request, 'criar_simulado.html', {'materias_com_assuntos': materias_com_assuntos})
