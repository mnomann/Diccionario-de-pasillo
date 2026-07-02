from app.schemas.comun import ErrorResponse, MensajeResponse, Paginacion
from app.schemas.usuario import (
    LoginRequest,
    LoginResponse,
    UsuarioCreate,
    UsuarioMe,
    UsuarioResponse,
)
from app.schemas.palabra import (
    PalabraCreate,
    PalabraDetail,
    PalabraList,
    PalabraUpdate,
    PaginatedPalabraResponse,
)
from app.schemas.frase import (
    FraseCreate,
    FraseDetail,
    FraseList,
    FraseUpdate,
    PaginatedFraseResponse,
)
from app.schemas.escenario import (
    EscenarioCreate,
    EscenarioDetail,
    EscenarioList,
    EscenarioUpdate,
    PaginatedEscenarioResponse,
)
from app.schemas.sugerencia import (
    SugerenciaCreate,
    SugerenciaDetail,
    SugerenciaList,
    SugerenciaResponse,
    PaginatedSugerenciaResponse,
)
from app.schemas.reporte import (
    PaginatedReporteResponse,
    ReporteCreate,
    ReporteDetail,
    ReporteResponse,
    ReporteUpdate,
)

__all__ = [
    "ErrorResponse",
    "MensajeResponse",
    "Paginacion",
    "UsuarioCreate",
    "UsuarioResponse",
    "UsuarioMe",
    "LoginRequest",
    "LoginResponse",
    "PalabraCreate",
    "PalabraUpdate",
    "PalabraList",
    "PalabraDetail",
    "PaginatedPalabraResponse",
    "FraseCreate",
    "FraseUpdate",
    "FraseList",
    "FraseDetail",
    "PaginatedFraseResponse",
    "EscenarioCreate",
    "EscenarioUpdate",
    "EscenarioList",
    "EscenarioDetail",
    "PaginatedEscenarioResponse",
    "SugerenciaCreate",
    "SugerenciaResponse",
    "SugerenciaList",
    "SugerenciaDetail",
    "PaginatedSugerenciaResponse",
    "ReporteCreate",
    "ReporteResponse",
    "ReporteDetail",
    "ReporteUpdate",
    "PaginatedReporteResponse",
]
