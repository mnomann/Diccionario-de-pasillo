<template>
  <div class="admin-reportes-container">
    <header class="view-header">
      <h1 class="title">Panel de Reportes</h1>
      <p class="subtitle">
        Gestiona los reportes enviados por los usuarios. Cambia el estado y
        añade comentarios de administrador.
      </p>
    </header>

    <!-- Filtros -->
    <div class="filters-bar">
      <div class="filter-group">
        <label class="filter-label" for="filtro-estado">Estado</label>
        <select id="filtro-estado" v-model="filtroEstado" class="filter-select" @change="onFiltrosChange">
          <option value="">Todos</option>
          <option value="pendiente">Pendiente</option>
          <option value="en_revision">En revisión</option>
          <option value="resuelto">Resuelto</option>
          <option value="rechazado">Rechazado</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label" for="filtro-tipo">Tipo</label>
        <select id="filtro-tipo" v-model="filtroTipo" class="filter-select" @change="onFiltrosChange">
          <option value="">Todos</option>
          <option value="error_contenido">Error de contenido</option>
          <option value="palabra_faltante">Palabra faltante</option>
          <option value="error_ortografia">Error ortográfico</option>
          <option value="sugerencia_mejora">Sugerencia de mejora</option>
          <option value="otro">Otro</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label" for="filtro-entidad">Sección</label>
        <select id="filtro-entidad" v-model="filtroEntidad" class="filter-select" @change="onFiltrosChange">
          <option value="">Todas</option>
          <option value="palabra">Palabra</option>
          <option value="frase">Frase</option>
          <option value="escenario">Escenario</option>
          <option value="general">General</option>
        </select>
      </div>
    </div>

    <!-- No autorizado -->
    <div v-if="!authStore.isAuthenticated" class="error-state">
      <p>Debes iniciar sesión como administrador para acceder a esta sección.</p>
      <button class="btn-retry" @click="authModalOpen = true">Iniciar Sesión</button>
    </div>

    <!-- Loading -->
    <div v-else-if="store.loading && store.reportes.length === 0" class="loading-state">
      <div class="loading-spinner" />
      <p>Cargando reportes...</p>
    </div>

    <!-- Error -->
    <div v-else-if="store.error" class="error-state">
      <p>{{ store.error }}</p>
      <button class="btn-retry" @click="store.fetchReportes()">Reintentar</button>
    </div>

    <!-- Tabla -->
    <template v-else-if="store.reportes.length > 0">
      <div class="table-wrapper">
        <table class="reportes-table">
          <thead>
            <tr>
              <th class="col-id">ID</th>
              <th class="col-tipo">Tipo</th>
              <th class="col-entidad">Sección</th>
              <th class="col-descripcion">Descripción</th>
              <th class="col-estado">Estado</th>
              <th class="col-fecha">Fecha</th>
              <th class="col-accion"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="reporte in store.reportes"
              :key="reporte.id"
              :class="['reporte-row', { 'row--expanded': expandedId === reporte.id }]"
              @click="toggleExpand(reporte.id)"
            >
              <td class="col-id">{{ reporte.id }}</td>
              <td class="col-tipo">{{ tipoLabel(reporte.tipo) }}</td>
              <td class="col-entidad">{{ entidadLabel(reporte.entidad_tipo) }}</td>
              <td class="col-descripcion">{{ truncar(reporte.descripcion, 60) }}</td>
              <td class="col-estado">
                <span :class="['estado-badge', `estado--${reporte.estado}`]">
                  {{ estadoLabel(reporte.estado) }}
                </span>
              </td>
              <td class="col-fecha">{{ formatearFecha(reporte.fecha_creacion) }}</td>
              <td class="col-accion">
                <ChevronDown :size="16" :class="['chevron-icon', { rotated: expandedId === reporte.id }]" />
              </td>
            </tr>

            <!-- Fila expandida -->
            <tr v-if="expandedId" class="expand-row">
              <td colspan="7">
                <transition name="expand-fade">
                  <div v-if="expandedId" class="expand-content">
                    <div class="expand-grid">
                      <div class="expand-section">
                        <h4 class="expand-section-title">Detalle del Reporte</h4>
                        <div class="detail-row">
                          <span class="detail-label">Tipo:</span>
                          <span>{{ tipoLabel(reporteExpandido?.tipo ?? '') }}</span>
                        </div>
                        <div class="detail-row">
                          <span class="detail-label">Sección:</span>
                          <span>{{ entidadLabel(reporteExpandido?.entidad_tipo ?? '') }}</span>
                        </div>
                        <div class="detail-row" v-if="reporteExpandido?.entidad_id">
                          <span class="detail-label">ID de contenido:</span>
                          <span>{{ reporteExpandido.entidad_id }}</span>
                        </div>
                        <div class="detail-row">
                          <span class="detail-label">Descripción completa:</span>
                        </div>
                        <p class="detail-descripcion">{{ reporteExpandido?.descripcion }}</p>
                        <div class="detail-row" v-if="reporteExpandido?.detalle_contacto">
                          <span class="detail-label">Email de contacto:</span>
                          <span>{{ reporteExpandido.detalle_contacto }}</span>
                        </div>
                        <div class="detail-row" v-if="reporteExpandido?.usuario">
                          <span class="detail-label">Usuario:</span>
                          <span>{{ reporteExpandido.usuario.nombre }} ({{ reporteExpandido.usuario.email }})</span>
                        </div>
                        <div class="detail-row">
                          <span class="detail-label">Fecha de creación:</span>
                          <span>{{ formatearFecha(reporteExpandido?.fecha_creacion ?? '') }}</span>
                        </div>
                        <div class="detail-row" v-if="reporteExpandido?.fecha_actualizacion">
                          <span class="detail-label">Última actualización:</span>
                          <span>{{ formatearFecha(reporteExpandido.fecha_actualizacion) }}</span>
                        </div>
                        <div class="detail-row" v-if="reporteExpandido?.comentario_admin">
                          <span class="detail-label">Comentario admin actual:</span>
                          <p class="detail-comentario">{{ reporteExpandido.comentario_admin }}</p>
                        </div>
                      </div>

                      <div class="expand-section">
                        <h4 class="expand-section-title">Gestión del Reporte</h4>

                        <div class="form-group">
                          <label class="field-label" for="edit-estado">Estado</label>
                          <select id="edit-estado" v-model="editEstado" class="field-select">
                            <option value="pendiente">Pendiente</option>
                            <option value="en_revision">En revisión</option>
                            <option value="resuelto">Resuelto</option>
                            <option value="rechazado">Rechazado</option>
                          </select>
                        </div>

                        <div class="form-group">
                          <label class="field-label" for="edit-comentario">Comentario del administrador</label>
                          <textarea
                            id="edit-comentario"
                            v-model="editComentario"
                            class="field-textarea"
                            placeholder="Añade una nota sobre la resolución..."
                            rows="3"
                          ></textarea>
                        </div>

                        <button
                          class="btn-save"
                          :disabled="guardando"
                          @click="guardarCambios"
                        >
                          <Save :size="16" />
                          {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
                        </button>

                        <p v-if="editError" class="edit-error">{{ editError }}</p>
                        <p v-if="editExito" class="edit-exito">Cambios guardados correctamente.</p>
                      </div>
                    </div>
                  </div>
                </transition>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      <div v-if="store.paginacion.total_paginas > 1" class="pagination-bar">
        <button
          class="page-btn"
          :disabled="store.paginacion.pagina <= 1"
          @click="cambiarPagina(store.paginacion.pagina - 1)"
        >
          <ChevronLeft :size="16" />
          Anterior
        </button>

        <div class="page-numbers">
          <button
            v-for="p in paginasVisibles"
            :key="p"
            :class="['page-num', { active: p === store.paginacion.pagina }]"
            @click="cambiarPagina(p)"
          >
            {{ p }}
          </button>
        </div>

        <button
          class="page-btn"
          :disabled="store.paginacion.pagina >= store.paginacion.total_paginas"
          @click="cambiarPagina(store.paginacion.pagina + 1)"
        >
          Siguiente
          <ChevronRight :size="16" />
        </button>
      </div>
    </template>

    <!-- Vacío -->
    <div v-else class="empty-state">
      <p>No se encontraron reportes con los filtros seleccionados.</p>
    </div>

    <AuthModal :is-open="authModalOpen" @close="authModalOpen = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ChevronDown, ChevronLeft, ChevronRight, Save } from 'lucide-vue-next'
import { useReportesStore } from '../store/reportes'
import { useAuthStore } from '../store/auth'
import type { ReporteDetail, ReporteEstado } from '../types'

import AuthModal from '../components/auth/AuthModal.vue'

const store = useReportesStore()
const authStore = useAuthStore()

const authModalOpen = ref(false)

const filtroEstado = ref('')
const filtroTipo = ref('')
const filtroEntidad = ref('')

const expandedId = ref<number | null>(null)
const editEstado = ref<string>('pendiente')
const editComentario = ref('')
const guardando = ref(false)
const editError = ref('')
const editExito = ref(false)

const reporteExpandido = computed<ReporteDetail | null>(() => {
  if (expandedId.value === null) return null
  return store.reportes.find((r) => r.id === expandedId.value) ?? null
})

const paginasVisibles = computed(() => {
  const total = store.paginacion.total_paginas
  const actual = store.paginacion.pagina
  const rango: number[] = []
  const inicio = Math.max(1, actual - 2)
  const fin = Math.min(total, actual + 2)
  for (let i = inicio; i <= fin; i++) {
    rango.push(i)
  }
  return rango
})

onMounted(() => {
  if (!authStore.isAuthenticated) return
  store.fetchReportes()
})

function onFiltrosChange() {
  store.setFiltros({
    estado: filtroEstado.value || undefined,
    tipo: filtroTipo.value || undefined,
    entidad_tipo: filtroEntidad.value || undefined,
  })
}

function cambiarPagina(pagina: number) {
  store.irPagina(pagina)
  expandedId.value = null
}

function toggleExpand(id: number) {
  if (expandedId.value === id) {
    expandedId.value = null
    return
  }
  expandedId.value = id
  const r = store.reportes.find((r) => r.id === id)
  if (r) {
    editEstado.value = r.estado
    editComentario.value = r.comentario_admin ?? ''
  }
  editError.value = ''
  editExito.value = false
}

async function guardarCambios() {
  if (!expandedId.value || guardando.value) return
  guardando.value = true
  editError.value = ''
  editExito.value = false
  try {
    await store.updateReporte(expandedId.value, {
      estado: editEstado.value as ReporteEstado,
      comentario_admin: editComentario.value.trim() || null,
    })
    editExito.value = true
  } catch {
    editError.value = 'Error al guardar los cambios. Intenta nuevamente.'
  } finally {
    guardando.value = false
  }
}

function tipoLabel(tipo: string): string {
  const mapa: Record<string, string> = {
    error_contenido: 'Error de contenido',
    palabra_faltante: 'Palabra faltante',
    error_ortografia: 'Error ortográfico',
    sugerencia_mejora: 'Sugerencia de mejora',
    otro: 'Otro',
  }
  return mapa[tipo] || tipo
}

function entidadLabel(entidad: string): string {
  const mapa: Record<string, string> = {
    palabra: 'Palabra',
    frase: 'Frase',
    escenario: 'Escenario',
    general: 'General',
  }
  return mapa[entidad] || entidad
}

function estadoLabel(estado: string): string {
  const mapa: Record<string, string> = {
    pendiente: 'Pendiente',
    en_revision: 'En revisión',
    resuelto: 'Resuelto',
    rechazado: 'Rechazado',
  }
  return mapa[estado] || estado
}

function truncar(texto: string, max: number): string {
  if (texto.length <= max) return texto
  return texto.slice(0, max) + '...'
}

function formatearFecha(fecha: string): string {
  if (!fecha) return '-'
  try {
    return new Date(fecha).toLocaleDateString('es-CL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return fecha
  }
}
</script>

<style scoped>
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.admin-reportes-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 3rem;
  animation: viewFadeIn 0.5s ease both;
}

.view-header {
  border-left: 6px solid var(--brand-accent);
  padding-left: 1.5rem;
}

.title {
  font-size: 2.2rem;
  font-weight: 900;
  color: #111;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: var(--text-main);
  line-height: 1.5;
}

/* ===== Filtros ===== */
.filters-bar {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 180px;
}

.filter-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.filter-select {
  padding: 0.5rem 0.7rem;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 6px;
  font-size: 0.9rem;
  color: #111;
  background: #fff;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.filter-select:focus {
  border-color: var(--brand-dark);
  box-shadow: 0 0 0 3px rgba(45, 51, 34, 0.08);
}

/* ===== Estados ===== */
.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  font-size: 1rem;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color, #e2e5dc);
  border-top-color: var(--brand-dark);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 1rem;
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: var(--brand-dark);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s;
}

