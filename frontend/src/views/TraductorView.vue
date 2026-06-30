<template>
  <div class="traductor-container">
    <header class="view-header">
      <h2 class="title">DESCIFRADOR DE CHILE</h2>
      <p class="subtitle">Introduce una frase para entender su contexto real.</p>
    </header>

    <!-- Busqueda -->
    <div class="search-bar-container">
      <div class="search-input-wrapper">
        <input
          class="search-input"
          type="text"
          v-model="query"
          placeholder="Ej: Estoy pato"
          @keyup.enter="buscar"
        />
      </div>
      <button class="translate-btn" @click="buscar" :disabled="store.loading">
        <Languages :size="18" />
        {{ store.loading ? 'TRADUCIENDO...' : 'TRADUCIR' }}
      </button>
    </div>

    <!-- Contexto opcional -->
    <div class="context-section">
      <button class="context-toggle" @click="showContext = !showContext">
        <MessageSquarePlus :size="16" />
        {{ showContext ? 'OCULTAR CONTEXTO' : 'AGREGAR CONTEXTO' }}
      </button>

      <transition name="slide">
        <div v-if="showContext" class="context-panel">
          <div class="context-tabs">
            <button
              :class="['tab', { active: contextMode === 'predef' }]"
              @click="contextMode = 'predef'; store.setContextoPersonalizado(null)"
            >
              Contexto predefinido
            </button>
            <button
              :class="['tab', { active: contextMode === 'custom' }]"
              @click="contextMode = 'custom'; store.setContextoId(null); store.setContextoNombre(null)"
            >
              Escribe tu contexto
            </button>
          </div>

          <div v-if="contextMode === 'predef'" class="context-predef">
            <p class="predef-hint">Elige un contexto social para mejorar la precisión de la traducción:</p>
            <div class="escenario-grid">
              <button
                v-for="esc in escenarios"
                :key="esc.id"
                :class="['escenario-card', { selected: selectedEscenario?.id === esc.id }]"
                @click="selectedEscenario = esc; onEscenarioChange()"
              >
                <div class="esc-icon-wrapper">
                  <component :is="iconoComponent(esc.icono, esc.nombre)" :size="22" class="esc-icon" />
                </div>
                <div class="esc-body">
                  <span class="esc-nombre">{{ esc.nombre }}</span>
                  <span class="esc-desc">{{ esc.descripcion || 'Sin descripción' }}</span>
                </div>
                <span v-if="selectedEscenario?.id === esc.id" class="esc-check">
                  <Check :size="16" />
                </span>
              </button>
            </div>
          </div>

          <div v-if="contextMode === 'custom'" class="context-custom">
            <textarea
              v-model="customContextText"
              @input="store.setContextoPersonalizado(customContextText)"
              class="context-textarea"
              placeholder="Describe la situacion en que se usa la frase..."
              rows="3"
            ></textarea>
          </div>
        </div>
      </transition>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner" />
      <p>Analizando frase con IA...</p>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="error-state">
      <p>{{ store.error }}</p>
    </div>

    <!-- Resultados -->
    <div v-if="store.resultado" class="results-layout">
      <transition name="result-enter">
        <div class="results-inner">
          <div class="main-card-white">
            <span class="card-label">FRASE ORIGINAL</span>
            <h1 class="phrase-text">"{{ store.resultado.fraseOriginal }}"</h1>

            <!-- Traduccion -->
            <div class="inner-box">
              <div class="box-header">
                <BookOpen :size="16" />
                <h3>SIGNIFICADO LITERAL</h3>
              </div>
              <p>{{ store.resultado.traduccion }}</p>
            </div>

            <!-- Componentes / Modismos detectados -->
            <div v-if="store.resultado.componentes.length > 0" class="inner-box">
              <div class="box-header">
                <Tags :size="16" />
                <h3>MODISMOS DETECTADOS</h3>
              </div>
              <div class="componentes-list">
                <div v-for="c in store.resultado.componentes" :key="c.token" class="componente-item">
                  <span class="comp-token">{{ c.token }}</span>
                  <span class="comp-arrow">&rarr;</span>
                  <span class="comp-trad">{{ c.traduccion || '?' }}</span>
                  <span class="comp-tipo">{{ c.tipo }}</span>
                </div>
              </div>
            </div>

            <!-- Intencion real -->
            <div class="inner-box">
              <div class="box-header">
                <MessageSquare :size="16" />
                <h3>INTENCION REAL</h3>
              </div>
              <p>{{ store.resultado.intencionReal }}</p>

              <div v-if="store.resultado.requiereContextoAdicional" class="dark-note">
                <Info :size="18" class="note-icon" />
                <p>Esta frase necesita mas contexto para ser interpretada correctamente.</p>
              </div>
            </div>

            <!-- Alternativas -->
            <div v-if="store.resultado.alternativas.length > 0" class="inner-box">
              <div class="box-header">
                <GitCompare :size="16" />
                <h3>TRADUCCIONES ALTERNATIVAS</h3>
              </div>
              <div v-for="(alt, i) in store.resultado.alternativas" :key="i" class="alternativa-item">
                <p class="alt-trad">{{ alt.traduccion }}</p>
                <p class="alt-ctx">{{ alt.contexto }} (confianza: {{ (alt.confianza * 100).toFixed(0) }}%)</p>
              </div>
            </div>
          </div>

          <aside class="side-info-column">
            <!-- Contexto detectado -->
            <div v-if="store.resultado.contextoDetectado" class="small-card">
              <h3 class="card-title">CONTEXTO DETECTADO</h3>
              <p class="context-name">{{ store.resultado.contextoDetectado.nombre }}</p>
              <p class="context-confianza">Confianza: {{ (store.resultado.contextoDetectado.confianza * 100).toFixed(0) }}%</p>
            </div>

            <!-- Nivel de ironia -->
            <div class="small-card">
              <h3 class="card-title">NIVEL DE IRONIA</h3>
              <div class="irony-row">
                <span>{{ nivelIroniaTexto }}</span>
                <div class="irony-bars">
                  <div class="bar" :class="ironiaClase(1)"></div>
                  <div class="bar" :class="ironiaClase(2)"></div>
                  <div class="bar" :class="ironiaClase(3)"></div>
                </div>
              </div>
            </div>

            <!-- Nivel de sarcasmo -->
            <div class="small-card">
              <h3 class="card-title">NIVEL DE SARCASMO</h3>
              <div class="irony-row">
                <span>{{ nivelSarcasmoTexto }}</span>
                <div class="irony-bars">
                  <div class="bar" :class="sarcasmoClase(1)"></div>
                  <div class="bar" :class="sarcasmoClase(2)"></div>
                  <div class="bar" :class="sarcasmoClase(3)"></div>
                </div>
              </div>
            </div>

            <!-- Nivel de formalidad -->
            <div class="small-card">
              <h3 class="card-title">FORMALIDAD</h3>
              <div class="irony-row">
                <span>{{ formalidadTexto }}</span>
                <div class="irony-bars">
                  <div class="bar" :class="formalidadClase(1)"></div>
                  <div class="bar" :class="formalidadClase(2)"></div>
                  <div class="bar" :class="formalidadClase(3)"></div>
                  <div class="bar" :class="formalidadClase(4)"></div>
                  <div class="bar" :class="formalidadClase(5)"></div>
                </div>
              </div>
            </div>

            <!-- Confianza -->
            <div class="small-card">
              <h3 class="card-title">CONFIANZA</h3>
              <p class="confianza-valor">{{ (store.resultado.confianza * 100).toFixed(0) }}%</p>
            </div>

            <router-link to="/escenarios" class="small-card link-card" style="text-decoration: none;">
              <div class="link-content">
                <h3 class="card-title">APRENDER ESCENARIOS SOCIALES</h3>
                <p>Ver ejemplos de como usar esta frase en la vida real.</p>
              </div>
              <ArrowRight :size="20" />
            </router-link>
          </aside>
        </div>
      </transition>
    </div>

    <!-- Sin resultados -->
    <div v-else-if="store.query && !store.loading && !store.error" class="no-results">
      <p>No se pudo traducir "{{ store.query }}".</p>
    </div>

    <!-- Estado inicial -->
    <div v-else-if="!store.loading && !store.error" class="empty-state">
      <p>Introduce una frase chilena para obtener su significado y contexto.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  Languages, BookOpen, MessageSquare, Info, ArrowRight, Tags, GitCompare,
  MessageSquarePlus, Check, Briefcase, HeartPulse, Users, Building2,
  Home, Sparkles, Speech, MessageCircle, Camera, Star, Heart, Sun,
} from 'lucide-vue-next'
import type { Component } from 'vue'
import { useTraductorStore } from '../store/traductor'
import { useEscenariosStore } from '../store/escenarios'
import type { EscenarioList } from '../types'

