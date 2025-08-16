import pytest
from pytest_bdd import given, when, then, scenario
from api.models import User
from django.core import mail
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def usuario_dados():
    return {
        "email": "joao@example.com",
        "password": "SenhaSegura123",
        "name": "João Vitor Fernandes Domingues"
    }

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Usuário preenche cadastro e recebe código de validação')
def test_usuario_recebe_codigo_de_validacao():
    pass

@given('que João está acessando pela primeira vez')
def nenhum_usuario_joao_existe():
    User.objects.filter(email="joao@example.com").delete()

@when('ele preenche corretamente as informações solicitadas para cadastro')
def envia_dados_de_cadastro(client, usuario_dados):
    resposta = client.post("/api/register/", data=usuario_dados)
    assert resposta.status_code == 201

@then('ele deve receber um e-mail contendo um código de validação')
def verifica_envio_email_codigo():
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == ["joao@example.com"]
