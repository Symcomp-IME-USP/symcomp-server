import pytest
from pytest_bdd import given, when, then, scenario
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def usuario_dados():
    return {
        "username": "joao",
        "email": "joao@example.com",
        "password": "senha_segura",
        "name": "João Vitor Fernandes Domingues"
    }

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Novo usuário faz cadastro com sucesso')
def test_cadastro_usuario():
    pass

@given('que João está acessando pela primeira vez')
def nenhum_usuario_joao_existe():
    User.objects.filter(username="joao").delete()

@when('ele preenhce as informações solicitadas')
def envia_dados_de_cadastro(client, usuario_dados):
    resposta = client.post("/api/register/", data=usuario_dados)
    assert resposta.status_code == 201

@then('ele deve estar logado na plataforma')
def verifica_autenticacao_automatica(client, usuario_dados):
    resposta = client.post("/api/token/", data={
        "username": usuario_dados["username"],
        "password": usuario_dados["password"]
    })
    assert resposta.status_code == 200
    assert "access" in resposta.data
