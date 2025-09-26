from django.urls import path
from desafio.views import responder_questao

urlpatterns = [
    path('questoes/<int:questao_id>/responder/', responder_questao, name='responder-questao'),
]