from django.db import models

class Link(models.Model):
    domain = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.domain

class Palestrante(models.Model):
    nome = models.CharField(max_length=255)
    ocupacao = models.CharField(max_length=255)
    biografia = models.TextField()
    email = models.EmailField()
    link_apresentacao = models.URLField()
    foto_url = models.URLField()
    foto_alt = models.CharField(max_length=255)
    links = models.ManyToManyField(Link, related_name="palestrantes")

    def __str__(self):
        return self.nome
