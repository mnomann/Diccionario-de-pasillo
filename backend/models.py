"""
Modelos SQLAlchemy para la plataforma Desenreda.

Refleja exactamente el esquema definido en init.sql con todas las
relaciones, restricciones e indices mapeados a traves de SQLAlchemy.

Tecnologia: SQLAlchemy 2.0+ con typing progresivo.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()

# ============================================================================
# Enums (reflejan los ENUM types de PostgreSQL)
# ============================================================================

CategoriaPalabra = Enum(
    "modismo",
    "muletilla",
    "jerga",
    "insulto_ligero",
    "abreviacion",
    name="categoria_palabra",
)

SugerenciaTipo = Enum(
    "palabra",
    "frase",
    "escenario",
    name="sugerencia_tipo",
)

SugerenciaEstado = Enum(
    "pendiente",
    "aprobado",
    "rechazado",
    name="sugerencia_estado",
)

# Lista de tonos validos para Frase (CHECK constraint en BD)
TONOS_FRASE = frozenset({
    "ironico",
    "sarcastico",
    "directo",
    "humoristico",
    "motivacional",
    "neutro",
})


# ============================================================================
# Tabla intermedia: frase <-> palabra (relacion N:M)
# ============================================================================

class FrasePalabra(Base):
    """
    Tabla intermedia para la relacion muchos-a-muchos entre Frase y Palabra.
    Incluye un campo de relevancia para uso futuro con algoritmos de ML.
    """

    __tablename__ = "frase_palabra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frase_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("frase.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    palabra_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("palabra.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    relevancia: Mapped[Optional[int]] = mapped_column(
        Integer, default=1, server_default="1"
    )

    __table_args__ = (
        UniqueConstraint("frase_id", "palabra_id", name="uq_frase_palabra"),
        CheckConstraint("relevancia BETWEEN 1 AND 5", name="ck_frase_palabra_relevancia"),
    )

    # Relationships
    frase: Mapped["Frase"] = relationship(back_populates="palabras_relacion")
    palabra: Mapped["Palabra"] = relationship(back_populates="frases_relacion")

    def __repr__(self) -> str:
        return f"<FrasePalabra(frase_id={self.frase_id}, palabra_id={self.palabra_id}, r={self.relevancia})>"


# ============================================================================
# Usuario
# ============================================================================

class Usuario(Base):
    """
    Usuarios registrados de la plataforma Desenreda.
    Almacena preferencias en JSONB para flexibilidad en la configuracion.
    """

    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    preferencias: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, server_default="true")
    fecha_registro: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.now
    )
    ultima_conexion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    sugerencias: Mapped[list["Sugerencia"]] = relationship(
        "Sugerencia", back_populates="usuario"
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, email={self.email}, activo={self.activo})>"


# ============================================================================
# Palabra
# ============================================================================

class Palabra(Base):
    """
    Catalogo de modismos, muletillas, jerga e insultos ligeros chilenos.
    Incluye columna generada TSVECTOR para busqueda de texto completo.

    Atributos principales:
        - palabra: el termino en espanol chileno
        - traduccion: significado neutro (espanol estandar)
        - categoria: clasificacion del tipo de palabra
        - variantes: JSONB array con variantes regionales/de uso
        - texto_busqueda: columna TSVECTOR generada automaticamente
    """

    __tablename__ = "palabra"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    palabra: Mapped[str] = mapped_column(String(200), nullable=False)
    traduccion: Mapped[str] = mapped_column(String(500), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)  # Enum manejado en BD
    nivel_formalidad: Mapped[Optional[int]] = mapped_column(
        Integer, default=2, server_default="2"
    )
    nivel_ironia: Mapped[Optional[int]] = mapped_column(
        Integer, default=0, server_default="0"
    )
    nivel_sarcasmo: Mapped[Optional[int]] = mapped_column(
        Integer, default=0, server_default="0"
    )
    pronunciacion_fonetica: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    ejemplo_uso: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    nota_cultural: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    origen: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    variantes: Mapped[Optional[list[Any]]] = mapped_column(
        JSON, default=list, server_default="'[]'::jsonb"
    )
    activo: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.now
    )
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    texto_busqueda: Mapped[Optional[str]] = mapped_column(
        TSVECTOR, nullable=True
    )  # Columna generada en BD

    __table_args__ = (
        CheckConstraint("nivel_formalidad BETWEEN 1 AND 5", name="ck_palabra_formalidad"),
        CheckConstraint("nivel_ironia BETWEEN 0 AND 10", name="ck_palabra_ironia"),
        CheckConstraint("nivel_sarcasmo BETWEEN 0 AND 10", name="ck_palabra_sarcasmo"),
    )

    # Relationships
    frases_relacion: Mapped[list["FrasePalabra"]] = relationship(
        "FrasePalabra", back_populates="palabra"
    )

    @property
    def frases(self) -> list["Frase"]:
        """Acceso directo a las frases asociadas via tabla intermedia."""
        return [fp.frase for fp in self.frases_relacion]

    def __repr__(self) -> str:
        return f"<Palabra(id={self.id}, palabra='{self.palabra}', categoria={self.categoria})>"


# ============================================================================
# Escenario
# ============================================================================

class Escenario(Base):
    """
    Escenarios contextuales donde se usan las frases con modismos.
    Proporciona el contexto situacional para entender cuando y
    donde usar cada expresion.
    """

    __tablename__ = "escenario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    icono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    activo: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.now
    )
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    frases: Mapped[list["Frase"]] = relationship(
        "Frase", back_populates="escenario", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Escenario(id={self.id}, nombre='{self.nombre}')>"


# ============================================================================
# Conversacion
# ============================================================================

class Conversacion(Base):
    __tablename__ = "conversacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frase_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("frase.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    participantes: Mapped[Optional[list[Any]]] = mapped_column(
        JSON, default=list, server_default="'[]'::jsonb"
    )

    # Relationships
    frase: Mapped["Frase"] = relationship(back_populates="conversacion")
    mensajes: Mapped[list["Mensaje"]] = relationship(
        "Mensaje", back_populates="conversacion",
        cascade="all, delete-orphan",
        order_by="Mensaje.orden",
    )

    def __repr__(self) -> str:
        return f"<Conversacion(id={self.id}, frase_id={self.frase_id})>"


class Mensaje(Base):
    __tablename__ = "mensaje"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversacion_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("conversacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    emisor: Mapped[str] = mapped_column(String(200), nullable=False)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    es_modismo: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    orden: Mapped[Optional[int]] = mapped_column(
        Integer, default=0, server_default="0"
    )

    # Relationships
    conversacion: Mapped["Conversacion"] = relationship(back_populates="mensajes")

    def __repr__(self) -> str:
        return f"<Mensaje(id={self.id}, orden={self.orden}, modismo={self.es_modismo})>"


# ============================================================================
# Frase
# ============================================================================

class Frase(Base):
    """
    Frases con modismos asociadas a escenarios especificos.
    Incluye metadatos sobre tono, intencion real y niveles de
    formalidad/ironia/sarcasmo para ayudar a personas neurodivergentes
    a interpretar correctamente la intencion comunicativa.
    """

    __tablename__ = "frase"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    escenario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("escenario.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    frase_original: Mapped[str] = mapped_column(String(500), nullable=False)
    traduccion: Mapped[str] = mapped_column(String(500), nullable=False)
    explicacion: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    tono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    intencion_real: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    nivel_formalidad: Mapped[Optional[int]] = mapped_column(
        Integer, default=3, server_default="3"
    )
    nivel_ironia: Mapped[Optional[int]] = mapped_column(
        Integer, default=0, server_default="0"
    )
    nivel_sarcasmo: Mapped[Optional[int]] = mapped_column(
        Integer, default=0, server_default="0"
    )
    ejemplo_uso: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    activo: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.now
    )
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint("nivel_formalidad BETWEEN 1 AND 5", name="ck_frase_formalidad"),
        CheckConstraint("nivel_ironia BETWEEN 0 AND 10", name="ck_frase_ironia"),
        CheckConstraint("nivel_sarcasmo BETWEEN 0 AND 10", name="ck_frase_sarcasmo"),
    )

    # Relationships
    escenario: Mapped["Escenario"] = relationship("Escenario", back_populates="frases")
    palabras_relacion: Mapped[list["FrasePalabra"]] = relationship(
        "FrasePalabra", back_populates="frase"
    )
    conversacion: Mapped[Optional["Conversacion"]] = relationship(
        "Conversacion", back_populates="frase",
        cascade="all, delete-orphan",
    )

    @property
    def palabras(self) -> list["Palabra"]:
        """Acceso directo a las palabras asociadas via tabla intermedia."""
        return [fp.palabra for fp in self.palabras_relacion]

    def __repr__(self) -> str:
        return f"<Frase(id={self.id}, tono={self.tono}, escenario_id={self.escenario_id})>"


# ============================================================================
# Sugerencia
# ============================================================================

class Sugerencia(Base):
    """
    Sugerencias de usuarios para nuevas palabras, frases o escenarios.
    Pueden ser anonimas (usuario_id = NULL) o asociadas a un usuario registrado.
    El contenido varia segun el tipo y se almacena como JSONB.
    """

    __tablename__ = "sugerencia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("usuario.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # Enum manejado en BD
    contenido: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    estado: Mapped[Optional[str]] = mapped_column(
        String(20), default="pendiente", server_default="'pendiente'"
    )  # Enum manejado en BD
    comentario_moderador: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    usuario_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=datetime.now
    )
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    usuario: Mapped[Optional["Usuario"]] = relationship("Usuario", back_populates="sugerencias")

    def __repr__(self) -> str:
        return (
            f"<Sugerencia(id={self.id}, tipo={self.tipo}, "
            f"estado={self.estado}, usuario_id={self.usuario_id})>"
        )
