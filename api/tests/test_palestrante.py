import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Palestrante

@pytest.mark.django_db
def test_criar_palestrante_com_links():
    client = APIClient()
    url = reverse("palestrante-list")

    data = {
        "nome": "João Vitor Fernandes Domingues",
        "ocupacao": "Psicólogo",
        "biografia": "Psicólogo comportamental radical formado pela PUC.",
        "email": "jvfd@usp.br",
        "link_apresentacao": "https://apresentacao.jvfd.com",
        "foto_url": "https://fotos.jvfd.com/foto.jpg",
        "foto_alt": "João palestrando",
        "links": [
            {"domain": "GitHub", "url": "https://github.com/jvfd"},
            {"domain": "Lattes", "url": "http://lattes.cnpq.br/jvfd"}
        ]
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 201

    assert response.data["nome"] == data["nome"]
    assert len(response.data["links"]) == 2

    nomes_links = {link["domain"] for link in response.data["links"]}
    assert "GitHub" in nomes_links
    assert "Lattes" in nomes_links

@pytest.mark.django_db
def test_criar_palestrante_sem_links():
    client = APIClient()
    url = reverse("palestrante-list")

    data = {
        "nome": "Maria da Silva",
        "ocupacao": "Designer",
        "biografia": "Designer com foco em acessibilidade.",
        "email": "maria@usp.br",
        "link_apresentacao": "https://apresentacao.maria.com",
        "foto_url": "https://fotos.maria.com/foto.jpg",
        "foto_alt": "Maria em palestra",
        "links": []
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["nome"] == data["nome"]
    assert response.data["links"] == []

@pytest.mark.django_db
def test_get_palestrante_por_id():
    palestrante = Palestrante.objects.create(
        nome="João Vitor Fernandes Domingues",
        ocupacao="Psicólogo",
        biografia="Psicólogo comportamental radical formado pela PUC.",
        email="jvfd@usp.br",
        link_apresentacao="https://apresentacao.jvfd.com",
        foto_url="https://fotos.jvfd.com/foto.jpg",
        foto_alt="João palestrando"
    )

    client = APIClient()
    url = reverse("palestrante-detail", args=[palestrante.id])

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["nome"] == "João Vitor Fernandes Domingues"
    assert response.data["ocupacao"] == "Psicólogo"
    assert response.data["email"] == "jvfd@usp.br"

@pytest.mark.django_db
def test_get_palestrantes():
    Palestrante.objects.create(
        nome="João Vitor Fernandes Domingues",
        ocupacao="Psicólogo",
        biografia="Psicólogo comportamental radical formado pela PUC.",
        email="jvfd@usp.br",
        link_apresentacao="https://apresentacao.jvfd.com",
        foto_url="https://fotos.jvfd.com/foto.jpg",
        foto_alt="João palestrando"
    )
    
    Palestrante.objects.create(
        nome="Leandro Fernandes Domingues",
        ocupacao="Advogado",
        biografia="Advogado especializado em seguros.",
        email="lfd@usp.br",
        link_apresentacao="https://apresentacao.lfd.com",
        foto_url="https://fotos.lfd.com/foto.jpg",
        foto_alt="Leandro advogando"
    )

    client = APIClient()
    url = reverse("palestrante-list")

    response = client.get(url)

    nomes_palestrantes = { palestrante["nome"] for palestrante in response.data}
    assert len(response.data) == 2
    assert "João Vitor Fernandes Domingues" in nomes_palestrantes
    assert "Leandro Fernandes Domingues" in nomes_palestrantes

@pytest.mark.django_db
def test_atualizar_um_campo_do_palestrante():
    palestrante = Palestrante.objects.create(
        nome="João Vitor Fernandes Domingues",
        ocupacao="Psicólogo",
        biografia="Psicólogo comportamental radical formado pela PUC.",
        email="jvfd@usp.br",
        link_apresentacao="https://apresentacao.jvfd.com",
        foto_url="https://fotos.jvfd.com/foto.jpg",
        foto_alt="João palestrando"
    )

    client = APIClient()
    url = reverse("palestrante-detail", args=[palestrante.id])

    novos_dados = {
        "ocupacao": "Pesquisador em Análise do Comportamento"
    }

    response = client.patch(url, novos_dados, format="json")

    assert response.status_code == 200
    assert response.data["ocupacao"] == "Pesquisador em Análise do Comportamento"

    palestrante.refresh_from_db()
    assert palestrante.ocupacao == "Pesquisador em Análise do Comportamento"

@pytest.mark.django_db
def test_atualizar_todos_os_campos_do_palestrante():
    palestrante = Palestrante.objects.create(
        nome="João Vitor Fernandes Domingues",
        ocupacao="Psicólogo",
        biografia="Psicólogo comportamental radical formado pela PUC.",
        email="jvfd@usp.br",
        link_apresentacao="https://apresentacao.jvfd.com",
        foto_url="https://fotos.jvfd.com/foto.jpg",
        foto_alt="João palestrando"
    )

    client = APIClient()
    url = reverse("palestrante-detail", args=[palestrante.id])

    novos_dados = {
        "nome": "João Victor Fernandes Domingues",
        "ocupacao": "Professor",
        "biografia": "Nova biografia.",
        "email": "jvfd@usp.br",
        "link_apresentacao": "https://nova.com",
        "foto_url": "https://nova.com/foto.jpg",
        "foto_alt": "João reformulado"
    }

    response = client.put(url, novos_dados, format="json")
    print(response.status_code)
    print(response.data)

    assert response.status_code == 200
    assert response.data["ocupacao"] == "Professor"

    palestrante.refresh_from_db()
    assert palestrante.ocupacao == "Professor"
    assert palestrante.biografia == "Nova biografia."

