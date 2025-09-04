import pytest
from pytest_bdd import given, when, then, scenario
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario("../gerar_certificados.feature", "Uma pessoa não cadastrada gera um certificado")
def test_gerar_certificado():
    pass 

@given("que uma pessoa não está cadastrada,")
def pessoa_nao_cadastrada():
    pass 

@when("ela preenche com o seu nome e email, e participa de um evento")
def preenche_forms(contexto):
    contexto['ouvinte'] = {
        "nome" : "João das Couves",
        "email" : "joao.couves@usp.br"
    }

@then("deve ser gerado um certificado")
def gerar_certificado(client, contexto):
    res = client.post("/api/certificado/", contexto['ouvinte'])
    assert res.status_code == 201