# ---------------------------------------------------
# Base image: Python optimizado para ML + CPU
# ---------------------------------------------------
FROM python:3.10-slim

# ---------------------------------------------------
# Instalar dependencias del sistema
# ---------------------------------------------------
RUN apt-get update && apt-get install -y \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------
# Crear directorio de la app
# ---------------------------------------------------
WORKDIR /app

# ---------------------------------------------------
# Copiar requirements.txt e instalar dependencias
# ---------------------------------------------------
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# ---------------------------------------------------
# Copiar TODO el proyecto dentro del contenedor
# ---------------------------------------------------
COPY . /app

# ---------------------------------------------------
# Puerto para HuggingFace Spaces
# ---------------------------------------------------
EXPOSE 7860

# ---------------------------------------------------
# Command para iniciar FastAPI en HF Spaces
# HuggingFace espera que corras en el puerto 7860
# ---------------------------------------------------
CMD ["uvicorn", "app_whatsapp:app", "--host", "0.0.0.0", "--port", "7860"]
