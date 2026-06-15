import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.comun import Paginacion
from app.schemas.frase import FraseList


class EscenarioList(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    total_frases: int = Field(0, description="Cantidad de frases asociadas")
    activo: bool
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class EscenarioDetail(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    activo: bool
    fecha_creacion: datetime.datetime
    fecha_actualizacion: Optional[datetime.datetime] = None
    frases: list[FraseList] = []

    model_config = {"from_attributes": True}


class EscenarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    icono: Optional[str] = Field(None, max_length=100)


class EscenarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    icono: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None


class PaginatedEscenarioResponse(BaseModel):
    data: list[EscenarioList]
    paginacion: Paginacion
