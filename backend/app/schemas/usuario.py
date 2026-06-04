import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electronico")
    contrasena: str = Field(
        ..., min_length=6, max_length=128, description="Contrasena del usuario"
    )
    preferencias: Optional[dict] = Field(None, description="Preferencias del usuario")


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: datetime.datetime

    model_config = {"from_attributes": True}


class UsuarioMe(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: datetime.datetime
    preferencias: Optional[dict] = None
    ultima_conexion: Optional[datetime.datetime] = None
    estadisticas: Optional[dict] = Field(
        None, description="Estadisticas del usuario"
    )

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Correo electronico")
    contrasena: str = Field(..., description="Contrasena")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token JWT")
    token_type: str = Field("bearer", description="Tipo de token")
    expira_en: int = Field(..., description="Tiempo de expiracion en segundos")
    usuario: UsuarioResponse
