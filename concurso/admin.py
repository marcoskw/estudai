from django.contrib import admin
from .models import Concurso

@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'ano')
    search_fields = ('nome', 'instituicao')