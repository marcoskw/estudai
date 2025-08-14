from django.db import models
from django.contrib.auth.models import User
from questao.models import Questao
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUsuario(AbstractUser):
    UF_CHOICES = (
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AM', 'Amazonas'), ('AP', 'Amapá'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'),
        ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'),
        ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')
    )
    
    nome_completo = models.CharField(max_length=255, blank=True, null=True)
    foto_de_perfil = models.ImageField(upload_to='fotos_de_perfil/', blank=True, null=True)
    uf = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    media = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) # Exemplo de campo numérico
    foco = models.CharField(max_length=255, blank=True, null=True)
    sobre_mim = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Simulado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    questoes = models.ManyToManyField(Questao)

    def __str__(self):
        return f"Simulado de {self.usuario.username} - {self.nome}"