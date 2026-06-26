"""
Alembic environment configuration for Desenreda.
Soporta migraciones automaticas usando SQLAlchemy models.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Agregar el directorio raiz del backend al path para importar models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# Importar los modelos SQLAlchemy para autogenerate support
from models import Base

# Alembic Config object
config = context.config

# Configurar logging si existe el archivo
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata

# --- Funciones de migracion ------------------------------------------------

def get_url() -> str:
    """
    Obtiene la URL de la base de datos desde variable de entorno
    o usa el valor por defecto del alembic.ini.

    Alembic usa SQLAlchemy sync engine, por lo que si la URL contiene
    ``+asyncpg`` (driver async) se reemplaza por el driver sync
    correspondiente (psycopg2).
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        url = config.get_main_option("sqlalchemy.url")
    # Reemplazar driver async por sync para Alembic
    url = url.replace("+asyncpg", "+psycopg2")
    return url


def run_migrations_offline() -> None:
    """
    Ejecuta migraciones en modo 'offline'.
    Genera SQL sin conectarse a la base de datos.
    """
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,           # Detectar cambios de tipo de columna
        compare_server_default=True, # Detectar cambios en defaults
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecuta migraciones en modo 'online'.
    Se conecta a la base de datos y ejecuta SQL directamente.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
