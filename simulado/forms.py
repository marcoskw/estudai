from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUsuario

class FormularioRegistro(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsuario
        # Herda os campos padrão e adiciona os seus campos personalizados
        fields = UserCreationForm.Meta.fields + (
            'email', 'nome_completo', 'foto_de_perfil', 'uf', 'cidade', 
            'data_nascimento', 'foco', 'sobre_mim',
        )

class FormularioEdicaoUsuario(UserChangeForm):
    password = None

    class Meta:
        model = CustomUsuario
        fields = (
            'nome_completo', 'email', 'foto_de_perfil', 'uf', 'cidade',
            'data_nascimento', 'foco', 'sobre_mim',
        )
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }