from graphviz import Digraph

# Crear el diagrama de flujo
dot = Digraph("Flujo de Viajes", format="png")
dot.attr(rankdir="TB", size="8")

# Nodo inicial
dot.node("start", "Solicitud inicial\n(Gerente/Director/Team Leader)", shape="oval", style="filled", fillcolor="lightblue")

# Validación requiere avión
dot.node("validacion", "¿Requiere avión?", shape="diamond", style="filled", fillcolor="lightyellow")

# Rama A: Con avión
dot.node("vp", "Vicepresidencia revisa\nAprobar/Rechazar", shape="diamond", style="filled", fillcolor="lightyellow")
dot.node("rechazo", "Solicitud rechazada", shape="oval", style="filled", fillcolor="lightcoral")
dot.node("comprador", "Asignar comprador de tiquetes", shape="box", style="filled", fillcolor="lightgreen")
dot.node("transporteA", "Encargado activa transporte", shape="box", style="filled", fillcolor="lightgreen")
dot.node("finA", "Fin del proceso (viaje con avión)", shape="oval", style="filled", fillcolor="lightblue")

# Rama B: Sin avión
dot.node("transporteB", "Encargado activa transporte", shape="box", style="filled", fillcolor="lightgreen")
dot.node("finB", "Fin del proceso (viaje sin avión)", shape="oval", style="filled", fillcolor="lightblue")

# Conexiones principales
dot.edge("start", "validacion")

# Rama A
dot.edge("validacion", "vp", label="Sí")
dot.edge("vp", "rechazo", label="Rechazar")
dot.edge("vp", "comprador", label="Aprobar")
dot.edge("comprador", "transporteA")
dot.edge("transporteA", "finA")

# Rama B
dot.edge("validacion", "transporteB", label="No")
dot.edge("transporteB", "finB")

# Renderizar en archivo temporal
output_path = "/mnt/data/flujo_viajes"
dot.render(output_path, cleanup=True)
