# Imagen base con Python
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (ej: para MySQL client)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para correr la app con Gunicorn
# -w 4 → 4 workers
# -b 0.0.0.0:5000 → escuchar en todas las interfaces en el puerto 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app", "--access-logfile", "-"]
