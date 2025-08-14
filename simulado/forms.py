from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUsuario

class FormularioRegistro(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsuario
        fields = UserCreationForm.Meta.fields + (
            'nome_completo', 'foto_de_perfil', 'uf', 'cidade', 'data_nascimento', 'media', 'foco', 'sobre_mim',
        )

class FormularioEdicaoUsuario(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUsuario
        fields = UserChangeForm.Meta.fields