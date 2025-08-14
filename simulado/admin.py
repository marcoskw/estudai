from django.contrib import admin
from .models import Simulado
from respostausuario.models import RespostaUsuario
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import FormularioRegistro, FormularioEdicaoUsuario
from .models import CustomUsuario


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

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = FormularioRegistro
    form = FormularioEdicaoUsuario
    model = CustomUsuario
    
    # Define quais campos aparecerão na lista de usuários
    list_display = (
        'username', 'email', 'nome_completo', 'uf', 'cidade', 'is_staff'
    )
    
    # Define os campos que aparecerão ao editar um usuário existente
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Pessoais', {'fields': ('nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'foco', 'sobre_mim', 'media',)}),
    )
    
    # Define os campos que aparecerão ao adicionar um novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Pessoais', {'fields': ('nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'foco', 'sobre_mim',)}),
    )