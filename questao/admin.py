from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Questao

@admin.register(Questao)
class QuestaoAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'enunciado',
        'alternativa_a',
        'alternativa_b',
        'alternativa_c',
        'alternativa_d',
        'alternativa_e'
    )
    list_display = ('id', 'concurso', 'materia', 'assunto', 'resposta_correta')
    list_filter = ('concurso', 'materia', 'assunto')
    search_fields = ('enunciado', 'concurso__nome', 'materia__nome')