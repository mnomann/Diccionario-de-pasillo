from typing import Optional

from pydantic import BaseModel, Field


class TraduccionRequest(BaseModel):
    frase: str = Field(..., min_length=1, max_length=500, description="Frase chilena a traducir")
    contexto_id: Optional[int] = Field(None, description="ID del escenario de contexto")
    contexto_nombre: Optional[str] = Field(None, max_length=100, description="Nombre del contexto")
    contexto_personalizado: Optional[str] = Field(
        None, max_length=500, description="Contexto escrito libremente por el usuario"
    )


class ContextoDetectado(BaseModel):
    id: int
    nombre: str
    confianza: float


class ComponenteToken(BaseModel):
    token: str
    traduccion: str
    tipo: str = Field(..., description="muletilla, jerga, abreviacion, neutro, modismo")
    nivel_formalidad: float = Field(..., ge=1.0, le=5.0)


class AnalisisCompleto(BaseModel):
    tono: str = Field(..., description="informal_confianza, informal, formal, etc.")
    intencion_real: str
    nivel_ironia: float = Field(..., ge=0.0, le=10.0)
    nivel_sarcasmo: float = Field(..., ge=0.0, le=10.0)
    nivel_formalidad_general: float = Field(..., ge=1.0, le=5.0)
    requiere_contexto_adicional: bool = False


class TraduccionAlternativa(BaseModel):
    traduccion: str
    contexto: str
    confianza: float = Field(..., ge=0.0, le=1.0)


class TraduccionResponse(BaseModel):
    frase_original: str
    traduccion: Optional[str] = None
    contexto_detectado: Optional[ContextoDetectado] = None
    componentes: list[ComponenteToken] = []
    analisis: Optional[AnalisisCompleto] = None
    confianza: float = Field(..., ge=0.0, le=1.0)
    alternativas: list[TraduccionAlternativa] = []
    sugerencia_contextos: Optional[list[dict]] = None
