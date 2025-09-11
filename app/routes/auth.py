import os
import datetime
import jwt
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear un blueprint de Flask llamado "auth" para las rutas de autenticación
auth = Blueprint("auth", __name__)

# Variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")  # Clave secreta para firmar JWT
API_USER = os.getenv("API_USER")      # Usuario permitido para login
API_PASSWORD = os.getenv("API_PASSWORD")  # Contraseña permitida para login

@auth.route("/login", methods=["POST"])
def login():
    """
    Endpoint para autenticación.
    Verifica las credenciales recibidas en el cuerpo de la petición.
    Si son correctas, retorna un JWT válido por 10 horas.
    """
    # Obtener datos JSON del cuerpo de la solicitud
    data = request.json

    # Validar credenciales
    if not data or data.get("user") != API_USER or data.get("password") != API_PASSWORD:
        # Retornar error 401 si son inválidas
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    # DEBUG: imprimir la SECRET_KEY (para desarrollo)
    print("SECRET_KEY:", repr(SECRET_KEY))

    # Generar token JWT
    token = jwt.encode(
        {
            "user": data["user"],  # Usuario dentro del payload
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=10)  # Expiración
        },
        SECRET_KEY,  # Clave secreta para firmar
        algorithm="HS256"  # Algoritmo de firma
    )

    # Retornar token en formato JSON
    return jsonify({"token": token})
