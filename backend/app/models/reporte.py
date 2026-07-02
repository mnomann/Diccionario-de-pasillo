import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Reporte(Base):
    __tablename__ = "reporte"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="reporte_tipo ENUM: error_contenido, palabra_faltante, error_ortografia, sugerencia_mejora, otro",
    )
    entidad_tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="reporte_entidad ENUM: palabra, frase, escenario, general",
    )
    entidad_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    detalle_contacto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pendiente",
        server_default="pendiente",
        comment="reporte_estado ENUM: pendiente, en_revision, resuelto, rechazado",
    )
    comentario_admin: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resuelto_por: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,
    )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    fecha_actualizacion: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    # Relaciones
    usuario: Mapped[Optional["Usuario"]] = relationship(
        "Usuario",
        foreign_keys=[usuario_id],
        backref="reportes_usuario",
        lazy="selectin",
    )
    admin: Mapped[Optional["Usuario"]] = relationship(
        "Usuario",
        foreign_keys=[resuelto_por],
        backref="reportes_resueltos",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Reporte id={self.id} tipo={self.tipo} estado={self.estado}>"
