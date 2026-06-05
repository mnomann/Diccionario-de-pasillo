import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { PalabraList, FraseList, PaginatedPalabras, PaginatedFrases } from '../types'

interface TraduccionResultado {
  fraseOriginal: string
  significadoLiteral: string
  usoComun: string
  nota: string
  nivelIronia: 'Bajo' | 'Medio' | 'Alto'
  etiquetas: string[]
}

export const useTraductorStore = defineStore('traductor', () => {
  const query = ref('')
  const resultado = ref<TraduccionResultado | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const usandoMock = ref(true)

  function determinarIronia(nivel: number): 'Bajo' | 'Medio' | 'Alto' {
    if (nivel <= 3) return 'Bajo'
    if (nivel <= 6) return 'Medio'
    return 'Alto'
  }

  async function traducir(texto: string) {
    query.value = texto
    loading.value = true
    error.value = null
    resultado.value = null

    try {
      const res = await api.get<PaginatedPalabras>('/palabras', {
        buscar: texto,
        tamanio: 1,
      })

      if (res.data.length > 0) {
        const p = res.data[0]
        resultado.value = {
          fraseOriginal: p.palabra,
          significadoLiteral: p.traduccion,
          usoComun: `"${p.ejemplo_uso || p.traduccion}"`,
          nota: `Categoría: ${p.categoria}. Nivel de formalidad: ${p.nivel_formalidad}/10.`,
          nivelIronia: determinarIronia(p.nivel_ironia),
          etiquetas: [p.categoria],
        }
        usandoMock.value = false
      } else {
        const fraseRes = await api.get<PaginatedFrases>('/frases', {
          buscar: texto,
          tamanio: 1,
        })
        if (fraseRes.data.length > 0) {
          const f = fraseRes.data[0]
          resultado.value = {
            fraseOriginal: f.frase_original,
            significadoLiteral: f.traduccion,
            usoComun: f.escenario?.nombre || '',
            nota: `Tono: ${f.tono || 'neutro'}. Formalidad: ${f.nivel_formalidad}/10.`,
            nivelIronia: determinarIronia(f.nivel_ironia),
            etiquetas: [f.tono || 'neutro'].filter(Boolean),
          }
          usandoMock.value = false
        }
      }
    } catch {
      // No hay datos mock para el traductor
    } finally {
      loading.value = false
    }
  }

  return {
    query,
    resultado,
    loading,
    error,
    usandoMock,
    traducir,
  }
})
