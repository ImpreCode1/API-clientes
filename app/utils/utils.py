from functools import wraps  # Para preservar metadata de funciones decoradas
from flask import request, jsonify  # Para manejar requests y respuestas JSON
import jwt, os  # JWT para tokens, os para variables de entorno

# =========================
#  Configuración
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")  # Clave secreta para firmar/verificar JWT

# =========================
#  Decorador de token requerido
# =========================
def token_requerido(f):
    """
    Decorador que protege rutas Flask verificando un token JWT en los headers.
    
    Si el token no existe o es inválido, devuelve un error 401.
    """
    @wraps(f)  # Mantiene metadata de la función original (nombre, docstring)
    def wrapper(*args, **kwargs):
        # Leer token del header Authorization: Bearer <token>
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            # Separar el token del prefijo "Bearer"
            jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            # Token inválido, expirado o mal formado
            return jsonify({"error": "Token inválido o expirado"}), 401

        # Token válido: ejecutar la función original
        return f(*args, **kwargs)

    return wrapper
