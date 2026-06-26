from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.frase import Frase


class Conversacion(Base):
    __tablename__ = "conversacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frase_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("frase.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    participantes: Mapped[Optional[list[Any]]] = mapped_column(
        JSONB, default=list, server_default="'[]'::jsonb", nullable=False
    )

    frase: Mapped["Frase"] = relationship(back_populates="conversacion")
    mensajes: Mapped[list["Mensaje"]] = relationship(
        "Mensaje", back_populates="conversacion", cascade="all, delete-orphan",
        order_by="Mensaje.orden",
    )

    def __repr__(self) -> str:
        return f"<Conversacion id={self.id} frase_id={self.frase_id}>"


class Mensaje(Base):
    __tablename__ = "mensaje"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversacion_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conversacion.id", ondelete="CASCADE"), nullable=False, index=True
    )
    emisor: Mapped[str] = mapped_column(String(200), nullable=False)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    es_modismo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    conversacion: Mapped["Conversacion"] = relationship(back_populates="mensajes")

    def __repr__(self) -> str:
        return f"<Mensaje id={self.id} orden={self.orden} modismo={self.es_modismo}>"
