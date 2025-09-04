import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture
def client():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    testing_client = app.test_client()

    yield testing_client

    with app.app_context():
        db.drop_all()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["msg"] == "API de Clientes corriendo"
