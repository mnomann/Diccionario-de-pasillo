import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { EscenarioList, EscenarioDetail, PaginatedEscenarios } from '../types'

export const useEscenariosStore = defineStore('escenarios', () => {
  const escenarios = ref<EscenarioList[]>([])
  const escenarioActual = ref<EscenarioDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const usandoMock = ref(true)

  async function fetchEscenarios(params?: { buscar?: string }) {
    loading.value = true
    error.value = null
    try {
      const result = await api.get<PaginatedEscenarios>('/escenarios', {
        buscar: params?.buscar,
        tamanio: 100,
      })
      escenarios.value = result.data
      usandoMock.value = false
    } catch {
      usandoMock.value = true
    } finally {
      loading.value = false
    }
  }

  async function fetchEscenario(id: number) {
    loading.value = true
    error.value = null
    try {
      escenarioActual.value = await api.get<EscenarioDetail>(`/escenarios/${id}`)
      usandoMock.value = false
    } catch {
      escenarioActual.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    escenarios,
    escenarioActual,
    loading,
    error,
    usandoMock,
    fetchEscenarios,
    fetchEscenario,
  }
})
