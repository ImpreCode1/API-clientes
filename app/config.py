import os  # Para trabajar con variables de entorno y rutas
from dotenv import load_dotenv  # Para cargar variables desde un archivo .env

# Cargar automáticamente las variables de entorno desde el archivo .env
load_dotenv()

# =========================
#  Configuración base
# =========================
class Config:
    """
    Clase de configuración principal para la aplicación Flask.
    Contiene configuración de base de datos, seguridad y rutas de subida de archivos.
    """
    # Clave secreta para Flask (sessions, CSRF, etc.)
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

    # URI de la base de datos para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # Deshabilitar el seguimiento de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para JWT (tokens de autenticación)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")

    # Carpeta para guardar archivos subidos
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "upload")


# =========================
#  Configuración para testing
# =========================
class TestConfig(Config):
    """
    Clase de configuración para tests.
    Hereda de Config y modifica la base de datos para usar SQLite en memoria.
    """
    TESTING = True  # Habilita modo testing en Flask

    # Base de datos en memoria para pruebas, evitando tocar la DB real
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
