from django.db import models

class Desafio(models.Model):
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo