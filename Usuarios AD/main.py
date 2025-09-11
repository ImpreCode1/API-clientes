from fastapi import FastAPI, Query
from ldap3 import Server, Connection, ALL, SUBTREE
from typing import Optional

app = FastAPI()

# =========================
# Configuración
# =========================
AD_SERVER = "ldap://impresistem.local"
BASE_DN = "DC=IMPRESISTEM,DC=local"
ATTRIBUTES = [
    "displayName",
    "mail",
    "title",
    "department",
    "streetAddress",  # Dirección
    "l",              # Ciudad
    "st",             # Estado/Departamento
    "postalCode",     # Código postal
    "co"              # País
]

# Credenciales de servicio (reemplaza por un usuario con permisos de lectura en AD)
AD_USER = "IMPRESISTEM\\sebastian.ortiz"
AD_PASSWORD = "Chivas504"

# =========================
# Función conexión
# =========================
def get_connection():
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)
    return conn

# =========================
# Endpoint
# =========================
@app.get("/usuarios")
def get_usuarios(
    correo: Optional[str] = Query(None, description="Correo del usuario"),
    username: Optional[str] = Query(None, description="SamAccountName o username")
):
    try:
        conn = get_connection()

        # Filtro base: usuarios personas activas con correo
        search_filter = (
            "(&(objectClass=user)(objectCategory=person)(mail=*)"
            "(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
        )

        # Ajustar filtro si se busca por correo o username
        if correo:
            search_filter = f"(&(objectClass=user)(mail={correo}))"
        elif username:
            search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"

        conn.search(
            search_base=BASE_DN,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=ATTRIBUTES
        )

        usuarios = []
        for entry in conn.entries:
            # Construir dirección comercial al estilo de Teams
            direccion_comercial = ", ".join(filter(None, [
                entry.streetAddress.value if entry.streetAddress else None,
                entry.l.value if entry.l else None,
                entry.st.value if entry.st else None,
                entry.co.value if entry.co else None
            ]))

            usuarios.append({
                "nombre": entry.displayName.value,
                "correo": entry.mail.value,
                "cargo": entry.title.value,
                "area": entry.department.value,
                "direccion_comercial": direccion_comercial or None
            })

        conn.unbind()

        return {"total": len(usuarios), "usuarios": usuarios}

    except Exception as e:
        return {"error": str(e)}
