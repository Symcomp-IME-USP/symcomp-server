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

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario("../cadastrar_usuario.feature", "Usuário faz cadastro, mas já está cadastrado")
def test_usuario_cadastra_novamente():
    pass

@given("que João já fez seu cadastro")
def envia_dados_de_cadastro_com_sucesso(client, usuario_dados, codigo_verificacao):
    client.post("/api/register/", data=usuario_dados)
    user = User.objects.get(email=usuario_dados["email"])
    EmailVerificationCode.objects.create(user=user, code=codigo_verificacao)
    client.post("/api/validate-code/", data={
        "email": usuario_dados["email"],
        "code": codigo_verificacao,
    })

@when("ele tenta se cadastrar novamente")
def envia_dados_novamente(client, usuario_dados, contexto):
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@then("ele deve ser avisado que já está cadastrado")
def verifica_mensagem_de_usuario_existente(contexto):
    res = contexto["res"]
    assert res.status_code == 409
    assert "usuário já existe" in res.data["error"].lower()
