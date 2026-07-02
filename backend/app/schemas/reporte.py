import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.comun import Paginacion
from app.schemas.usuario import UsuarioResponse


class ReporteCreate(BaseModel):
    tipo: str = Field(
        ...,
        description="Tipo de reporte: error_contenido, palabra_faltante, error_ortografia, sugerencia_mejora, otro",
    )
    entidad_tipo: str = Field(
        ...,
        description="Tipo de entidad reportada: palabra, frase, escenario, general",
    )
    entidad_id: Optional[int] = Field(
        None, description="ID de la entidad reportada (opcional)"
    )
    descripcion: str = Field(
        ..., min_length=1, max_length=5000, description="Descripcion del reporte"
    )
class ReporteResponse(BaseModel):
    id: int
    tipo: str
    entidad_tipo: str
    entidad_id: Optional[int] = None
    descripcion: str
    detalle_contacto: Optional[str] = None
    estado: str
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class ReporteDetail(BaseModel):
    id: int
    tipo: str
    entidad_tipo: str
    entidad_id: Optional[int] = None
    descripcion: str
    detalle_contacto: Optional[str] = None
    estado: str
    fecha_creacion: datetime.datetime
    usuario: Optional[UsuarioResponse] = None
    comentario_admin: Optional[str] = None
    resuelto_por: Optional[int] = None
    fecha_actualizacion: Optional[datetime.datetime] = None

    model_config = {"from_attributes": True}


class ReporteUpdate(BaseModel):
    estado: Optional[str] = Field(
        None,
        description="Nuevo estado: pendiente, en_revision, resuelto, rechazado",
    )
    comentario_admin: Optional[str] = Field(
        None, max_length=5000, description="Comentario del administrador"
    )


class PaginatedReporteResponse(BaseModel):
    data: list[ReporteDetail]
    paginacion: Paginacion
