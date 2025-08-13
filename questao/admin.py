from django.contrib import admin
from .models import Questao

@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'concurso', 'materia', 'assunto', 'resposta_correta')
    list_filter = ('concurso', 'materia', 'assunto')
    search_fields = ('enunciado', 'concurso__nome', 'materia__nome')