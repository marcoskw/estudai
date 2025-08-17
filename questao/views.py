from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from questao.models import Questao
from assunto.models import Assunto
from django.http import JsonResponse
from django.db.models import Count, Case, When, IntegerField, Avg

@login_required
def get_assuntos(request, materia_id):
    assuntos = Assunto.objects.filter(materia_id=materia_id).values('id', 'nome')
    return JsonResponse(list(assuntos), safe=False)

@login_required
def visualizar_questao(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    
    context = {
        'questao': questao,
    }
    return render(request, 'visualizar_questao.html', context)