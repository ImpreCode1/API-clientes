from flask import Flask  # Framework principal de Flask
from app.extensions import db  # Instancia de SQLAlchemy
from app.routes.clientes import clientes  # Blueprint para rutas de clientes
from app.routes.auth import auth  # Blueprint para rutas de autenticación

# =========================
#  Función de creación de la app
# =========================
def create_app(config_class):
    """
    Crea y configura la aplicación Flask.

    Args:
        config_class: Clase de configuración con variables como SECRET_KEY, DB_URI, etc.

    Returns:
        app: instancia de Flask configurada
    """
    # Crear instancia de Flask
    app = Flask(__name__)

    # Cargar configuración desde la clase proporcionada
    app.config.from_object(config_class)

    # Inicializar la extensión SQLAlchemy con la app
    db.init_app(app)

    # Crear las tablas en la base de datos (si no existen)
    with app.app_context():
        db.create_all()

    # Registrar los Blueprints para modularizar rutas
    app.register_blueprint(clientes)
    app.register_blueprint(auth)

    # =========================
    #  Ruta de prueba raíz
    # =========================
    @app.route("/")
    def home():
        """
        Ruta de prueba que indica que la API está corriendo
        """
        return {"msg": "API de Clientes corriendo"}

    # Retornar la instancia de la app
    return app