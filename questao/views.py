from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from questao.models import Questao
from django.db.models import Count, Case, When, IntegerField, Avg

@login_required
def visualizar_questao(request, pk):
    questao = get_object_or_404(Questao, pk=pk)
    
    context = {
        'questao': questao,
    }
    return render(request, 'visualizar_questao.html', context)