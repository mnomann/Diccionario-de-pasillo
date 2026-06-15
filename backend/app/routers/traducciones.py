from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas.comun import ErrorResponse
from app.schemas.traduccion import TraduccionRequest, TraduccionResponse
from app.services.traduccion_service import traducir_frase

router = APIRouter(prefix="/traducciones", tags=["Traducciones"])


@router.post(
    "/traducir",
    response_model=TraduccionResponse,
    summary="Traducir una frase chilena a lenguaje neutral",
    responses={
        422: {"model": ErrorResponse, "description": "Error de validacion"},
        502: {"model": ErrorResponse, "description": "Error del servicio de traduccion"},
    },
)
async def traducir(
    request: TraduccionRequest,
) -> Any:
    """Traduce una frase chilena a lenguaje neutral usando IA.

    Recibe una frase (obligatorio) y opcionalmente un contexto.
    Devuelve la traduccion, desglose por componentes, analisis de tono/ironia
    y nivel de confianza.
    """
    try:
        resultado = await traducir_frase(request)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al procesar la traduccion: {exc}",
        ) from exc

    return resultado
