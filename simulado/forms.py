from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUsuario

class FormularioRegistro(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsuario
        fields = UserCreationForm.Meta.fields + (
            'nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'media', 'foco', 'sobre_mim',
        )

class FormularioEdicaoUsuario(UserChangeForm):
    password = None  # Remove o campo de senha do formulário

    class Meta:
        model = CustomUsuario
        # Define os campos que o usuário poderá editar
        fields = (
            'nome_completo',
            'email',
            'foto_de_perfil',
            'uf',
            'cidade',
            'data_nascimento',
            'foco',
            'sobre_mim',
        )
        # Adiciona um widget para que o campo de data seja exibido como um seletor de data
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }