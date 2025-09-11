from app.extensions import db

class Cliente(db.Model):
    """
    Modelo Cliente para almacenar información detallada de cada cliente en la base de datos.

    Cada instancia representa un cliente con todos sus datos de contacto,
    información fiscal, comercial y logística.
    """
    __tablename__ = "clientes"

    # Identificador único del cliente
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Código único del cliente (obligatorio)
    codigo_cliente = db.Column(db.String(20), unique=True, nullable=False)

    # Nombre oficial del cliente
    nombre_cliente = db.Column(db.String(255))

    # Grupo o clasificación interna del cliente
    grupo = db.Column(db.String(100))

    # Nombres alternativos o comerciales
    nombre2 = db.Column(db.String(100))
    nombre3 = db.Column(db.String(100))
    nombre4 = db.Column(db.String(100))

    # Datos de la sociedad o entidad
    sociedad = db.Column(db.String(50))
    organizacion_ventas = db.Column(db.String(50))
    canal_distribucion = db.Column(db.String(50))
    sector = db.Column(db.String(50))
    zona_ventas = db.Column(db.String(50))
    oficina_ventas = db.Column(db.String(50))
    grupo_clientes = db.Column(db.String(50))

    # Información del vendedor responsable
    nombre_vendedor = db.Column(db.String(100))
    codigo_vendedor = db.Column(db.String(50))

    # Información logística
    zona_transporte = db.Column(db.String(50))
    descripcion_zona_transp = db.Column(db.String(100))

    # Dirección física del cliente
    poblacion = db.Column(db.String(100))
    calle = db.Column(db.String(255))

    # Información fiscal y de identificación
    numero_identificacion = db.Column(db.String(50))
    condicion_pago = db.Column(db.String(50))
    vias_pago = db.Column(db.String(100))

    # Información de contacto del cliente
    contacto_cliente = db.Column(db.String(100))
    nombre_pila_contacto = db.Column(db.String(100))
    denominacion_fiscal = db.Column(db.String(100))
    correo_contacto = db.Column(db.String(150))
    telefono_contacto = db.Column(db.String(50))
    celular_contacto = db.Column(db.String(50))
    telefono1 = db.Column(db.String(50))
    telefono3 = db.Column(db.String(50))
    fax = db.Column(db.String(50))

    # Información de gestión y control interno
    motivo_bloqueo_pedido = db.Column(db.String(255))
    clasificacion_impuesto = db.Column(db.String(50))
    concepto_busqueda = db.Column(db.String(100))
    id_responsable_cartera = db.Column(db.String(50))
    responsable_deudor = db.Column(db.String(100))
    telefono_responsable = db.Column(db.String(50))
    nota_interna = db.Column(db.Text)
    fecha_creacion = db.Column(db.Date)
    correo_ejecutivo = db.Column(db.String(150))
    tipo_cliente = db.Column(db.String(50))
    kam_regional = db.Column(db.String(100))
    centro_expedicion = db.Column(db.String(50))
    aplica_ebill = db.Column(db.Boolean, default=False)

    # Correos adicionales
    correo1 = db.Column(db.String(150))
    correo2 = db.Column(db.String(150))

    # Clasificación comercial adicional
    grupo1_foco = db.Column(db.String(100))
    grupo2_comercial = db.Column(db.String(100))
    grupo3_acuerdo_pago = db.Column(db.String(100))
    grupo4_sucursal = db.Column(db.String(100))
    cuadrante_cliente = db.Column(db.String(50))
    doble_razon_social = db.Column(db.String(255))
    clasificacion_doble = db.Column(db.String(100))

    # Productos o marcas asociadas
    hp_sum = db.Column(db.String(50))
    hikvision = db.Column(db.String(50))
    hilook = db.Column(db.String(50))
    ezviz = db.Column(db.String(50))

    # Datos de gestión y dirección
    clasificacion = db.Column(db.String(100))
    kam = db.Column(db.String(100))
    director = db.Column(db.String(100))
    foco = db.Column(db.String(100))

    def __repr__(self):
        """
        Representación legible del cliente para debugging.
        Muestra el código y nombre del cliente.
        """
        return f"<Cliente {self.codigo_cliente} - {self.nombre_cliente}>"
