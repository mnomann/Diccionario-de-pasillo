import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.comun import Paginacion


class EscenarioResumen(BaseModel):
    id: int
    nombre: str
    icono: Optional[str] = None

    model_config = {"from_attributes": True}


class FraseList(BaseModel):
    id: int
    frase_original: str
    traduccion: str
    escenario: Optional[EscenarioResumen] = None
    tono: Optional[str] = None
    nivel_formalidad: float
    nivel_ironia: float
    fecha_creacion: datetime.datetime

    model_config = {"from_attributes": True}


class FraseDetail(BaseModel):
    id: int
    escenario_id: Optional[int] = None
    escenario: Optional[EscenarioResumen] = None
    frase_original: str
    traduccion: str
    explicacion: Optional[str] = None
    tono: Optional[str] = None
    intencion_real: Optional[str] = None
    nivel_formalidad: float
    nivel_ironia: float
    nivel_sarcasmo: float
    ejemplo_uso: Optional[str] = None
    activo: bool
    fecha_creacion: datetime.datetime
    fecha_actualizacion: Optional[datetime.datetime] = None

    model_config = {"from_attributes": True}


class FraseCreate(BaseModel):
    escenario_id: Optional[int] = None
    frase_original: str = Field(..., min_length=1)
    traduccion: str = Field(..., min_length=1)
    explicacion: Optional[str] = None
    tono: Optional[str] = Field(None, max_length=100)
    intencion_real: Optional[str] = None
    nivel_formalidad: float = Field(5.0, ge=0.0, le=10.0)
    nivel_ironia: float = Field(5.0, ge=0.0, le=10.0)
    nivel_sarcasmo: float = Field(5.0, ge=0.0, le=10.0)
    ejemplo_uso: Optional[str] = None


class FraseUpdate(BaseModel):
    escenario_id: Optional[int] = None
    frase_original: Optional[str] = Field(None, min_length=1)
    traduccion: Optional[str] = Field(None, min_length=1)
    explicacion: Optional[str] = None
    tono: Optional[str] = Field(None, max_length=100)
    intencion_real: Optional[str] = None
    nivel_formalidad: Optional[float] = Field(None, ge=0.0, le=10.0)
    nivel_ironia: Optional[float] = Field(None, ge=0.0, le=10.0)
    nivel_sarcasmo: Optional[float] = Field(None, ge=0.0, le=10.0)
    ejemplo_uso: Optional[str] = None
    activo: Optional[bool] = None


class PaginatedFraseResponse(BaseModel):
    data: list[FraseList]
    paginacion: Paginacion
