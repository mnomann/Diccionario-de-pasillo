"""
Migration 001_initial: Creacion inicial de todas las tablas.

Descripcion:
    Crea el esquema completo de la base de datos Desenreda:
    - Extensiones: pg_trgm, pgcrypto, uuid-ossp
    - ENUM types: categoria_palabra, sugerencia_tipo, sugerencia_estado, tono_frase
    - Tablas: usuario, palabra, escenario, frase, sugerencia, frase_palabra
    - Indices para busqueda de texto completo, JSONB, ILIKE (trigramas)
    - Triggers para actualizacion automatica de fechas
    - Funciones PL/pgSQL asociadas

Revision ID: 001_initial
Revises: (None - migracion inicial)
Create Date: 2026-06-03 18:00:00.000000
"""

from typing import Final, Optional, Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: Final[str] = "001_initial"
down_revision: Optional[str] = None
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    """
    Ejecuta la migracion hacia arriba: crea todo el esquema inicial.
    """

    # --- Extensiones -------------------------------------------------------
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")

    # --- ENUM types --------------------------------------------------------
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE categoria_palabra AS ENUM (
                'modismo', 'muletilla', 'jerga',
                'insulto_ligero', 'abreviacion'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE sugerencia_tipo AS ENUM (
                'palabra', 'frase', 'escenario'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE sugerencia_estado AS ENUM (
                'pendiente', 'aprobado', 'rechazado'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE tono_frase AS ENUM (
                'ironico', 'sarcastico', 'directo',
                'humoristico', 'motivacional', 'neutro'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
    """)

    # --- Tabla: usuario ----------------------------------------------------
    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("contrasena_hash", sa.String(length=255), nullable=False),
        sa.Column("preferencias", sa.JSON(), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("fecha_registro", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=True),
        sa.Column("ultima_conexion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_usuario_email"),
    )

    # --- Tabla: palabra ----------------------------------------------------
    op.create_table(
        "palabra",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("palabra", sa.String(length=200), nullable=False),
        sa.Column("traduccion", sa.String(length=500), nullable=False),
        sa.Column("categoria", sa.Enum(
            "modismo", "muletilla", "jerga",
            "insulto_ligero", "abreviacion",
            name="categoria_palabra"
        ), nullable=False),
        sa.Column("nivel_formalidad", sa.Integer(),
                  server_default=sa.text("2"), nullable=True),
        sa.Column("nivel_ironia", sa.Integer(),
                  server_default=sa.text("0"), nullable=True),
        sa.Column("nivel_sarcasmo", sa.Integer(),
                  server_default=sa.text("0"), nullable=True),
        sa.Column("pronunciacion_fonetica", sa.String(length=100), nullable=True),
        sa.Column("ejemplo_uso", sa.String(length=500), nullable=True),
        sa.Column("nota_cultural", sa.String(length=1000), nullable=True),
        sa.Column("origen", sa.String(length=500), nullable=True),
        sa.Column("variantes", sa.JSON(), server_default=sa.text("'[]'::jsonb"), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=True),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Agregar columna generada TSVECTOR (se agrega via SQL directo)
    op.execute("""
        ALTER TABLE palabra
        ADD COLUMN IF NOT EXISTS texto_busqueda TSVECTOR
        GENERATED ALWAYS AS (
            to_tsvector('spanish',
                COALESCE(palabra, '') || ' ' ||
                COALESCE(traduccion, '') || ' ' ||
                COALESCE(ejemplo_uso, '') || ' ' ||
                COALESCE(nota_cultural, '')
            )
        ) STORED
    """)

    # --- Tabla: escenario --------------------------------------------------
    op.create_table(
        "escenario",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.String(length=500), nullable=False),
        sa.Column("icono", sa.String(length=50), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=True),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- Tabla: frase ------------------------------------------------------
    op.create_table(
        "frase",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("escenario_id", sa.Integer(), nullable=False),
        sa.Column("frase_original", sa.String(length=500), nullable=False),
        sa.Column("traduccion", sa.String(length=500), nullable=False),
        sa.Column("explicacion", sa.String(length=1000), nullable=True),
        sa.Column("tono", sa.String(length=50), nullable=True),
        sa.Column("intencion_real", sa.String(length=500), nullable=True),
        sa.Column("nivel_formalidad", sa.Integer(),
                  server_default=sa.text("3"), nullable=True),
        sa.Column("nivel_ironia", sa.Integer(),
                  server_default=sa.text("0"), nullable=True),
        sa.Column("nivel_sarcasmo", sa.Integer(),
                  server_default=sa.text("0"), nullable=True),
        sa.Column("ejemplo_uso", sa.String(length=500), nullable=True),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=True),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["escenario_id"],
            ["escenario.id"],
            name="fk_frase_escenario",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- Tabla: sugerencia -------------------------------------------------
    op.create_table(
        "sugerencia",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("tipo", sa.Enum(
            "palabra", "frase", "escenario",
            name="sugerencia_tipo"
        ), nullable=False),
        sa.Column("contenido", sa.JSON(), nullable=False),
        sa.Column("estado", sa.Enum(
            "pendiente", "aprobado", "rechazado",
            name="sugerencia_estado"
        ), server_default=sa.text("'pendiente'"), nullable=True),
        sa.Column("comentario_moderador", sa.String(length=500), nullable=True),
        sa.Column("usuario_email", sa.String(length=255), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=True),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["usuario_id"],
            ["usuario.id"],
            name="fk_sugerencia_usuario",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- Tabla: frase_palabra (relacion N:M) -------------------------------
    op.create_table(
        "frase_palabra",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("frase_id", sa.Integer(), nullable=False),
        sa.Column("palabra_id", sa.Integer(), nullable=False),
        sa.Column("relevancia", sa.Integer(),
                  server_default=sa.text("1"), nullable=True),
        sa.ForeignKeyConstraint(
            ["frase_id"],
            ["frase.id"],
            name="fk_frase_palabra_frase",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["palabra_id"],
            ["palabra.id"],
            name="fk_frase_palabra_palabra",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("frase_id", "palabra_id",
                            name="uq_frase_palabra"),
    )

    # --- Indices -----------------------------------------------------------

    # FTS en palabra
    op.create_index(
        "idx_palabra_texto_busqueda",
        "palabra",
        ["texto_busqueda"],
        postgresql_using="gin",
    )

    # Trigramas para busqueda ILIKE en palabra
    op.create_index(
        "idx_palabra_palabra_trgm",
        "palabra",
        ["palabra"],
        postgresql_using="gin",
        postgresql_ops={"palabra": "gin_trgm_ops"},
    )

    op.create_index(
        "idx_palabra_traduccion_trgm",
        "palabra",
        ["traduccion"],
        postgresql_using="gin",
        postgresql_ops={"traduccion": "gin_trgm_ops"},
    )

    # GIN para JSONB
    op.create_index(
        "idx_usuario_preferencias",
        "usuario",
        ["preferencias"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_palabra_variantes",
        "palabra",
        ["variantes"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_sugerencia_contenido",
        "sugerencia",
        ["contenido"],
        postgresql_using="gin",
    )

    # Indices parciales para busquedas comunes
    op.create_index(
        "idx_palabra_categoria",
        "palabra",
        ["categoria"],
        postgresql_where=sa.text("activo = TRUE"),
    )

    op.create_index(
        "idx_frase_escenario",
        "frase",
        ["escenario_id"],
        postgresql_where=sa.text("activo = TRUE"),
    )

    op.create_index(
        "idx_sugerencia_estado",
        "sugerencia",
        ["estado"],
    )

    op.create_index(
        "idx_sugerencia_usuario",
        "sugerencia",
        ["usuario_id"],
    )

    op.create_index(
        "idx_sugerencia_tipo",
        "sugerencia",
        ["tipo"],
    )

    # Trigramas para busqueda en frase
    op.create_index(
        "idx_frase_frase_original_trgm",
        "frase",
        ["frase_original"],
        postgresql_using="gin",
        postgresql_ops={"frase_original": "gin_trgm_ops"},
    )

    op.create_index(
        "idx_frase_traduccion_trgm",
        "frase",
        ["traduccion"],
        postgresql_using="gin",
        postgresql_ops={"traduccion": "gin_trgm_ops"},
    )

    # Trigramas para busqueda en escenario
    op.create_index(
        "idx_escenario_nombre_trgm",
        "escenario",
        ["nombre"],
        postgresql_using="gin",
        postgresql_ops={"nombre": "gin_trgm_ops"},
    )

    op.create_index(
        "idx_escenario_descripcion_trgm",
        "escenario",
        ["descripcion"],
        postgresql_using="gin",
        postgresql_ops={"descripcion": "gin_trgm_ops"},
    )

    # Indice unico case-insensitive para email
    op.create_index(
        "idx_usuario_email_lower",
        "usuario",
        [sa.text("LOWER(email)")],
        unique=True,
    )

    # Indice parcial para tono en frase
    op.create_index(
        "idx_frase_tono",
        "frase",
        ["tono"],
        postgresql_where=sa.text("tono IS NOT NULL"),
    )

    # --- Funcion y triggers ------------------------------------------------

    op.execute("""
        CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.fecha_actualizacion = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    for table_name in ("palabra", "escenario", "frase", "sugerencia"):
        op.execute(f"""
            CREATE TRIGGER trg_{table_name}_actualizacion
                BEFORE UPDATE ON {table_name}
                FOR EACH ROW
                WHEN (OLD.* IS DISTINCT FROM NEW.*)
                EXECUTE FUNCTION actualizar_fecha_modificacion();
        """)

    op.execute("""
        CREATE OR REPLACE FUNCTION actualizar_ultima_conexion()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.ultima_conexion = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trg_usuario_conexion
            BEFORE UPDATE OF contrasena_hash, preferencias, activo ON usuario
            FOR EACH ROW
            WHEN (OLD.* IS DISTINCT FROM NEW.*)
            EXECUTE FUNCTION actualizar_ultima_conexion();
    """)


def downgrade() -> None:
    """
    Revierte la migracion: elimina todas las tablas y tipos creados.
    Orden inverso para respetar dependencias de foreign keys.
    """

    # Eliminar triggers primero
    for table_name in ("palabra", "escenario", "frase", "sugerencia"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_actualizacion ON {table_name}")

    op.execute("DROP TRIGGER IF EXISTS trg_usuario_conexion ON usuario")

    # Eliminar funciones
    op.execute("DROP FUNCTION IF EXISTS actualizar_fecha_modificacion()")
    op.execute("DROP FUNCTION IF EXISTS actualizar_ultima_conexion()")

    # Eliminar tablas en orden inverso
    op.drop_table("frase_palabra")
    op.drop_table("sugerencia")
    op.drop_table("frase")
    op.drop_table("palabra")
    op.drop_table("escenario")
    op.drop_table("usuario")

    # Eliminar ENUM types
    op.execute("DROP TYPE IF EXISTS tono_frase")
    op.execute("DROP TYPE IF EXISTS sugerencia_estado")
    op.execute("DROP TYPE IF EXISTS sugerencia_tipo")
    op.execute("DROP TYPE IF EXISTS categoria_palabra")

    # Nota: las extensiones NO se eliminan en downgrade
    # (podrian estar siendo usadas por otras bases de datos)
