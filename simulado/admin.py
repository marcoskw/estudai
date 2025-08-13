from django.contrib import admin
from .models import Simulado
from respostausuario.models import RespostaUsuario

# Inline para exibir as respostas de um simulado na página do Simulado
class RespostaUsuarioInline(admin.TabularInline):
    model = RespostaUsuario
    extra = 0
    readonly_fields = ('questao', 'alternativa_escolhida', 'correta')

@admin.register(RespostaUsuario)
class RespostaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('simulado', 'questao', 'alternativa_escolhida', 'correta')
    list_filter = ('correta',)
    
@admin.register(Simulado)
class SimuladoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome', 'data_criacao')
    list_filter = ('usuario', 'data_criacao')
    inlines = [RespostaUsuarioInline]

