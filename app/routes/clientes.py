from flask import Blueprint, request, jsonify
from app.models.cliente import Cliente, db
import pandas as pd
import io
from app.utils.utils import token_requerido

clientes = Blueprint("clientes", __name__)

# =========================
#  Obtener todos los clientes
# =========================
@clientes.route("/clientes", methods=["GET"])
@token_requerido
def obtener_clientes():
    clientes = Cliente.query.all()
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
#  Obtener cliente por codigo (con campos importantes o fields opcional)
# =========================
@clientes.route("/clientes/<string:codigo_cliente>", methods=["GET"])
@token_requerido
def obtener_cliente(codigo_cliente):
    cliente = Cliente.query.filter_by(codigo_cliente=codigo_cliente).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Lista de campos importantes por defecto
    default_fields = [
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

    # Si vienen fields en query params, usamos esos
    fields_param = request.args.get("fields")
    if fields_param:
        requested_fields = [f.strip() for f in fields_param.split(",")]
    else:
        requested_fields = default_fields

    resultado = {}
    for field in requested_fields:
        if hasattr(cliente, field):
            value = getattr(cliente, field)
            # Convertir fecha a string ISO
            if isinstance(value, (db.Date, )):
                value = value.isoformat() if value else None
            resultado[field] = value
        else:
            resultado[field] = None  # puedes cambiarlo a error 400 si prefieres

    return jsonify(resultado), 200

# =========================
#  Obtener cliente con campos específicos
# =========================
@clientes.route("/clientes/<string:codigo_cliente>/", methods=["GET"])
@token_requerido
def obtener_cliente_campos(codigo_cliente):
    # Buscar cliente
    cliente = Cliente.query.filter_by(codigo_cliente=codigo_cliente).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Obtener los campos solicitados en query params
    fields_param = request.args.get("fields")
    if not fields_param:
        return jsonify({"error": "Debes indicar los campos en el parámetro 'fields'"}), 400

    requested_fields = [f.strip() for f in fields_param.split(",")]

    resultado = {}
    for field in requested_fields:
        if hasattr(cliente, field):
            resultado[field] = getattr(cliente, field)
        else:
            resultado[field] = None  # o podrías devolver un error si prefieres

    return jsonify(resultado), 200

# =========================
#  Crear cliente manualmente
# =========================
@clientes.route("/clientes", methods=["POST"])
@token_requerido
def crear_cliente():
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
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    # Diccionario de mapeo Excel -> Modelo
    excel_to_db = {
        "Cód.": "codigo_cliente",
        "Cliente": "nombre_cliente",
        "Grupo": "grupo",
        "Nombre2": "nombre2",
        "Nombre 3": "nombre3",
        "Nombre 4": "nombre4",
        "Soc.": "sociedad",
        "OrgVt": "organizacion_ventas",
        "CDis": "canal_distribucion",
        "Se": "sector",
        "Zona de ventas": "zona_ventas",
        "Oficina de ventas": "oficina_ventas",
        "Grupo de clientes": "grupo_clientes",
        "Nombre Vendedor": "nombre_vendedor",
        "Vendedor": "codigo_vendedor",
        "ZonaTransp": "zona_transporte",
        "Zona de Transporte": "descripcion_zona_transp",
        "Población": "poblacion",
        "Calle": "calle",
        "Nº ident.fis.1": "numero_identificacion",
        "CPag": "condicion_pago",
        "Vías pago": "vias_pago",
        "Contacto Cliente": "contacto_cliente",
        "Nombre de pila": "nombre_pila_contacto",
        "Denominación f.int": "denominacion_fiscal",
        "Correo contacto": "correo_contacto",
        "Tel contacto": "telefono_contacto",
        "Celular Contacto": "celular_contacto",
        "Teléfono 1": "telefono1",
        "Nº telefax": "fax",
        "Motivo Bloqueo Pedido": "motivo_bloqueo_pedido",
        "Cl.impto.": "clasificacion_impuesto",
        "Conc.búsq.": "concepto_busqueda",
        "ID Responsable Cartera": "id_responsable_cartera",
        "Resp.en deudor": "responsable_deudor",
        "Múmero teléfono responsable": "telefono_responsable",
        "Nota interior de una cuenta": "nota_interna",
        "Fecha Creación": "fecha_creacion",
        "Tel 3": "telefono3",
        "Mail Ejec": "correo_ejecutivo",
        "Tipo Clte": "tipo_cliente",
        "KAM Regional": "kam_regional",
        "CE Centro de expedición": "centro_expedicion",
        "FE /Aplica a eBill": "aplica_ebill",
        "Correo 1": "correo1",
        "Correo 2": "correo2",
        "Grupo 1 / FOCO": "grupo1_foco",
        "Grupo 2 CCIAL": "grupo2_comercial",
        "Grupo 3 ACUERDO PAGO": "grupo3_acuerdo_pago",
        "Grupo 4  SUCUR/TERCERO": "grupo4_sucursal",
        "CUADRANTE CLTE": "cuadrante_cliente",
        "DOBLE RAZON SOCIAL": "doble_razon_social",
        "CLASIF DOBLE": "clasificacion_doble",
        "HP SUM": "hp_sum",
        "HIKVISION": "hikvision",
        "HILOOK": "hilook",
        "EZVIZ": "ezviz",
        "CLASIF": "clasificacion",
        "KAM": "kam",
        "DIRECTOR": "director",
        "FOCO": "foco"
    }

    try:
        df = pd.read_excel(file)

        clientes = []
        filas_invalidas = []

        for index, row in df.iterrows():
            cliente_data = {}
            for excel_col, db_col in excel_to_db.items():
                value = row.get(excel_col)

                # Convertir NaN a None
                if pd.isna(value):
                    value = None

                # Convertir booleano
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

            # Validar que código_cliente no sea None
            if not cliente_data.get("codigo_cliente"):
                filas_invalidas.append(index + 2)  # +2 porque Excel empieza en 1 y encabezado
                continue

            clientes.append(Cliente(**cliente_data))

        # Insertar en la DB
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
