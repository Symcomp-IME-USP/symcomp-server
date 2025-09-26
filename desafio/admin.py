from django.contrib import admin
from .models import Desafio
from .questao.models import Questao

admin.site.register(Desafio)
admin.site.register(Questao)
