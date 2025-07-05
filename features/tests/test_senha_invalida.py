import pytest
from pytest_bdd import given, when, then, scenario
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

@pytest.mark.django_db
@scenario('../cadastrar_usuario.feature', 'Senha com mais de 510 caracteres')
def test_cadastro_com_senha_de_mais_de_255_caracteres():
    pass

@given("que João preencheu todas as informações solicitadas")
def joao_envia_dados_corretamente(usuario_dados):
    usuario_dados["email"] = "joao@joao.com"
    usuario_dados["name"] = "João Vitor Fernandes Domingues"

@when("ele tenta cadastrar uma senha com mais de 510 caracteres")
def joao_preenche_senha_com_mais_de_255_caracteres(client, usuario_dados, contexto):
    # Senha aleatória de 512 caracteres gerada por uma LLM
    usuario_dados["password"] = "n8K$^apz4y!TQ9rWvYF3bMGZ#oJ@L2kXs1iUmN7eq5tC&uBj6xHV!glOD^AfK%RcwPnEZ$8mYdT#S*0qvI^3bJL7zWh9N$GyfMaVo!r@pCtXu64BksF#eUQ2ZxLRwJmK9PnYT$%vbdNcOlgH#^uAf0&Mi7KpsCQ8!tVWj3E2XzL1RyodGnUBhF@M$k#nn8K$^apz4y!TQ9rWvYF3bMGZ#oJ@L2kXs1iUmN7eq5tC&uBj6xHV!glOD^AfK%RcwPnEZ$8mYdT#S*0qvI^3bJL7zWh9N$GyfMaVo!r@pCtXu64BksF#eUQ2ZxLRwJmK9PnYT$%vbdNcOlgH#^uAf0&Mi7KpsCQ8!tVWj3E2XzL1RyodGnUBhF@M$k#n"
    res = client.post("/api/register/", data=usuario_dados)
    contexto["res"] = res

@then("ele deve ser avisado que a senha é invalida")
def joao_nao_se_cadastra_pois_senha_e_invalida(contexto):
    res = contexto["res"]
    assert res.status_code == 400
