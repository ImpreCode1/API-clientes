# =========================
#  extensions.py
# =========================
# Este archivo centraliza las extensiones de Flask que serán usadas
# en toda la aplicación. Permite inicializarlas solo una vez y luego
# reutilizarlas en los Blueprints o la aplicación principal.

from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy para gestionar la base de datos
# Esta instancia se inicializará más tarde en create_app()
db = SQLAlchemy()
