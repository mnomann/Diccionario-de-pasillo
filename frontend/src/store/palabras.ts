import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../services/api'
import type { PalabraList, PalabraDetail, PaginatedPalabras } from '../types'

const MOCK_PALABRAS: PalabraList[] = [
  { id: 1, palabra: 'Cachai', traduccion: '¿Entiendes? / ¿Comprendes?', categoria: 'muletilla', nivel_formalidad: 1, nivel_ironia: 1, ejemplo_uso: '"Es complicado el tema, ¿cachai?"', fecha_creacion: '' },
  { id: 2, palabra: 'Fome', traduccion: 'Aburrido, sin gracia, que no tiene sentido del humor.', categoria: 'modismo', nivel_formalidad: 2, nivel_ironia: 2, ejemplo_uso: '"La película estaba súper fome, me quedé dormido."', fecha_creacion: '' },
  { id: 3, palabra: 'Pololo/a', traduccion: 'Novio o novia. Pareja formal pero antes del compromiso de matrimonio.', categoria: 'modismo', nivel_formalidad: 2, nivel_ironia: 0, ejemplo_uso: '"Voy al cine con mi polola más rato."', fecha_creacion: '' },
  { id: 4, palabra: 'Pega', traduccion: 'Trabajo, empleo u ocupación remunerada.', categoria: 'jerga', nivel_formalidad: 1, nivel_ironia: 0, ejemplo_uso: '"Tengo mucha pega hoy, no creo que pueda salir."', fecha_creacion: '' },
  { id: 5, palabra: 'Al tiro', traduccion: 'Inmediatamente, de inmediato, en seguida.', categoria: 'modismo', nivel_formalidad: 2, nivel_ironia: 0, ejemplo_uso: '"Voy para allá al tiro, dame 5 minutos."', fecha_creacion: '' },
  { id: 6, palabra: 'Bacán', traduccion: 'Excelente, genial, muy bueno. Algo positivo.', categoria: 'modismo', nivel_formalidad: 2, nivel_ironia: 1, ejemplo_uso: '"¡Qué bacán tu chaqueta nueva!"', fecha_creacion: '' },
]

export const usePalabrasStore = defineStore('palabras', () => {
  const palabras = ref<PalabraList[]>(MOCK_PALABRAS)
  const palabraActual = ref<PalabraDetail | null>(null)
  const categorias = ref<string[]>(['TODO', 'Modismos', 'Muletillas', 'Jerga', 'Abreviaciones'])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const usandoMock = ref(true)

  const palabrasFiltradas = computed(() => {
    return palabras.value
  })

  async function fetchPalabras(params?: { categoria?: string; buscar?: string }) {
    loading.value = true
    error.value = null
    try {
      const result = await api.get<PaginatedPalabras>('/palabras', {
        categoria: params?.categoria,
        buscar: params?.buscar,
        tamanio: 100,
      })
      palabras.value = result.data
      usandoMock.value = false
    } catch {
      let filtradas = MOCK_PALABRAS
      if (params?.categoria) {
        filtradas = filtradas.filter(p => p.categoria === params.categoria)
      }
      if (params?.buscar) {
        const q = params.buscar.toLowerCase()
        filtradas = filtradas.filter(p =>
          p.palabra.toLowerCase().includes(q) ||
          p.traduccion.toLowerCase().includes(q)
        )
      }
      palabras.value = filtradas
      usandoMock.value = true
    } finally {
      loading.value = false
    }
  }

  async function fetchPalabra(id: number) {
    loading.value = true
    error.value = null
    try {
      palabraActual.value = await api.get<PalabraDetail>(`/palabras/${id}`)
      usandoMock.value = false
    } catch {
      palabraActual.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    palabras,
    palabraActual,
    categorias,
    loading,
    error,
    usandoMock,
    palabrasFiltradas,
    fetchPalabras,
    fetchPalabra,
  }
})
