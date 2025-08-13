from django.db import models
from .models import Simulado, Questao

class RespostaUsuario(models.Model):
    simulado = models.ForeignKey(Simulado, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    alternativa_escolhida = models.CharField(max_length=1)
    correta = models.BooleanField()
    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resposta de {self.simulado.usuario.username} para Questão {self.questao.id}"