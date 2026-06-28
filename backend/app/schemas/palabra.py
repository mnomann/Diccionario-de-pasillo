import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.comun import Paginacion


class PalabraList(BaseModel):
    id: int
    palabra: str
    traduccion: str
    significado_literal: Optional[str] = None
    categoria: str
    nivel_formalidad: float
    nivel_ironia: float
    ejemplo_uso: Optional[str] = None
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class PalabraDetail(BaseModel):
    id: int
    palabra: str
    traduccion: str
    significado_literal: Optional[str] = None
    categoria: str
    nivel_formalidad: float
    nivel_ironia: float
    nivel_sarcasmo: float
    pronunciacion_fonetica: Optional[str] = None
    ejemplo_uso: Optional[str] = None
    nota_cultural: Optional[str] = None
    origen: Optional[str] = None
    variantes: Optional[list] = None
    activo: bool
    fecha_creacion: datetime.datetime
    fecha_actualizacion: Optional[datetime.datetime] = None

    model_config = {"from_attributes": True}


class PalabraCreate(BaseModel):
    palabra: str = Field(..., min_length=1, max_length=200)
    traduccion: str = Field(..., min_length=1)
    significado_literal: Optional[str] = None
    categoria: str = Field(..., min_length=1, max_length=100)
    nivel_formalidad: float = Field(5.0, ge=0.0, le=10.0)
    nivel_ironia: float = Field(5.0, ge=0.0, le=10.0)
    nivel_sarcasmo: float = Field(5.0, ge=0.0, le=10.0)
    pronunciacion_fonetica: Optional[str] = None
    ejemplo_uso: Optional[str] = None
    nota_cultural: Optional[str] = None
    origen: Optional[str] = None
    variantes: Optional[list] = None


class PalabraUpdate(BaseModel):
    palabra: Optional[str] = Field(None, min_length=1, max_length=200)
    traduccion: Optional[str] = Field(None, min_length=1)
    significado_literal: Optional[str] = None
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    nivel_formalidad: Optional[float] = Field(None, ge=0.0, le=10.0)
    nivel_ironia: Optional[float] = Field(None, ge=0.0, le=10.0)
    nivel_sarcasmo: Optional[float] = Field(None, ge=0.0, le=10.0)
    pronunciacion_fonetica: Optional[str] = None
    ejemplo_uso: Optional[str] = None
    nota_cultural: Optional[str] = None
    origen: Optional[str] = None
    variantes: Optional[list] = None
    activo: Optional[bool] = None


class PaginatedPalabraResponse(BaseModel):
    data: list[PalabraList]
    paginacion: Paginacion
