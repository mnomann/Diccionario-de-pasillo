import json
import logging
from typing import Any

import google.generativeai as genai
from fastapi import HTTPException, status

from app.config import settings
from app.schemas.traduccion import (
    AnalisisCompleto,
    ComponenteToken,
    ContextoDetectado,
    TraduccionAlternativa,
    TraduccionRequest,
    TraduccionResponse,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configurar Gemini SDK
# ---------------------------------------------------------------------------
genai.configure(api_key=settings.GOOGLE_API_KEY)

# ---------------------------------------------------------------------------
# Prompt del sistema (System Instruction)
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTION = (
    "Eres un traductor de lenguaje chileno. Tu objetivo es explicar modismos, "
    "ironia y sarcasmo a personas que necesitan respuestas muy literales.\n"
    "REGLAS ESTRICTAS:\n"
    "- Usa lenguaje extremadamente simple, cotidiano y corto.\n"
    "- No uses palabras formales, psicologicas ni complejas. Explicalo como si "
    "hablaras con un nino.\n"
    "- Devuelve estrictamente el JSON solicitado.\n"
    "\n"
    "EJEMPLO 1:\n"
    "Contexto: Un companero llega tarde y sudado.\n"
    'Frase: "Me vine rajado."\n'
    "Salida esperada: "
    '{"es_ironico": false, "significado_literal": "Vine corriendo muy rapido.", '
    '"modismos_detectados": ["rajado"], '
    '"explicacion_social": "Usa una palabra informal para decir que corrio rapido '
    'porque estaba atrasado."}\n'
    "\n"
    "EJEMPLO 2:\n"
    'Contexto: A un alumno se le cae el cafe en el notebook.\n'
    'Frase: "Puta, la wea bacan, justo lo que necesitaba hoy."\n'
    "Salida esperada: "
    '{"es_ironico": true, "significado_literal": "Es una situacion terrible.", '
    '"modismos_detectados": ["wea", "bacan", "puta"], '
    '"explicacion_social": "Esta muy enojado. Dice que es algo bueno (bacan) '
    'como una broma por la mala suerte."}'
)


def _construir_mensaje_usuario(request: TraduccionRequest) -> str:
    """Construye el mensaje que se envia al modelo con el contexto y la frase."""
    partes: list[str] = []

    if request.contexto_personalizado:
        partes.append(f"Contexto: {request.contexto_personalizado}")
    elif request.contexto_nombre:
        partes.append(f"Contexto: {request.contexto_nombre}")
    elif request.contexto_id is not None:
        partes.append(f"Contexto ID: {request.contexto_id}")

    partes.append(f"Frase: \"{request.frase}\"")
    return "\n".join(partes)


def _parsear_respuesta_ia(texto: str) -> dict[str, Any]:
    """Intenta extraer un diccionario desde la respuesta de la IA."""
    contenido = texto.strip()

    if contenido.startswith("```"):
        lineas = contenido.splitlines()
        lineas_filtradas = [
            l for l in lineas if not l.startswith("```")
        ]
        contenido = "\n".join(lineas_filtradas).strip()

    return json.loads(contenido)


def _transformar_respuesta(
    request: TraduccionRequest,
    datos_ia: dict[str, Any],
) -> TraduccionResponse:
    """Transforma el JSON de la IA al esquema TraduccionResponse."""
    es_ironico = datos_ia.get("es_ironico", False)
    significado_literal = datos_ia.get("significado_literal", "")
    modismos_detectados: list[str] = datos_ia.get("modismos_detectados", [])
    explicacion_social = datos_ia.get("explicacion_social", "")

    componentes: list[ComponenteToken] = []
    for modismo in modismos_detectados:
        componentes.append(
            ComponenteToken(
                token=modismo,
                traduccion="",
                tipo="jerga",
                nivel_formalidad=1.0,
            )
        )

    nivel_ironia = 8.0 if es_ironico else 0.0
    analisis = AnalisisCompleto(
        tono="informal",
        intencion_real=explicacion_social if explicacion_social else significado_literal,
        nivel_ironia=nivel_ironia,
        nivel_sarcasmo=0.0,
        nivel_formalidad_general=1.5,
        requiere_contexto_adicional=False,
    )

    confianza = 0.70 if es_ironico else 0.85

    return TraduccionResponse(
        frase_original=request.frase,
        traduccion=significado_literal or None,
        contexto_detectado=None,
        componentes=componentes,
        analisis=analisis,
        confianza=confianza,
        alternativas=[],
        sugerencia_contextos=None,
    )


async def traducir_frase(request: TraduccionRequest) -> TraduccionResponse:
    """Envia la frase a Gemini y retorna la traduccion estructurada."""
    logger.info(
        "Solicitando traduccion para frase=%s contexto_id=%s contexto_nombre=%s contexto_personalizado=%s",
        request.frase,
        request.contexto_id,
        request.contexto_nombre,
        request.contexto_personalizado,
    )

    modelo = genai.GenerativeModel(
        model_name=settings.GOOGLE_MODEL,
        system_instruction=SYSTEM_INSTRUCTION,
    )

    mensaje_usuario = _construir_mensaje_usuario(request)

    try:
        respuesta = await modelo.generate_content_async(mensaje_usuario)
    except Exception as exc:
        logger.error("Error al llamar a Gemini: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"El servicio de traduccion no esta disponible temporalmente: {exc}",
        ) from exc

    if not respuesta.text:
        logger.error("Gemini devolvio respuesta vacia")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El servicio de traduccion devolvio una respuesta vacia",
        )

    try:
        datos_ia = _parsear_respuesta_ia(respuesta.text)
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        logger.error(
            "Respuesta invalida de Gemini (JSON malformado): %s | texto=%s",
            exc,
            respuesta.text,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El servicio de traduccion devolvio un formato no valido",
        ) from exc

    return _transformar_respuesta(request, datos_ia)