const store = useTraductorStore()
const escenariosStore = useEscenariosStore()

const query = ref('')
const showContext = ref(false)
const contextMode = ref<'predef' | 'custom'>('predef')
const selectedEscenario = ref<EscenarioList | null>(null)
const customContextText = ref('')
const escenarios = computed(() => escenariosStore.escenarios)

onMounted(() => {
  if (escenarios.value.length === 0) {
    escenariosStore.fetchEscenarios()
  }
})

function onEscenarioChange() {
  if (selectedEscenario.value) {
    store.setContextoNombre(selectedEscenario.value.nombre)
  } else {
    store.setContextoId(null)
    store.setContextoNombre(null)
  }
}

const iconoComponentMap: Record<string, Component> = {
  'briefcase': Briefcase,
  'heart-pulse': HeartPulse,
  'people': Users,
  'building': Building2,
  'house': Home,
  'party-popper': Sparkles,
}

const defaultEscenaIcons: Component[] = [
  MessageSquare, Speech, MessageCircle, Camera,
  BookOpen, Star, Heart, Sun,
]

function iconoComponent(icono: string | null, nombre: string): Component {
  if (icono && iconoComponentMap[icono]) return iconoComponentMap[icono]
  const idx = nombre.length % defaultEscenaIcons.length
  return defaultEscenaIcons[idx]
}

