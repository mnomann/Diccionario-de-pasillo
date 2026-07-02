import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '../services/api'
import type { ReporteDetail, ReporteCreate, ReporteUpdate, ReporteResponse, PaginatedReportes, Paginacion } from '../types'

export const useReportesStore = defineStore('reportes', () => {
  const reportes = ref<ReporteDetail[]>([])
  const reporteActual = ref<ReporteDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const paginacion = ref<Paginacion>({
    pagina: 1,
    tamanio: 10,
    total_elementos: 0,
    total_paginas: 0,
  })

  const filtros = ref<{
    estado?: string
    tipo?: string
    entidad_tipo?: string
  }>({})

  async function fetchReportes(overrideFiltros?: {
    estado?: string
    tipo?: string
    entidad_tipo?: string
    pagina?: number
  }) {
    loading.value = true
    error.value = null
    try {
      const params: Record<string, string | number | boolean | undefined | null> = {
        estado: overrideFiltros?.estado ?? filtros.value.estado,
        tipo: overrideFiltros?.tipo ?? filtros.value.tipo,
        entidad_tipo: overrideFiltros?.entidad_tipo ?? filtros.value.entidad_tipo,
        pagina: overrideFiltros?.pagina ?? paginacion.value.pagina,
        tamanio: paginacion.value.tamanio,
      }
      const result = await api.get<PaginatedReportes>('/reportes', params)
      reportes.value = result.data
      paginacion.value = result.paginacion
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al cargar reportes'
    } finally {
      loading.value = false
    }
  }

  async function fetchReporte(id: number) {
    loading.value = true
    error.value = null
    try {
      reporteActual.value = await api.get<ReporteDetail>(`/reportes/${id}`)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al cargar reporte'
    } finally {
      loading.value = false
    }
  }

  async function createReporte(data: ReporteCreate) {
    loading.value = true
    error.value = null
    try {
      await api.post<ReporteResponse>('/reportes', data)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al enviar reporte'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateReporte(id: number, data: ReporteUpdate) {
    loading.value = true
    error.value = null
    try {
      const actualizado = await api.patch<ReporteDetail>(`/reportes/${id}`, data)
      const idx = reportes.value.findIndex((r) => r.id === id)
      if (idx !== -1) {
        reportes.value[idx] = actualizado
      }
      if (reporteActual.value?.id === id) {
        reporteActual.value = actualizado
      }
      return actualizado
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al actualizar reporte'
      throw e
    } finally {
      loading.value = false
    }
  }

  function setFiltros(nuevosFiltros: { estado?: string; tipo?: string; entidad_tipo?: string }) {
    filtros.value = { ...nuevosFiltros }
    paginacion.value.pagina = 1
    fetchReportes()
  }

  function irPagina(pagina: number) {
    paginacion.value.pagina = pagina
    fetchReportes()
  }

  return {
    reportes,
    reporteActual,
    loading,
    error,
    paginacion,
    filtros,
    fetchReportes,
    fetchReporte,
    createReporte,
    updateReporte,
    setFiltros,
    irPagina,
  }
})
