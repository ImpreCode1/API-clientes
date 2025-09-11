import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db

# =========================
# Fixture de cliente de prueba
# =========================
# Esta fixture crea una instancia de la aplicación Flask configurada
# para pruebas, inicializa la base de datos en memoria y proporciona
# un cliente de test para hacer requests HTTP simuladas.
@pytest.fixture
def client():
    # Crear app con configuración de prueba
    app = create_app(TestConfig)

    # Crear tablas dentro del contexto de la app
    with app.app_context():
        db.create_all()

    # Crear cliente de pruebas para enviar requests
    testing_client = app.test_client()

    # Devolver el cliente al test
    yield testing_client

    # Limpiar la base de datos después de cada test
    with app.app_context():
        db.drop_all()


# =========================
# Test de la ruta principal "/"
# =========================
# Verifica que la ruta "/" responda correctamente
def test_home(client):
    # Hacer request GET a la ruta principal
    response = client.get("/")

    # Comprobar que el status code sea 200 OK
    assert response.status_code == 200

    # Comprobar que el mensaje en JSON sea el esperado
    assert response.json["msg"] == "API de Clientes corriendo"
