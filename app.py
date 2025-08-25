
from flask import Flask
from config import Config
from extensions import db
from routes.clientes import clientes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()  # Esto crea las tablas si no existen

app.register_blueprint(clientes)

@app.route("/")
def home():
    return {"msg": "API de Clientes corriendo"}

if __name__ == "__main__":
    app.run(debug=True)