function buscar() {
  if (query.value.trim()) {
    store.traducir(query.value.trim())
  }
}

const nivelIroniaTexto = computed(() => {
  if (!store.resultado) return ''
  const n = store.resultado.nivelIronia
  if (n <= 3) return 'Bajo'
  if (n <= 6) return 'Medio'
  return 'Alto'
})

const nivelSarcasmoTexto = computed(() => {
  if (!store.resultado) return ''
  const n = store.resultado.nivelSarcasmo
  if (n <= 3) return 'Bajo'
  if (n <= 6) return 'Medio'
  return 'Alto'
})

const formalidadTexto = computed(() => {
  if (!store.resultado) return ''
  const n = store.resultado.nivelFormalidad
  if (n <= 2) return 'Informal'
  if (n <= 3.5) return 'Neutral'
  return 'Formal'
})

function nivelToBarras(nivel: number, max: number): number {
  if (max === 3) {
    if (nivel <= 3) return 1
    if (nivel <= 6) return 2
    return 3
  }
  return Math.min(Math.ceil((nivel / 10) * max), max)
}

function ironiaClase(barIndex: number): string {
  if (!store.resultado) return 'inactive'
  const activas = nivelToBarras(store.resultado.nivelIronia, 3)
  return barIndex <= activas ? 'active' : 'inactive'
}

function sarcasmoClase(barIndex: number): string {
  if (!store.resultado) return 'inactive'
  const activas = nivelToBarras(store.resultado.nivelSarcasmo, 3)
  return barIndex <= activas ? 'active' : 'inactive'
}

function formalidadClase(barIndex: number): string {
  if (!store.resultado) return 'inactive'
  // Para formalidad: invertimos la logica (1=formal, 5=informal)
  // Pero usamos nivelToBarras directamente (1=mas formal, 5=mas informal)
  const activas = Math.round(store.resultado.nivelFormalidad)
  return barIndex <= activas ? 'active' : 'inactive'
}
</script>

<style scoped>
/* Manten los mismos estilos que ya existen en el archivo actual,
   pero agrega estos adicionales: */

.context-section {
  margin-top: 0.5rem;
}

.context-toggle {
  background: none;
  border: 1px dashed var(--border-color, #ccc);
  color: var(--text-muted);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.context-toggle:hover {
  border-color: var(--brand-accent);
  color: var(--brand-accent);
  background: rgba(var(--brand-accent-rgb), 0.05);
}

.context-panel {
  margin-top: 0.75rem;
  background: var(--brand-card-inner);
  border-radius: 10px;
  padding: 1rem;
  border: 1px solid var(--border-color);
}

.context-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.tab {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: none;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.2s;
}

.tab.active {
  background: var(--brand-accent);
  color: #fff;
  border-color: var(--brand-accent);
}

.predef-hint {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.escenario-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.5rem;
}

.escenario-card {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-family: inherit;
  color: inherit;
}

.escenario-card:hover {
  border-color: var(--brand-dark);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transform: translateY(-1px);
}

.escenario-card.selected {
  border-color: var(--brand-accent);
  background: rgba(74, 93, 53, 0.04);
  box-shadow: 0 0 0 2px rgba(74, 93, 53, 0.15);
}

.esc-icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--brand-sidebar);
  flex-shrink: 0;
}

