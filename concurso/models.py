from django.db import models

class Concurso(models.Model):
    orgao = models.CharField(max_length=200) 
    cargo = models.CharField(max_length=200) 
    ano = models.IntegerField()
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.orgao} - {self.cargo} ({self.ano})"