import pytest
from pytest_bdd import given, when, then, scenario
from api.models import ActivityHistory
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def usuario_dados():
    return {
        "email": "marcelo@example.com",
        "password": "SenhaSegura123",
        "name": "Marcelo Mascarenhas Martinelli"
    }

