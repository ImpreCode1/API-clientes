from flask import Flask
from app.config import Config
from app.extensions import db
from app.routes.clientes import clientes
from app.routes.auth import auth

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()  # Esto crea las tablas si no existen

app.register_blueprint(clientes)
app.register_blueprint(auth)


@app.route("/")
def home():
    return {"msg": "API de Clientes corriendo"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
