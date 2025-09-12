from flask import Blueprint, request, jsonify
from app.models.cliente import Cliente, db
import pandas as pd
import io
from app.utils.utils import token_requerido

# Crear blueprint para clientes
clientes = Blueprint("clientes", __name__)

# =========================
#  Obtener todos los clientes
# =========================
@clientes.route("/clientes", methods=["GET"])
@token_requerido  # Requiere token válido
def obtener_clientes():
    """
    Devuelve todos los clientes en formato JSON con campos importantes.
    """
    clientes = Cliente.query.all()  # Obtener todos los registros
    resultado = [
        {
            "id": c.id,
            "codigo_cliente": c.codigo_cliente,
            "nombre_cliente": c.nombre_cliente,
            "grupo": c.grupo,
            "nombre_vendedor": c.nombre_vendedor,
            "codigo_vendedor": c.codigo_vendedor,
            "correo_contacto": c.correo_contacto,
            "telefono_contacto": c.telefono_contacto,
            "celular_contacto": c.celular_contacto,
            "poblacion": c.poblacion,
            "calle": c.calle,
            "fecha_creacion": c.fecha_creacion.isoformat() if c.fecha_creacion else None,
            "tipo_cliente": c.tipo_cliente,
        }
        for c in clientes
    ]
    return jsonify(resultado), 200

# =========================
#  Obtener cliente por código (con campos importantes o fields opcional)
# =========================
@clientes.route("/clientes/<string:codigo_cliente>", methods=["GET"])
@token_requerido
def obtener_cliente(codigo_cliente):
    """
    Devuelve los datos de un cliente específico.
    Permite especificar campos con query param 'fields'.
    Si no se indican campos, se usan campos por defecto.
    """
    cliente = Cliente.query.filter_by(codigo_cliente=codigo_cliente).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    fields_param = request.args.get("fields")

    if fields_param:
        requested_fields = [f.strip() for f in fields_param.split(",")]
    else:
        requested_fields = [
            "id",
            "codigo_cliente",
            "nombre_cliente",
            "grupo",
            "nombre_vendedor",
            "codigo_vendedor",
            "correo_contacto",
            "telefono_contacto",
            "celular_contacto",
            "poblacion",
            "calle",
            "fecha_creacion",
            "tipo_cliente",
        ]

    resultado = {}
    for field in requested_fields:
        if hasattr(cliente, field):
            value = getattr(cliente, field)
            # Si es fecha (Date o DateTime), formatear
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            resultado[field] = value
        else:
            resultado[field] = None

    return jsonify(resultado), 200


# =========================
#  Crear cliente manualmente
# =========================
@clientes.route("/clientes", methods=["POST"])
@token_requerido
def crear_cliente():
    """
    Crea un nuevo cliente con los datos recibidos en JSON.
    """
    data = request.get_json()
    try:
        nuevo_cliente = Cliente(**data)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({"mensaje": "Cliente creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# =========================
#  Actualizar cliente
# =========================
@clientes.route("/clientes/<int:id>", methods=["PUT"])
@token_requerido
def actualizar_cliente(id):
    """
    Actualiza los campos de un cliente existente.
    """
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(cliente, key, value)

    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado exitosamente"}), 200

# =========================
#  Eliminar cliente
# =========================
@clientes.route("/clientes/<int:id>", methods=["DELETE"])
@token_requerido
def eliminar_cliente(id):
    """
    Elimina un cliente existente por su ID.
    """
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado exitosamente"}), 200

# =========================
#  Importar clientes desde Excel
# =========================
@clientes.route("/clientes/importar", methods=["POST"])
@token_requerido
def importar_clientes():
    """
    Permite importar clientes desde un archivo Excel.
    Convierte columnas a campos del modelo Cliente.
    """
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    # Mapeo columnas Excel -> campos modelo
    excel_to_db = {
        "Cód.": "codigo_cliente",
        "Cliente": "nombre_cliente",
        "Grupo": "grupo",
        # ... (otros mapeos omitidos para brevedad)
        "FOCO": "foco"
    }

    try:
        df = pd.read_excel(file)
        clientes = []
        filas_invalidas = []

        for idx, (index, row) in enumerate(df.iterrows()):
            cliente_data = {}
            for excel_col, db_col in excel_to_db.items():
                value = row[excel_col] if excel_col in row else None

                # Convertir NaN a None
                if pd.isna(value):
                    value = None

                # Booleano aplica_ebill
                if db_col == "aplica_ebill":
                    if value is None:
                        value = False
                    elif str(value).strip().lower() in ["sí", "si", "yes", "true", "1"]:
                        value = True
                    else:
                        value = False

                # Convertir fechas
                if db_col == "fecha_creacion" and value is not None:
                    if isinstance(value, pd.Timestamp):
                        value = value.to_pydatetime()
                    elif isinstance(value, str):
                        try:
                            value = pd.to_datetime(value, dayfirst=True)
                        except:
                            value = None

                cliente_data[db_col] = value

            # Validar código_cliente
            if not cliente_data.get("codigo_cliente"):
                filas_invalidas.append(idx + 2)
                continue

            clientes.append(Cliente(**cliente_data))

        # Insertar en la base de datos
        db.session.add_all(clientes)
        db.session.commit()

        mensaje = f"{len(clientes)} clientes importados exitosamente."
        if filas_invalidas:
            mensaje += f" Filas ignoradas por código_cliente vacío: {filas_invalidas}"

        return jsonify({"mensaje": mensaje}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# =========================
#  Exportar clientes a Excel
# =========================
@clientes.route("/clientes/exportar", methods=["GET"])
@token_requerido
def exportar_clientes():
    """
    Exporta todos los clientes a un archivo Excel.
    """
    clientes = Cliente.query.all()
    data = [
        {
            "codigo_cliente": c.codigo_cliente,
            "nombre_cliente": c.nombre_cliente,
            "grupo": c.grupo,
            "correo_contacto": c.correo_contacto,
            "telefono_contacto": c.telefono_contacto,
        }
        for c in clientes
    ]

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Clientes")

    output.seek(0)

    return (
        output.read(),
        200,
        {
            "Content-Disposition": "attachment; filename=clientes.xlsx",
            "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
    )
