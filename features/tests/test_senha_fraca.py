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
def test_cadastro_com_senha_sem_letra():
    pass

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha sem letras minúsculas')
def test_cadastro_com_senha_sem_letras_minusculas():
    pass

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha sem letras maiúsculas')
def test_cadastro_com_senha_sem_letras_maiusculas():
    pass

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha sem números')
def test_cadastro_com_senha_sem_numeros():
    pass

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha com menos de 8 caracteres')
def test_cadastro_com_senha_com_menos_de_oito_caracteres():
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

@when("ele tenta cadastrar uma senha sem letras minúsculas")
def joao_preenche_senha_sem_letra_minuscula(client, usuario_dados, contexto):
    usuario_dados["password"] = "12345678A"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@when("ele tenta cadastrar uma senha sem letras maiúsculas")
def joao_preenche_senha_sem_letra_maiuscula(client, usuario_dados, contexto):
    usuario_dados["password"] = "12345678a"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@when("ele tenta cadastrar uma senha sem números")
def joao_preenche_senha_sem_letra_maiuscula(client, usuario_dados, contexto):
    usuario_dados["password"] = "abcdefgh"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@when("ele tenta cadastrar uma senha com menos de 8 caracteres")
def joao_preenche_senha_sem_letra_maiuscula(client, usuario_dados, contexto):
    usuario_dados["password"] = "a1Bc"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@then("ele deve ser avisado que a senha é fraca")
def joao_nao_se_cadastra_pois_senha_e_fraca(contexto):
    res = contexto["res"]
    assert res.status_code == 400
