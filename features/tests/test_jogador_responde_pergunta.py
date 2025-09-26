import pytest
from pytest_bdd import given, when, then, scenario
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from desafio.models import Desafio
from desafio.questao.models import Questao
from api.models import PerfilUsuario, Papel

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario('../jogador_responde_pergunta.feature', 'Jogador responde corretamente a uma pergunta')
def test_jogador_responde_corretamente_a_uma_pergunta():
    pass

@given("que existe um jogador")
def criar_jogador(contexto):
    user = User.objects.create_user(email="jogador@example.com", name="Jogador", password="123")
    perfil = PerfilUsuario.objects.create(user=user, papel=Papel.PARTICIPANTE, pontos=0)
    contexto["user"] = user
    contexto["perfil"] = perfil
    return contexto

@given("que existe um desafio")
def criar_desafio(contexto):
    desafio = Desafio.objects.create(titulo="Desafio Teste", descricao="Teste do desafio")
    contexto["desafio"] = desafio
    return contexto

@given("que existe perguntas no desafio")
def criar_questao(contexto):
    questao = Questao.objects.create(
        pergunta="2 + 2 = ?",
        resposta="4",
        valor_pontos=10,
        desafio=contexto["desafio"]
    )
    contexto["questao"] = questao
    return contexto

@when("ele responde a uma pergunta")
def responder_pergunta(client, contexto):
    user = contexto["user"]
    client.force_authenticate(user=user)
    resposta = {"resposta": "4"}
    response = client.post(f"/questoes/{contexto['questao'].id}/responder/", resposta, format="json")
    contexto["response"] = response
    return contexto

@when("ela está correta")
def verificar_resposta_correta(contexto):
    response = contexto["response"]
    assert response.status_code == 200
    assert response.data["resposta_correta"] is True

@then("ele deve receber pontos pelo acerto")
def verificar_pontuacao(contexto):
    perfil = PerfilUsuario.objects.get(user=contexto["user"])
    assert perfil.pontos == 10
