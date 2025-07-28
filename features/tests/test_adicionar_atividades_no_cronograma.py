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
def nao_organizador_dados():
    return {
        'email': 'carlinhos@carlinhos.com',
        'name': 'Carlos Eduardo Ferreira',
        'password': 'd1vo1ncRivel!'
    }

@pytest.fixture
def atividade_valida_dados():
    return {
        "tipo": "palestra",
        "status": "confirmada",
        "comeca_as": "2025-10-20T12:00:00",
        "termina_as": "2025-10-20T13:00:00"
    }

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario('../adicionar_atividades_no_cronograma.feature', 'Um organizador deve conseguir adicionar no cronograma uma atividade')
def test_adiciona_atividade_no_cronograma():
    pass

@pytest.mark.django_db
@scenario('../adicionar_atividades_no_cronograma.feature', 'Um usuário que não é organizador não deve conseguir adicionar uma atividade no cronograma')
def test_nao_organizador_adiciona_atividade_no_cronograma():
    pass

@pytest.mark.django_db
@scenario('../adicionar_atividades_no_cronograma.feature', 'Um organizador não deve poder adicionar uma atividade fora dos horários do cronograma')
def test_adiciona_atividade_fora_do_cronograma():
    pass

@pytest.mark.django_db
@scenario('../adicionar_atividades_no_cronograma.feature', 'Um organizador não deve poder adicionar uma atividade que não está livre no cronograma')
def test_adiciona_uma_atividade_no_horario_de_outra():
    pass

# --------- GIVEN ----------

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

@given('que Carlinhos não é um organizador')
def nao_organizador_esta_logado(client, contexto, nao_organizador_dados):
    response = client.post("/api/register/", data=nao_organizador_dados, format='json')
    assert response.status_code == 201

    carlinhos = User.objects.get(email=nao_organizador_dados['email'])
    carlinhos.is_active = True
    carlinhos.save()
    
    response = client.post("/api/token/", data={
        "email": nao_organizador_dados['email'],
        "password": nao_organizador_dados['password']
    }, format='json')

    assert response.status_code == 200

    contexto["token"] = response.data["access"]

# -------- WHEN ------

@when('ele adiciona uma atividade no cronograma')
def adiciona_atividade_no_cronograma(contexto, client, atividade_valida_dados):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.post("/api/atividade/", data=atividade_valida_dados, format='json')
    
    assert response.status_code == 201

@when('ele tenta adicionar uma atividade no cronograma')
def tenta_adicionar_atividade_no_cronograma(client, contexto, atividade_valida_dados):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.post("/api/atividade/", data=atividade_valida_dados, format='json')

    assert response.status_code == 403

@when('ele adicionar uma atividade fora dos dias 20 a 24 de outubro')
def adiciona_atividade_fora_dos_dias(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    atividade = {
        "tipo": "palestra",
        "status": "confirmada",
        "comeca_as": "2025-10-19T12:00:00",
        "termina_as": "2025-10-19T13:00:00"
    }

    response = client.post("/api/atividade/", data=atividade, format='json')

    assert response.status_code == 400

@when('fora do horário das 12:00 às 18:45')
def adiciona_atividade_fora_do_horario(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    atividade = {
        "tipo": "palestra",
        "status": "confirmada",
        "comeca_as": "2025-10-20T11:00:00",
        "termina_as": "2025-10-20T12:00:00"
    }

    response = client.post("/api/atividade/", data=atividade, format='json')

    assert response.status_code == 400

@when('ele adicionar uma atividade na segunda feira às 12:00')
def adiciona_uma_atividade_no_horario_da_segunda(client, contexto, atividade_valida_dados):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.post("/api/atividade/", data=atividade_valida_dados, format='json')

    assert response.status_code == 201

@when('adiciona outra atividade no mesmo horário da segunda feira às 12:00')
def adiciona_uma_outra_atividade_no_mesmo_horario(client,contexto, atividade_valida_dados):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")
    
    response = client.post("/api/atividade/", data=atividade_valida_dados, format='json')

    assert response.status_code == 400

# --------- THEN -------

@then('a atividade deve ser adicionada')
def atividade_foi_adicionada(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.get('/api/atividade/')
    assert response.status_code == 200
    atividades = response.data

    assert [atividade["comeca_as"] == "2025-10-20T12:00:00" for atividade in atividades]

@then('a atividade não deve ser adicionada')
def atividade_nao_foi_adicionada(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.get('/api/atividade/')
    assert response.status_code == 200
    atividades = response.data

    assert len(atividades) == 0

@then('só deve ser adicionada uma atividade')
def atividade_no_mesmo_horario_nao_pode_ser_adicionada(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    response = client.get('/api/atividade/')
    assert response.status_code == 200
    atividades = response.data

    assert len(atividades) == 1