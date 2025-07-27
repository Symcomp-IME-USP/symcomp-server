import pytest
from pytest_bdd import given, when, then, scenario
from rest_framework.test import APIClient
from api.models import User, PerfilUsuario, Papel

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def organizador_dados():
    return {
        'email': 'od4ir@od4ir.com',
        'name': 'Odair Gonçalves Oliveira',
        'password': 'SenhaSuperS3gura.'
    }

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario('../adicionar_atividades_no_cronograma.feature', 'Um organizador deve conseguir adicionar no cronograma uma atividade')
def test_adiciona_atividade_no_cronograma():
    pass

@given('que Odair é organizador')
def organizador_esta_logado(client, organizador_dados, contexto):
    admin = User.objects.create_superuser(
        email='admin@admin.com',
        name='Admin',
        password='AdminSenha123!'
    )
    PerfilUsuario.objects.create(user=admin, papel=Papel.PRESIDENTE)

    # login admin
    response = client.post("/api/token/", data={
        "email": 'admin@admin.com',
        "password": 'AdminSenha123!'
    }, format='json')
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    # criar Odair
    response = client.post("/api/register/", data=organizador_dados, format='json')
    assert response.status_code == 201

    # ativar Odair
    odair = User.objects.get(email=organizador_dados["email"])
    odair.is_active = True
    odair.save()

    # promover Odair
    response = client.post("/api/promover/", data={
        "email": organizador_dados["email"],
        "papel": Papel.ORGANIZADOR
    }, format='json')
    assert response.status_code == 200

    # login como Odair
    response = client.post("/api/token/", data={
        "email": organizador_dados['email'],
        "password": organizador_dados['password']
    }, format='json')
    assert response.status_code == 200

    contexto["token"] = response.data["access"]

@when('ele adiciona uma atividade no cronograma')
def adiciona_atividade_no_cronograma(contexto, client):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    atividade_dados = {
        "tipo": "palestra",
        "status": "confirmada",
        "comeca_as": "2025-10-20T12:00:00",
        "termina_as": "2025-10-20T13:00:00"
    }

    response = client.post("/api/atividade/", data=atividade_dados, format='json')
    
    assert response.status_code == 201

@then('a atividade deve ser adicionada')
def atividade_foi_adicionada(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.get('/api/atividade/')
    assert response.status_code == 200
    atividades = response.data

    assert [atividade["comeca_as"] == "2025-10-20T12:00:00" for atividade in atividades]
