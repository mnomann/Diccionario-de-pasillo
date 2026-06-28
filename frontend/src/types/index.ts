export interface Paginacion {
  pagina: number
  tamanio: number
  total_elementos: number
  total_paginas: number
}

export interface PalabraList {
  id: number
  palabra: string
  traduccion: string
  categoria: string
  nivel_formalidad: number
  nivel_ironia: number
  ejemplo_uso: string | null
  fecha_creacion: string
}

export interface PalabraDetail {
  id: number
  palabra: string
  traduccion: string
  categoria: string
  nivel_formalidad: number
  nivel_ironia: number
  nivel_sarcasmo: number
  pronunciacion_fonetica: string | null
  ejemplo_uso: string | null
  nota_cultural: string | null
  origen: string | null
  variantes: string[] | null
  activo: boolean
  fecha_creacion: string
  fecha_actualizacion: string | null
}

export interface PaginatedPalabras {
  data: PalabraList[]
  paginacion: Paginacion
}

export interface EscenarioResumen {
  id: number
  nombre: string
  icono: string | null
}

export interface FraseList {
  id: number
  frase_original: string
  traduccion: string
  escenario: EscenarioResumen | null
  tono: string | null
  nivel_formalidad: number
  nivel_ironia: number
  fecha_creacion: string
}

export interface MensajeChat {
  emisor: string
  texto: string
  es_modismo: boolean
}

export interface Conversacion {
  participantes: string[]
  mensajes: MensajeChat[]
}

export interface FraseDetail {
  id: number
  escenario_id: number | null
  escenario: EscenarioResumen | null
  frase_original: string
  traduccion: string
  explicacion: string | null
  tono: string | null
  intencion_real: string | null
  nivel_formalidad: number
  nivel_ironia: number
  nivel_sarcasmo: number
  ejemplo_uso: string | null
  activo: boolean
  fecha_creacion: string
  fecha_actualizacion: string | null
}

export interface PaginatedFrases {
  data: FraseList[]
  paginacion: Paginacion
}

export interface EscenarioList {
  id: number
  nombre: string
  descripcion: string | null
  icono: string | null
  total_frases: number
  activo: boolean
  fecha_creacion: string
}

export interface EscenarioDetail {
  id: number
  nombre: string
  descripcion: string | null
  icono: string | null
  activo: boolean
  fecha_creacion: string
  fecha_actualizacion: string | null
  frases: FraseDetail[]
}

export interface PaginatedEscenarios {
  data: EscenarioList[]
  paginacion: Paginacion
}

export interface UsuarioCreate {
  nombre: string
  email: string
  contrasena: string
  preferencias?: Record<string, string>
}

export interface UsuarioResponse {
  id: number
  nombre: string
  email: string
  fecha_registro: string
}

export interface UsuarioMe {
  id: number
  nombre: string
  email: string
  fecha_registro: string
  preferencias: Record<string, string> | null
  ultima_conexion: string | null
  estadisticas: Record<string, unknown> | null
}

export interface LoginRequest {
  email: string
  contrasena: string
}

export interface LoginResponse {
  token: string
  token_type: string
  expira_en: number
  usuario: UsuarioResponse
}

export interface SugerenciaCreate {
  tipo: string
  contenido: Record<string, unknown>
  usuario_email?: string
}

export interface SugerenciaResponse {
  id: number
  tipo: string
  estado: string
  mensaje: string
  fecha_creacion: string
}

export interface SugerenciaList {
  id: number
  tipo: string
  contenido_resumen: string
  estado: string
  comentario_moderador: string | null
  fecha_creacion: string
}

export interface PaginatedSugerencias {
  data: SugerenciaList[]
  paginacion: Paginacion
}

export interface ErrorResponse {
  error: string
  detalle: string
  codigo: string
  detalles?: Record<string, unknown>[]
}

// ============================================================
// Traducciones (IA con Gemini)
// ============================================================

export interface TraduccionRequest {
  frase: string
  contexto_id?: number | null
  contexto_nombre?: string | null
  contexto_personalizado?: string | null
}

export interface ContextoDetectado {
  id: number
  nombre: string
  confianza: number
}

export interface ComponenteToken {
  token: string
  traduccion: string
  tipo: string
  nivel_formalidad: number
}

export interface AnalisisCompleto {
  tono: string
  intencion_real: string
  nivel_ironia: number
  nivel_sarcasmo: number
  nivel_formalidad_general: number
  requiere_contexto_adicional: boolean
}

export interface TraduccionAlternativa {
  traduccion: string
  contexto: string
  confianza: number
}

export interface TraduccionResponse {
  frase_original: string
  traduccion: string | null
  contexto_detectado: ContextoDetectado | null
  componentes: ComponenteToken[]
  analisis: AnalisisCompleto | null
  confianza: number
  alternativas: TraduccionAlternativa[]
  sugerencia_contextos: Array<Record<string, unknown>> | null
}
