import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.escenario import Escenario


class Frase(Base):
    __tablename__ = "frase"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    escenario_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("escenario.id", ondelete="CASCADE"), nullable=True, index=True
    )
    frase_original: Mapped[str] = mapped_column(Text, nullable=False)
    traduccion: Mapped[str] = mapped_column(Text, nullable=False)
    significado_literal: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    explicacion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tono: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    intencion_real: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nivel_formalidad: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    nivel_ironia: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    nivel_sarcasmo: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    ejemplo_uso: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    fecha_actualizacion: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    escenario: Mapped[Optional["Escenario"]] = relationship(
        "Escenario",
        back_populates="frases",
    )

    def __repr__(self) -> str:
        return f"<Frase id={self.id}>"
