import pytest
from pytest_bdd import given, when, then, scenario
from api.models import User, EmailVerificationCode
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def usuario_dados():
    return {}

@pytest.fixture
def contexto():
    return {}

@pytest.fixture
def codigo_verificacao():
    return "123456"

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha sem letras')
def test_cadastro_com_sucesso():
    pass

@given("que João preencheu todas as informações solicitadas")
def joao_envia_dados_corretamente(usuario_dados):
    usuario_dados["email"] = "joao@joao.com"
    usuario_dados["name"] = "João Vitor Fernandes Domingues"

@when("ele tenta cadastrar uma senha sem letras")
def joao_preenche_senha_sem_letra(client, usuario_dados, contexto):
    usuario_dados["password"] = "12345678"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@then("ele deve ser avisado que a senha é fraca")
def joao_nao_se_cadastra_pois_senha_e_fraca(contexto):
    res = contexto["res"]
    assert res.status_code == 400
