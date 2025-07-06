import pytest
from pytest_bdd import given, when, then, scenario
from api.models import User, EmailVerificationCode
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

@pytest.fixture
def codigo_verificacao():
    return "123456"

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Usuário valida código e efetiva login')
def test_cadastro_com_sucesso():
    pass

@given('que João recebeu o código de validação por e-mail')
def joao_recebeu_codigo_valido(client, usuario_dados, codigo_verificacao):
    response = client.post("/api/register/", data=usuario_dados)
    assert response.status_code == 201

    user = User.objects.get(email=usuario_dados["email"])

    EmailVerificationCode.objects.create(user=user, code=codigo_verificacao)

@when('ele informa corretamente o código recebido')
def envia_codigo_valido(client, usuario_dados, codigo_verificacao):
    response = client.post("/api/validate-code/", data={
        "email": usuario_dados["email"],
        "code": codigo_verificacao,
    })
    assert response.status_code == 200

@then('ele deve estar logado na plataforma')
def verifica_token_login(client, usuario_dados):
    response = client.post("/api/token/", data={
        "email": usuario_dados["email"],
        "password": usuario_dados["password"],
    })
    assert response.status_code == 200
    assert "access" in response.data