.btn-retry:hover {
  opacity: 0.85;
}

/* ===== Tabla ===== */
.table-wrapper {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  overflow: hidden;
}

.reportes-table {
  width: 100%;
  border-collapse: collapse;
}

.reportes-table thead {
  background: #f4f6ed;
}

.reportes-table th {
  text-align: left;
  padding: 0.9rem 1rem;
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
}

.col-id { width: 50px; }
.col-tipo { width: 160px; }
.col-entidad { width: 100px; }
.col-descripcion { min-width: 200px; }
.col-estado { width: 120px; }
.col-fecha { width: 160px; }
.col-accion { width: 40px; }

.reporte-row {
  cursor: pointer;
  transition: background-color 0.15s;
}

.reporte-row:hover {
  background: #fafbf8;
}

.reporte-row td {
  padding: 0.85rem 1rem;
  font-size: 0.9rem;
  color: #111;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
  vertical-align: middle;
}

.reporte-row:last-child td {
  border-bottom: none;
}

.row--expanded {
  background: #f7f9f4;
}

.row--expanded + .expand-row td {
  background: #f7f9f4;
  padding: 0;
}

.chevron-icon {
  color: var(--text-muted);
  transition: transform 0.25s ease;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

/* ===== Badge Estado ===== */
.estado-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.estado--pendiente {
  background: #fef3c7;
  color: #92400e;
}

.estado--en_revision {
  background: #e0f2fe;
  color: #0369a1;
}

.estado--resuelto {
  background: #d1fae5;
  color: #065f46;
}

.estado--rechazado {
  background: #fce4ec;
  color: #c62828;
}

/* ===== Fila expandida ===== */
.expand-row td {
  padding: 0 !important;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
}

.expand-content {
  padding: 1.5rem 2rem;
}

.expand-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.expand-section-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
}

