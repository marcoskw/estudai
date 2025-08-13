from django.db import models

class Concurso(models.Model):
    nome = models.CharField(max_length=200)
    ano = models.IntegerField()
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.ano})"