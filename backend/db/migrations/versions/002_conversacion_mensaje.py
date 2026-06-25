"""
Migration 002_conversacion_mensaje: Agrega tablas de conversacion y mensaje.

Descripcion:
    Crea las tablas conversacion y mensaje para almacenar conversaciones
    de ejemplo asociadas a cada frase. Incluye sus indices y comentarios.

Revision ID: 002_conversacion_mensaje
Revises: 001_initial
Create Date: 2026-06-25 18:00:00.000000
"""

from typing import Final, Optional, Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: Final[str] = "002_conversacion_mensaje"
down_revision: Optional[str] = "001_initial"
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    op.create_table(
        "conversacion",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("frase_id", sa.Integer(), nullable=False),
        sa.Column("participantes", sa.JSON(),
                  server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.ForeignKeyConstraint(
            ["frase_id"],
            ["frase.id"],
            name="fk_conversacion_frase",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("frase_id", name="uq_conversacion_frase"),
    )

    op.create_table(
        "mensaje",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("conversacion_id", sa.Integer(), nullable=False),
        sa.Column("emisor", sa.String(length=200), nullable=False),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("es_modismo", sa.Boolean(),
                  server_default=sa.text("false"), nullable=False),
        sa.Column("orden", sa.Integer(),
                  server_default=sa.text("0"), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversacion_id"],
            ["conversacion.id"],
            name="fk_mensaje_conversacion",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "idx_conversacion_frase",
        "conversacion",
        ["frase_id"],
    )

    op.create_index(
        "idx_mensaje_conversacion",
        "mensaje",
        ["conversacion_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_mensaje_conversacion", table_name="mensaje")
    op.drop_index("idx_conversacion_frase", table_name="conversacion")
    op.drop_table("mensaje")
    op.drop_table("conversacion")
