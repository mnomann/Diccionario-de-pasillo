# ============================================================================
# DESENREDA - Backend Dockerfile
# Python + FastAPI + Uvicorn
# Multi-stage build: builder -> produccion
# ============================================================================

# ---------------------------------------------------------------------------
# STAGE 1: Builder
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Instalar dependencias del sistema necesarias para compilar algunos paquetes
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo requirements.txt primero (optimizacion de cache)
COPY requirements.txt .

# Instalar dependencias en /install para luego copiarlas a produccion
RUN pip install --prefix=/install --no-warn-script-location \
    -r requirements.txt

# ---------------------------------------------------------------------------
# STAGE 2: Produccion
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS production

# Instalar solo libpq-dev para conector PostgreSQL en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Crear usuario no-root para seguridad
RUN addgroup --system --gid 1001 desenreda && \
    adduser --system --uid 1001 --gid 1001 desenreda

WORKDIR /app

# Copiar dependencias desde builder a /usr/local
COPY --from=builder /install /usr/local

# Copiar codigo de la aplicacion
COPY --chown=desenreda:desenreda . .

# Exponer puerto de la aplicacion
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Cambiar a usuario no-root
USER desenreda

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
