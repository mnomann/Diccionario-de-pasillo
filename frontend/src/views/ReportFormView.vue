<template>
  <div class="report-form-container">
    <header class="view-header">
      <h1 class="title">Reportar un Problema</h1>
      <p class="subtitle">
        Ayúdanos a mejorar la plataforma reportando errores, sugiriendo contenido o
        notificando información incorrecta.
      </p>
    </header>

    <div v-if="enviado" class="success-box">
      <div class="success-icon">
        <CheckCircle :size="32" />
      </div>
      <h2 class="success-title">Reporte Enviado</h2>
      <p class="success-text">
        Gracias por tu aporte. Nuestro equipo revisará el reporte a la brevedad.
      </p>
      <button class="btn-secondary" @click="resetForm">Enviar otro reporte</button>
    </div>

    <form v-else class="report-form" @submit.prevent="submitForm">
      <div v-if="store.error" class="form-error">
        <AlertCircle :size="18" />
        <span>{{ store.error }}</span>
      </div>

      <div class="form-group">
        <label class="form-label" for="tipo">Tipo de reporte</label>
        <select id="tipo" v-model="formData.tipo" class="form-select" required>
          <option value="" disabled>Selecciona un tipo</option>
          <option value="error_contenido">Error de contenido</option>
          <option value="palabra_faltante">Palabra faltante</option>
          <option value="error_ortografia">Error ortográfico</option>
          <option value="sugerencia_mejora">Sugerencia de mejora</option>
          <option value="otro">Otro</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label" for="entidad_tipo">Sección relacionada</label>
        <select id="entidad_tipo" v-model="formData.entidad_tipo" class="form-select" required>
          <option value="" disabled>Selecciona una sección</option>
          <option value="palabra">Palabra</option>
          <option value="frase">Frase</option>
          <option value="escenario">Escenario</option>
          <option value="general">General / No aplica</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label" for="descripcion">Descripción</label>
        <textarea
          id="descripcion"
          v-model="formData.descripcion"
          class="form-textarea"
          placeholder="Describe el problema o sugerencia en detalle..."
          rows="5"
          required
        ></textarea>
        <p class="form-help">
          {{ formData.descripcion.length }} caracteres (mínimo 10)
        </p>
      </div>

      <div v-if="!authStore.isAuthenticated" class="form-group">
        <label class="form-label" for="detalle_contacto">
          Correo de contacto
          <span class="label-optional">(opcional)</span>
        </label>
        <input
          id="detalle_contacto"
          v-model="formData.detalle_contacto"
          type="email"
          class="form-input"
          placeholder="email@ejemplo.com"
        />
        <p class="form-help">Si deseas que te contactemos para más información.</p>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-primary" :disabled="store.loading || !formEsValido">
          <Send :size="18" />
          {{ store.loading ? 'Enviando...' : 'Enviar reporte' }}
        </button>
        <button type="button" class="btn-secondary" @click="$router.back()">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Send, CheckCircle, AlertCircle } from 'lucide-vue-next'
import { useReportesStore } from '../store/reportes'
import { useAuthStore } from '../store/auth'
import type { ReporteTipo, ReporteEntidad } from '../types'

const route = useRoute()
const store = useReportesStore()
const authStore = useAuthStore()

const enviado = ref(false)

const formData = reactive({
  tipo: '' as ReporteTipo | '',
  entidad_tipo: '' as ReporteEntidad | '',
  entidad_id: null as number | null,
  descripcion: '',
  detalle_contacto: '',
})

const formEsValido = computed(() => {
  return (
    formData.tipo !== '' &&
    formData.entidad_tipo !== '' &&
    formData.descripcion.trim().length >= 10
  )
})

onMounted(() => {
  const entidadTipo = route.params.entidadTipo as string | undefined
  const entidadId = route.params.entidadId as string | undefined

  const validEntidades: ReporteEntidad[] = ['palabra', 'frase', 'escenario', 'general']
  if (entidadTipo && validEntidades.includes(entidadTipo as ReporteEntidad)) {
    formData.entidad_tipo = entidadTipo as ReporteEntidad
  }

  if (entidadId) {
    const parsed = parseInt(entidadId, 10)
    if (!isNaN(parsed)) {
      formData.entidad_id = parsed
    }
  }
})

async function submitForm() {
  if (!formEsValido.value || store.loading) return

  try {
    await store.createReporte({
      tipo: formData.tipo as ReporteTipo,
      entidad_tipo: formData.entidad_tipo as ReporteEntidad,
      entidad_id: formData.entidad_id,
      descripcion: formData.descripcion.trim(),
      detalle_contacto: formData.detalle_contacto.trim() || null,
    })
    enviado.value = true
  } catch {
    // error se maneja en el store
  }
}

function resetForm() {
  formData.tipo = ''
  formData.entidad_tipo = ''
  formData.entidad_id = null
  formData.descripcion = ''
  formData.detalle_contacto = ''
  store.error = null
  enviado.value = false
}
</script>

<style scoped>
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes successPopIn {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}

.report-form-container {
  max-width: 640px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

/* ===== Formulario ===== */
.report-form {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #991b1b;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.label-optional {
  font-weight: 400;
  color: var(--text-muted);
  text-transform: none;
  letter-spacing: normal;
  font-size: 0.8rem;
}

.form-select,
.form-input,
.form-textarea {
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 8px;
  font-size: 0.95rem;
  color: #111;
  background: #fff;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.form-select:focus,
.form-input:focus,
.form-textarea:focus {
  border-color: var(--brand-dark);
  box-shadow: 0 0 0 3px rgba(45, 51, 34, 0.08);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-help {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* ===== Botones ===== */
.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 0.5rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--brand-accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #3d4f30;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: var(--brand-dark);
  color: var(--brand-dark);
}

/* ===== Éxito ===== */
.success-box {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  animation: successPopIn 0.4s ease both;
}

.success-icon {
  color: #4a7c3f;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
}

.success-text {
  font-size: 1rem;
  color: var(--text-main);
  max-width: 400px;
}

@media (max-width: 768px) {
  .report-form {
    padding: 1.5rem;
  }

  .title {
    font-size: 1.6rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
