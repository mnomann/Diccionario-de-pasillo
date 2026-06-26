from app.routers.auth import router as auth_router
from app.routers.palabras import router as palabras_router
from app.routers.frases import router as frases_router
from app.routers.escenarios import router as escenarios_router
from app.routers.sugerencias import router as sugerencias_router
from app.routers.usuarios import router as usuarios_router
from app.routers.traducciones import router as traducciones_router

__all__ = [
    "auth_router",
    "palabras_router",
    "frases_router",
    "escenarios_router",
    "sugerencias_router",
    "usuarios_router",
    "traducciones_router",
]
