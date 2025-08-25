from django.contrib import admin
from .models import Concurso

@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('orgao', 'cargo', 'instituicao', 'ano') 
    search_fields = ('orgao', 'cargo', 'instituicao') 
    list_filter = ('instituicao', 'ano')