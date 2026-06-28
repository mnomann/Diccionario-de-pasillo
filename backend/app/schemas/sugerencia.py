import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.comun import Paginacion


class SugerenciaCreate(BaseModel):
    tipo: str = Field(..., description="Tipo de sugerencia (nueva_palabra, correccion, otro)")
    contenido: dict = Field(..., description="Contenido de la sugerencia")
    usuario_email: Optional[EmailStr] = Field(None, description="Email del usuario no registrado")


class SugerenciaResponse(BaseModel):
    id: int
    tipo: str
    estado: str
    mensaje: str = Field("Sugerencia recibida correctamente", description="Mensaje de confirmacion")
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class SugerenciaList(BaseModel):
    id: int
    tipo: str
    contenido_resumen: str = Field(..., description="Resumen legible del contenido")
    estado: str
    comentario_moderador: Optional[str] = None
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class SugerenciaDetail(BaseModel):
    id: int
    tipo: str
    contenido: dict
    estado: str
    comentario_moderador: Optional[str] = None
    usuario_email: Optional[str] = None
    fecha_creacion: datetime.datetime
    fecha_actualizacion: datetime.datetime

    model_config = {"from_attributes": True}


class PaginatedSugerenciaResponse(BaseModel):
    data: list[SugerenciaList]
    paginacion: Paginacion
