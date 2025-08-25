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


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = FormularioRegistro
    form = FormularioEdicaoUsuario
    model = CustomUsuario
    list_display = (
        'username', 'email', 'nome_completo', 'is_staff'
    )

    # Fieldsets para a página de EDIÇÃO de um usuário
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'foco', 'sobre_mim', 'media')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets para a página de CRIAÇÃO de um novo usuário (sincronizado com o FormularioRegistro)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2'),
        }),
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'foco', 'sobre_mim',)
        }),
    )