import pytest
from pytest_bdd import given, when, then, scenario
from rest_framework.test import APIClient
from django.core import mail
from api.models import User, Link, Papel, PerfilUsuario

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def organizador_dados():
    return {
        'email': 'anna@anna.com',
        'name': 'Anna Beatriz Serikyaku',
        'password': 'SenhaSuperS3gura.'
    }

@pytest.fixture
def palestrante_usuario_dados():
    return {
        'email': 'kely@kely.com',
        'name': 'Kely Cristina',
        'password': 'divaDemaisCl0seCategory!'
    }

@pytest.fixture
def contexto():
    return {}

@pytest.mark.django_db
@scenario('../cadastrar_palestrantes.feature', 'Organizador cadastra palestrante que não é usuário')
def test_cadastrar_palestrante_que_nao_e_usuario():
    pass

@pytest.mark.django_db
@scenario('../cadastrar_palestrantes.feature', 'Organizador cadastra palestrante que já é usuário')
def test_cadastrar_palestrante_que_ja_e_usuario():
    pass

@given('que Anna é organizadora')
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

    # criar Anna
    response = client.post("/api/register/", data=organizador_dados, format='json')
    assert response.status_code == 201

    # ativar Anna
    anna = User.objects.get(email=organizador_dados["email"])
    anna.is_active = True
    anna.save()

    # promover Anna
    response = client.post("/api/promover/", data={
        "email": organizador_dados["email"],
        "papel": Papel.ORGANIZADOR
    }, format='json')
    assert response.status_code == 200

    # login como Anna
    response = client.post("/api/token/", data={
        "email": organizador_dados['email'],
        "password": organizador_dados['password']
    }, format='json')
    assert response.status_code == 200

    contexto["token"] = response.data["access"]

@given('o palestrante já é usuário')
def palestrante_eh_usuario(client, palestrante_usuario_dados):
    response = client.post("/api/register/", data=palestrante_usuario_dados, format='json')
    assert response.status_code == 201

@when('ela insere corretamente as informações sobre o palestrante')
def organizador_informa_sobre_palestrante(client, contexto):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {contexto['token']}")

    link = Link.objects.create(domain="LinkedIn", url="https://linkedin.com/in/kely")

    response = client.post("/api/palestrante/", data={
        "email": "kely@kely.com",
        "display_name": "Kely Cristina",
        "ocupacao": "Professora e Pesquisadora",
        "biografia": "Atua em pesquisa interdisciplinar entre arte e tecnologia.",
        "link_apresentacao": "https://youtu.be/kely-talk",
        "foto_url": "https://example.com/kely.jpg",
        "foto_alt": "Foto de Kely Cristina",
        "links": [{"domain": link.domain, "url": link.url}]
        }, format="json")


    assert response.status_code == 201

    contexto['palestrante_email'] = "kely@kely.com"

@then('deve ser enviado um email com o código de primeiro acesso do palestrante')
def palestrante_recebe_codigo(contexto):
    email = mail.outbox[1]
    assert contexto['palestrante_email'] in email.to

@then('o palestrante não deve receber código de primeiro acesso por email')
def palestrante_nao_recebe_codigo():
    assert len(mail.outbox) == 3