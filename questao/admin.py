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
        'alternativa_e',
        'comentario_resposta',
    )
    list_display = ('id', 'materia', 'assunto', 'concurso', 'resposta_correta')
    list_filter = ('materia', 'assunto', 'concurso')
    search_fields = ('enunciado', 'concurso__nome', 'materia__nome')
    
    # Adicionado para campos de busca em vez de select
    autocomplete_fields = ['concurso', 'materia', 'assunto']

    # Adicionado para organizar os campos do formulário
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('materia', 'assunto', 'concurso')
        }),
        ('Conteúdo da Questão', {
            'fields': ('enunciado', ('alternativa_a', 'alternativa_b'), ('alternativa_c', 'alternativa_d'), 'alternativa_e')
        }),
        ('Gabarito e Comentários', {
            'fields': ('resposta_correta', 'comentario_resposta')
        }),
    )

    class Media:
        js = ('admin/js/admin_filtering.js',)