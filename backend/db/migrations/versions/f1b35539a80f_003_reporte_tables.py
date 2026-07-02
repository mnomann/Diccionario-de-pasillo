"""003_reporte_tables

Revision ID: f1b35539a80f
Revises: 002_conversacion_mensaje
Create Date: 2026-07-01 09:13:58.965250
"""
from typing import Final, Optional, Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: Final[str] = "f1b35539a80f"
down_revision: Optional[str] = "002_conversacion_mensaje"
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    op.create_table(
        "reporte",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tipo", sa.String(length=50), nullable=False,
                  comment="reporte_tipo ENUM: error_contenido, palabra_faltante, error_ortografia, sugerencia_mejora, otro"),
        sa.Column("entidad_tipo", sa.String(length=50), nullable=False,
                  comment="reporte_entidad ENUM: palabra, frase, escenario, general"),
        sa.Column("entidad_id", sa.Integer(), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("detalle_contacto", sa.Text(), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("estado", sa.String(length=50), nullable=False,
                  server_default=sa.text("'pendiente'"),
                  comment="reporte_estado ENUM: pendiente, en_revision, resuelto, rechazado"),
        sa.Column("comentario_admin", sa.Text(), nullable=True),
        sa.Column("resuelto_por", sa.Integer(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"],
                                name="fk_reporte_usuario", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["resuelto_por"], ["usuario.id"],
                                name="fk_reporte_resuelto_por", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_reporte_usuario_id", "reporte", ["usuario_id"])


def downgrade() -> None:
    op.drop_index("idx_reporte_usuario_id", table_name="reporte")
    op.drop_table("reporte")
