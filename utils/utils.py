from functools import wraps
from flask import request, jsonify
import jwt, os

SECRET_KEY = os.getenv("SECRET_KEY")

def token_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        try:
            jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return jsonify({"error": "Token inválido o expirado"}), 401
        return f(*args, **kwargs)
    return wrapper
