from django.db import models
from desafio.models import Desafio

class Questao(models.Model):
    pergunta = models.CharField(max_length=255)
    resposta = models.CharField(max_length=255)
    valor_pontos = models.DecimalField(max_digits=10, decimal_places=2)

    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.CASCADE,
        related_name="questoes"
    )

    def __str__(self):
        return self.pergunta
