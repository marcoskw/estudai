from django.db import models
from concurso.models import Concurso 
from materia.models import Materia 
from assunto.models import Assunto

class Questao(models.Model):
    OPCOES_RESPOSTA = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    enunciado = models.TextField()
    alternativa_a = models.TextField()
    alternativa_b = models.TextField()
    alternativa_c = models.TextField()
    alternativa_d = models.TextField()
    alternativa_e = models.TextField()
    resposta_correta = models.CharField(max_length=1, choices=OPCOES_RESPOSTA)
    comentario_resposta = models.TextField(blank=True, null=True)
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Questão {self.id} de {self.concurso.nome}"