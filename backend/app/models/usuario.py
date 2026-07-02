import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.sugerencia import Sugerencia


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    contrasena_hash: Mapped[str] = mapped_column(Text, nullable=False)
    es_admin: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, server_default="false", nullable=True
    )
    preferencias: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default={})
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_registro: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    ultima_conexion: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    sugerencias: Mapped[list["Sugerencia"]] = relationship(
        "Sugerencia",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email}>"
