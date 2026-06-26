from typing import Any, Optional

from pydantic import BaseModel, Field


class Paginacion(BaseModel):
    pagina: int = Field(..., ge=1, description="Pagina actual")
    tamanio: int = Field(..., ge=1, le=100, description="Elementos por pagina")
    total_elementos: int = Field(..., ge=0, description="Total de elementos")
    total_paginas: int = Field(..., ge=0, description="Total de paginas")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Mensaje de error")
    detalle: str = Field("", description="Detalle adicional del error")
    codigo: str = Field("ERROR_DESCONOCIDO", description="Codigo del error")
    detalles: Optional[list[dict[str, Any]]] = Field(None, description="Detalles de validacion")


class MensajeResponse(BaseModel):
    mensaje: str = Field(..., description="Mensaje informativo")
