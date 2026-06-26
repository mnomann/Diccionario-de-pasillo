import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { TraduccionRequest, TraduccionResponse } from '../types'

export interface TraduccionResultado {
  fraseOriginal: string
  traduccion: string | null
  contextoDetectado: { id: number; nombre: string; confianza: number } | null
  componentes: Array<{ token: string; traduccion: string; tipo: string; nivelFormalidad: number }>
  tono: string
  intencionReal: string
  nivelIronia: number
  nivelSarcasmo: number
  nivelFormalidad: number
  confianza: number
  alternativas: Array<{ traduccion: string; contexto: string; confianza: number }>
  requiereContextoAdicional: boolean
}

export const useTraductorStore = defineStore('traductor', () => {
  const query = ref('')
  const resultado = ref<TraduccionResultado | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Contexto opcional
  const contextoId = ref<number | null>(null)
  const contextoNombre = ref<string | null>(null)
  const contextoPersonalizado = ref<string | null>(null)

  function setContextoId(id: number | null) {
    contextoId.value = id
    contextoNombre.value = null
    contextoPersonalizado.value = null
  }

  function setContextoNombre(nombre: string | null) {
    contextoNombre.value = nombre
    contextoId.value = null
    contextoPersonalizado.value = null
  }

  function setContextoPersonalizado(texto: string | null) {
    contextoPersonalizado.value = texto
    contextoId.value = null
    contextoNombre.value = null
  }

  function limpiarContexto() {
    contextoId.value = null
    contextoNombre.value = null
    contextoPersonalizado.value = null
  }

  async function traducir(texto: string) {
    query.value = texto
    loading.value = true
    error.value = null
    resultado.value = null

    const body: TraduccionRequest = {
      frase: texto,
      contexto_id: contextoId.value,
      contexto_nombre: contextoNombre.value,
      contexto_personalizado: contextoPersonalizado.value,
    }

    try {
      const res = await api.post<TraduccionResponse>('/traducciones/traducir', body)

      resultado.value = {
        fraseOriginal: res.frase_original,
        traduccion: res.traduccion,
        contextoDetectado: res.contexto_detectado,
        componentes: res.componentes.map(c => ({
          token: c.token,
          traduccion: c.traduccion,
          tipo: c.tipo,
          nivelFormalidad: c.nivel_formalidad,
        })),
        tono: res.analisis?.tono || '',
        intencionReal: res.analisis?.intencion_real || '',
        nivelIronia: res.analisis?.nivel_ironia || 0,
        nivelSarcasmo: res.analisis?.nivel_sarcasmo || 0,
        nivelFormalidad: res.analisis?.nivel_formalidad_general || 0,
        confianza: res.confianza,
        alternativas: res.alternativas.map(a => ({
          traduccion: a.traduccion,
          contexto: a.contexto,
          confianza: a.confianza,
        })),
        requiereContextoAdicional: res.analisis?.requiere_contexto_adicional || false,
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al traducir la frase'
    } finally {
      loading.value = false
    }
  }

  return {
    query,
    resultado,
    loading,
    error,
    contextoId,
    contextoNombre,
    contextoPersonalizado,
    setContextoId,
    setContextoNombre,
    setContextoPersonalizado,
    limpiarContexto,
    traducir,
  }
})