.esc-icon {
  color: var(--brand-dark);
}

.escenario-card.selected .esc-icon-wrapper {
  background: rgba(74, 93, 53, 0.15);
}

.esc-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.esc-nombre {
  font-size: 0.85rem;
  font-weight: 800;
  color: #111;
  line-height: 1.2;
}

.esc-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
  line-height: 1.3;
  margin-top: 0.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.esc-check {
  color: var(--brand-accent);
  flex-shrink: 0;
}

@media (max-width: 500px) {
  .escenario-grid {
    grid-template-columns: 1fr;
  }
}

.context-textarea {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: #fff;
  font-size: 0.9rem;
  color: #111;
  resize: vertical;
  font-family: inherit;
}

.componentes-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.componente-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.6rem;
  background: #fff;
  border-radius: 6px;
  font-size: 0.9rem;
}

.comp-token {
  font-weight: 700;
  color: var(--brand-dark);
  min-width: 80px;
}

.comp-arrow {
  color: var(--text-muted);
}

.comp-trad {
  flex: 1;
  color: #111;
}

.comp-tipo {
  font-size: 0.75rem;
  color: var(--text-muted);
  background: var(--brand-tag);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: 600;
}

.alternativa-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}

.alternativa-item:last-child {
  border-bottom: none;
}

.alt-trad {
  font-weight: 600;
  color: #111;
}

.alt-ctx {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.context-name {
  font-weight: 700;
  color: #111;
  font-size: 1rem;
}

.context-confianza {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.confianza-valor {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--brand-accent);
}

.error-state {
  text-align: center;
  padding: 2rem 1rem;
  color: #c0392b;
  font-weight: 500;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  max-height: 300px;
}

/* ===== Mantener los estilos existentes del archivo original ===== */
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.traductor-container {
  max-width: 1000px;
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

.view-header .title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
}

.view-header .subtitle {
  font-size: 1rem;
  color: var(--text-main);
  margin-top: 0.25rem;
}

.search-bar-container {
  width: 100%;
  height: 60px;
  background-color: rgba(var(--brand-note-rgb), 0.12);
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
}

.search-input-wrapper {
  flex: 1;
  height: 44px;
  background-color: var(--brand-sidebar);
  border-radius: 999px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  transition: box-shadow 0.2s;
}

.search-input-wrapper:focus-within {
  box-shadow: 0 0 0 3px rgba(var(--brand-dark-rgb), 0.12);
}

.search-input {
  width: 100%;
  font-size: 1rem;
  color: #111;
  font-weight: 500;
  background: none;
  border: none;
  outline: none;
}

.search-input::placeholder {
  color: #888;
}

.translate-btn {
  height: 44px;
  background-color: var(--brand-accent);
  color: #fff;
  border: none;
  padding: 0 1.5rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
  white-space: nowrap;
}

.translate-btn:hover:not(:disabled) {
  background-color: #3d4f30;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.translate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem 1rem;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color, #e2e5dc);
  border-top-color: var(--brand-dark);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.result-enter-enter-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.result-enter-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

.results-inner {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.main-card-white {
  flex: 2.5;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}

.card-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
}

.phrase-text {
  font-size: 2.2rem;
  font-weight: 800;
  color: #111;
  margin: 0.5rem 0 2rem 0;
}

.inner-box {
  background-color: var(--brand-card-inner);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.box-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.box-header h3 {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.inner-box p {
  font-size: 1rem;
  font-weight: 500;
  color: #111;
}

.dark-note {
  background-color: var(--brand-note);
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.dark-note p,
.note-icon {
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1.4;
}

.side-info-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.small-card {
  background-color: #f7f9f4;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
}

.small-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.card-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

.irony-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.irony-bars {
  display: flex;
  gap: 4px;
}

.bar {
  width: 20px;
  height: 6px;
  border-radius: 99px;
}

.bar.active { background-color: #6da34d; }
.bar.inactive { background-color: #e2e8d5; }

.link-card {
  background-color: #E2E3DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
  transition: box-shadow 0.2s, transform 0.2s;
}

.link-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  transform: translateY(-1px);
}

.link-content p {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

.no-results,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  font-size: 1rem;
}
</style>
