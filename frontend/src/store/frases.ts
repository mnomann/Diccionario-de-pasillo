import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { FraseList, PaginatedFrases } from '../types'

interface FraseDisplay {
  id: number
  word: string
  meaning: string
  example?: string
  tags?: string[]
  type: 'normal' | 'wide'
}

const MOCK_FRASES: FraseDisplay[] = [
  { id: 1, word: 'Al tiro', meaning: 'Inmediatamente, enseguida.', type: 'normal' },
  { id: 2, word: '¿Cachai?', meaning: '¿Entiendes? o ¿Comprendes?', example: '"Es complicado de explicar, ¿cachai?"', tags: ['Expresión', 'Muy Común'], type: 'wide' },
  { id: 3, word: 'Fome', meaning: 'Aburrido, sin gracia.', tags: ['Adjetivo'], type: 'normal' },
  { id: 4, word: 'Bacán', meaning: 'Excelente, genial.', tags: ['Adjetivo'], type: 'normal' },
  { id: 5, word: 'Cuático', meaning: 'Exagerado, intenso, o sorprendente.', tags: ['Expresión'], type: 'normal' },
  { id: 6, word: 'Pololo / Polola', meaning: 'Novio, novia.', type: 'normal' },
  { id: 7, word: 'Luca', meaning: 'Mil pesos chilenos.', tags: ['Dinero'], type: 'normal' },
  { id: 8, word: 'Micro', meaning: 'Autobús de transporte público.', type: 'normal' },
]

export const useFrasesStore = defineStore('frases', () => {
  const frases = ref<FraseDisplay[]>(MOCK_FRASES)
  const loading = ref(false)
  const usandoMock = ref(true)

  function mapFraseToDisplay(f: FraseList): FraseDisplay {
    return {
      id: f.id,
      word: f.frase_original,
      meaning: f.traduccion,
      tags: f.tono ? [f.tono] : undefined,
      type: 'normal',
    }
  }

  async function fetchFrases(params?: { escenario_id?: number; buscar?: string }) {
    loading.value = true
    try {
      const result = await api.get<PaginatedFrases>('/frases', {
        escenario_id: params?.escenario_id,
        buscar: params?.buscar,
        tamanio: 100,
      })
      const mapped = result.data.map(mapFraseToDisplay)
      if (mapped.length > 0) {
        mapped[0] = { ...mapped[0], type: 'wide' }
      }
      frases.value = mapped
      usandoMock.value = false
    } catch {
      frases.value = MOCK_FRASES
      usandoMock.value = true
    } finally {
      loading.value = false
    }
  }

  return {
    frases,
    loading,
    usandoMock,
    fetchFrases,
  }
})
