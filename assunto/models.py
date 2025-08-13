from django.db import models
from .models import Materia

class Assunto(models.Model):
    nome = models.CharField(max_length=100)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.materia.nome})"

from django.db import models
