from flask import Flask
from app.extensions import db
from app.routes.clientes import clientes
from app.routes.auth import auth


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(clientes)
    app.register_blueprint(auth)

    @app.route("/")
    def home():
        return {"msg": "API de Clientes corriendo"}

    return app
