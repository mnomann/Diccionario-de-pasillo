import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import { api } from '../services/api'
import type { EscenarioList, EscenarioDetail, PaginatedEscenarios, Paginacion } from '../types'

export const useEscenariosStore = defineStore('escenarios', () => {
  const escenarios = ref<EscenarioList[]>([])
  const paginacion = ref<Paginacion>({
    pagina: 1,
    tamanio: 12,
    total_elementos: 0,
    total_paginas: 0
  })
  const filtros = ref<{ busqueda?: string }>({})
  const escenarioActual = ref<EscenarioDetail | null>(null)
  const loading = ref(false)
  const loadingFrases = ref(false)
  const error = ref<string | null>(null)

  const detallesCache = reactive<Record<number, EscenarioDetail>>({})

  async function fetchEscenarios(params?: { busqueda?: string; pagina?: number; tamanio?: number }) {
    loading.value = true
    error.value = null
    try {
      const mergedParams = { ...filtros.value, ...params }
      const result = await api.get<PaginatedEscenarios>('/escenarios', {
        buscar: mergedParams.busqueda,
        pagina: mergedParams.pagina ?? 1,
        tamanio: mergedParams.tamanio ?? 12,
      })
      escenarios.value = result.data
      paginacion.value = result.paginacion
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al cargar escenarios'
      escenarios.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchEscenario(id: number) {
    loading.value = true
    error.value = null
    try {
      escenarioActual.value = await api.get<EscenarioDetail>(`/escenarios/${id}`)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al cargar el escenario'
      escenarioActual.value = null
    } finally {
      loading.value = false
    }
  }

  async function fetchFrasesPorEscenario(id: number): Promise<EscenarioDetail | null> {
    if (detallesCache[id]) return detallesCache[id]
    loadingFrases.value = true
    try {
      const detalle = await api.get<EscenarioDetail>(`/escenarios/${id}`)
      detallesCache[id] = detalle
      return detalle
    } catch {
      return null
    } finally {
      loadingFrases.value = false
    }
  }

  function setFiltros(nuevosFiltros: { busqueda?: string }) {
    filtros.value = { ...nuevosFiltros }
  }

  function cambiarPagina(pagina: number) {
    fetchEscenarios({ pagina })
  }

  function limpiarCache() {
    for (const key of Object.keys(detallesCache)) {
      delete detallesCache[Number(key)]
    }
  }

  return {
    escenarios,
    paginacion,
    filtros,
    escenarioActual,
    loading,
    loadingFrases,
    error,
    detallesCache,
    fetchEscenarios,
    fetchEscenario,
    fetchFrasesPorEscenario,
    setFiltros,
    cambiarPagina,
    limpiarCache,
  }
})
