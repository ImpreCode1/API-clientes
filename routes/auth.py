import os
import datetime
import jwt
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY")
API_USER = os.getenv("API_USER")
API_PASSWORD = os.getenv("API_PASSWORD")

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or data.get("user") != API_USER or data.get("password") != API_PASSWORD:
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    print("SECRET_KEY:", repr(SECRET_KEY))
    token = jwt.encode(
        {
            "user": data["user"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})