.detail-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-label {
  font-weight: 700;
  color: var(--text-muted);
  flex-shrink: 0;
  min-width: 140px;
}

.detail-descripcion {
  font-size: 0.9rem;
  color: #111;
  line-height: 1.5;
  margin: 0.25rem 0 0.75rem 0;
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 6px;
  padding: 0.75rem;
}

.detail-comentario {
  font-size: 0.9rem;
  color: #333;
  font-style: italic;
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  margin: 0.25rem 0 0;
}

/* ===== Formulario de gestión ===== */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.field-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.field-select,
.field-textarea {
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 6px;
  font-size: 0.9rem;
  color: #111;
  background: #fff;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.field-select:focus,
.field-textarea:focus {
  border-color: var(--brand-dark);
  box-shadow: 0 0 0 3px rgba(45, 51, 34, 0.08);
}

.field-textarea {
  resize: vertical;
  min-height: 70px;
}

.btn-save {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: var(--brand-accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: #3d4f30;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.edit-error {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #c62828;
  font-weight: 500;
}

.edit-exito {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #065f46;
  font-weight: 600;
}

/* ===== Paginación ===== */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem 0;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 1rem;
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--brand-dark);
  color: var(--brand-dark);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-num {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-main);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.page-num:hover {
  border-color: var(--border-color, #e2e5dc);
}

.page-num.active {
  background: var(--brand-accent);
  color: #fff;
  border-color: var(--brand-accent);
}

/* ===== Transiciones ===== */
.expand-fade-enter-active,
.expand-fade-leave-active {
  transition: opacity 0.2s ease;
}

.expand-fade-enter-from,
.expand-fade-leave-to {
  opacity: 0;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .title {
    font-size: 1.6rem;
  }

  .filters-bar {
    flex-direction: column;
  }

  .filter-group {
    min-width: unset;
  }

  .expand-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .reportes-table {
    min-width: 700px;
  }
}
</style>
