from django.db import models
from django.contrib.auth.models import User
from questao.models import Questao

class Simulado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    questoes = models.ManyToManyField(Questao)

    def __str__(self):
        return f"Simulado de {self.usuario.username} - {self.nome}"