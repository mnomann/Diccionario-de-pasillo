import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Palabra(Base):
    __tablename__ = "palabra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    palabra: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    traduccion: Mapped[str] = mapped_column(Text, nullable=False)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    nivel_formalidad: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    nivel_ironia: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    nivel_sarcasmo: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pronunciacion_fonetica: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    ejemplo_uso: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nota_cultural: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    origen: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    variantes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=[])
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

    def __repr__(self) -> str:
        return f"<Palabra id={self.id} palabra={self.palabra}>"
