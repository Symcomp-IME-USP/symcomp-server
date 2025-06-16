import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_criar_palestrante_com_links():
    client = APIClient()
    url = reverse("palestrante-list")

    dados = {
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

    response = client.post(url, dados, format="json")

    assert response.status_code == 201
    
    assert response.data["nome"] == dados["nome"]
    assert len(response.data["links"]) == 2

    nomes_links = {link["domain"] for link in response.data["links"]}
    assert "GitHub" in nomes_links
    assert "Lattes" in nomes_links

@pytest.mark.django_db
def test_criar_palestrante_sem_links():
    client = APIClient()
    url = reverse("palestrante-list")

    dados = {
        "nome": "Maria da Silva",
        "ocupacao": "Designer",
        "biografia": "Designer com foco em acessibilidade.",
        "email": "maria@usp.br",
        "link_apresentacao": "https://apresentacao.maria.com",
        "foto_url": "https://fotos.maria.com/foto.jpg",
        "foto_alt": "Maria em palestra",
        "links": []
    }

    response = client.post(url, dados, format="json")

    assert response.status_code == 201
    assert response.data["nome"] == dados["nome"]
    assert response.data["links"] == []
