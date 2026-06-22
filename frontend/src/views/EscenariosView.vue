<template>
  <div class="escenarios-container">
    <header class="view-header">
      <h1 class="title">Escenarios Sociales</h1>
      <p class="subtitle">Explora situaciones cotidianas donde se usan las expresiones chilenas.</p>
    </header>

    <div v-if="store.loading" class="loading-state">Cargando escenarios...</div>

    <div v-else-if="store.error" class="error-state">
      <p>{{ store.error }}</p>
      <button class="btn-retry" @click="store.fetchEscenarios()">Reintentar</button>
    </div>

    <template v-else>
      <div class="search-wrapper">
        <input
          v-model="busqueda"
          type="text"
          placeholder="Buscar escenario..."
          class="search-input"
          @input="onBuscar"
        />
      </div>

      <div v-if="store.escenarios.length === 0" class="empty-state">
        No se encontraron escenarios. Intenta con otros términos.
      </div>

      <div v-else class="accordion">
        <div
          v-for="escenario in store.escenarios"
          :key="escenario.id"
          class="accordion-item"
          :class="{ expanded: expandedIds.has(escenario.id) }"
          :style="{ '--i': store.escenarios.indexOf(escenario) }"
        >
          <button class="accordion-header" @click="toggleEscenario(escenario.id)">
            <div class="accordion-header-left">
              <div class="accordion-icon-wrapper">
                <component :is="iconoComponent(escenario.icono)" :size="24" class="accordion-icon" />
              </div>
              <div class="accordion-header-text">
                <h3 class="accordion-title">{{ escenario.nombre }}</h3>
                <p class="accordion-desc">{{ escenario.descripcion }}</p>
              </div>
            </div>
            <div class="accordion-header-right">
              <span class="frase-count-badge">
                {{ escenario.total_frases }} {{ escenario.total_frases === 1 ? 'situación' : 'situaciones' }}
              </span>
              <span class="chevron" :class="{ rotated: expandedIds.has(escenario.id) }">
                <ChevronDown :size="20" />
              </span>
            </div>
          </button>

          <transition name="accordion-body">
            <div v-if="expandedIds.has(escenario.id)" class="accordion-body">
              <div v-if="loadingEscenarioIds.has(escenario.id)" class="loading-frases">
                Cargando situaciones...
              </div>
              <div v-else-if="detalle(escenario.id)?.frases.length === 0" class="empty-frases">
                No hay situaciones registradas para este escenario aún.
              </div>
              <TransitionGroup v-else name="card-enter" tag="div" class="escenas-list">
                <router-link
                  v-for="(frase, idx) in detalle(escenario.id)?.frases ?? []"
                  :key="frase.id"
                  :to="`/escenarios/${escenario.id}/frases/${frase.id}`"
                  class="escena-card"
                  :style="{ '--card-delay': idx * 0.05 + 's' }"
                >
                  <div class="escena-imagen" :style="{ background: gradientParaEscena(frase.id) }">
                    <div class="escena-icon-circle">
                      <component :is="iconoParaEscena(frase.id)" :size="22" />
                    </div>
                    <span class="escena-imagen-label">Ver conversación</span>
                  </div>

                  <div class="escena-contenido">
                    <div class="escena-tags">
                      <span v-if="frase.tono" class="frase-tono" :class="'tono--' + frase.tono">{{ frase.tono }}</span>
                      <span class="meta-chip">
                        <Briefcase :size="12" /> Formalidad {{ frase.nivel_formalidad }}/10
                      </span>
                      <span v-if="frase.nivel_ironia > 0" class="meta-chip">
                        <MessageCircle :size="12" /> Ironía {{ frase.nivel_ironia }}/10
                      </span>
                    </div>

                    <div class="escena-expresion">
                      <span class="expresion-label">EXPRESIÓN</span>
                      <p class="expresion-texto">&ldquo;{{ frase.frase_original }}&rdquo;</p>
                      <p class="expresion-traduccion">{{ frase.traduccion }}</p>
                    </div>

                    <div v-if="frase.explicacion" class="escena-contexto">
                      <span class="contexto-label">CONTEXTO</span>
                      <p>{{ frase.explicacion }}</p>
                    </div>

                    <div class="escena-ver">
                      <span>Ver conversación completa &rarr;</span>
                    </div>
                  </div>
                </router-link>
              </TransitionGroup>
            </div>
          </transition>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Component } from 'vue'
import {
  ChevronDown, Briefcase, MessageCircle,
  Users, Home, Building2, HeartPulse, Sparkles,
  MessageSquare, Speech, Camera, BookOpen, Star, Heart,
  Sun,
} from 'lucide-vue-next'
import { useEscenariosStore } from '../store/escenarios'
import type { EscenarioDetail } from '../types'

const store = useEscenariosStore()
const busqueda = ref('')
const expandedIds = ref(new Set<number>())
const loadingEscenarioIds = ref(new Set<number>())

const iconoComponentMap: Record<string, Component> = {
  'briefcase': Briefcase,
  'heart-pulse': HeartPulse,
  'people': Users,
  'building': Building2,
  'house': Home,
  'party-popper': Sparkles,
}

function iconoComponent(icono: string | null): Component {
  if (!icono) return MessageSquare
  return iconoComponentMap[icono] || MessageSquare
}

const escenaGradientes = [
  'linear-gradient(135deg, #fef3c7, #fde68a)',
  'linear-gradient(135deg, #d1fae5, #a7f3d0)',
  'linear-gradient(135deg, #e0f2fe, #bae6fd)',
  'linear-gradient(135deg, #ede9fe, #c4b5fd)',
  'linear-gradient(135deg, #fce7f3, #f9a8d4)',
  'linear-gradient(135deg, #fce4ec, #fecaca)',
  'linear-gradient(135deg, #e0e7ff, #a5b4fc)',
  'linear-gradient(135deg, #fef9c3, #fde047)',
]

const escenaIconos: Component[] = [
  MessageSquare, Speech, MessageCircle, Camera,
  BookOpen, Star, Heart, Sun,
]

function gradientParaEscena(id: number): string {
  return escenaGradientes[id % escenaGradientes.length]
}

function iconoParaEscena(id: number): Component {
  return escenaIconos[id % escenaIconos.length]
}

function detalle(id: number): EscenarioDetail | undefined {
  return store.detallesCache[id]
}

async function toggleEscenario(id: number) {
  if (expandedIds.value.has(id)) {
    expandedIds.value.delete(id)
    expandedIds.value = new Set(expandedIds.value)
    return
  }
  expandedIds.value.add(id)
  expandedIds.value = new Set(expandedIds.value)

  if (!store.detallesCache[id]) {
    loadingEscenarioIds.value.add(id)
    loadingEscenarioIds.value = new Set(loadingEscenarioIds.value)
    await store.fetchFrasesPorEscenario(id)
    loadingEscenarioIds.value.delete(id)
    loadingEscenarioIds.value = new Set(loadingEscenarioIds.value)
  }
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null

function onBuscar() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    store.setFiltros({ busqueda: busqueda.value || undefined })
    store.fetchEscenarios()
    expandedIds.value = new Set()
  }, 300)
}

onMounted(() => {
  store.fetchEscenarios()
})
</script>

<style scoped>
/* ===== Animations ===== */
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes accordionSlideIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes cardFadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ===== Contenedor principal ===== */
.escenarios-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 3rem;
  animation: viewFadeIn 0.5s ease both;
}

/* ===== Header ===== */
.view-header {
  border-left: 6px solid var(--brand-dark);
  padding-left: 1.5rem;
  margin-bottom: 0.5rem;
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

/* ===== Búsqueda ===== */
.search-wrapper {
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 8px;
  font-size: 0.95rem;
  background: #fff;
  color: #111;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
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

/* ===== Acordeón ===== */
.accordion {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.accordion-item {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s;
  animation: accordionSlideIn 0.4s ease both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}

.accordion-item:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.accordion-item.expanded {
  border-color: var(--brand-dark);
  box-shadow: 0 4px 16px rgba(45, 51, 34, 0.1);
}

/* ===== Header del acordeón ===== */
.accordion-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  color: inherit;
  font: inherit;
  text-align: left;
  transition: background-color 0.15s;
}

.accordion-header:hover {
  background-color: #fafbf8;
}

.accordion-header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

.accordion-icon-wrapper {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--brand-sidebar);
  flex-shrink: 0;
}

.accordion-icon {
  color: var(--brand-dark);
}

.accordion-header-text {
  flex: 1;
  min-width: 0;
}

.accordion-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.accordion-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 0.15rem 0 0;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.accordion-header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.frase-count-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--brand-dark);
  background: var(--brand-sidebar);
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  white-space: nowrap;
}

.chevron {
  display: flex;
  color: var(--text-muted);
  transition: transform 0.25s ease;
}

.chevron.rotated {
  transform: rotate(180deg);
}

/* ===== Cuerpo del acordeón ===== */
.accordion-body-enter-active,
.accordion-body-leave-active {
  transition: max-height 0.3s ease, opacity 0.25s ease;
  max-height: 3000px;
  overflow: hidden;
}

.accordion-body-enter-from,
.accordion-body-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.accordion-body {
  border-top: 1px solid var(--border-color, #e2e5dc);
  padding: 1.25rem 1.5rem;
}

.loading-frases,
.empty-frases {
  text-align: center;
  padding: 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.95rem;
}

/* ===== TransitionGroup: entrada escalonada de cards ===== */
.card-enter-enter-active {
  animation: cardFadeSlideUp 0.4s ease both;
  animation-delay: var(--card-delay, 0s);
}

.card-enter-leave-active {
  transition: opacity 0.2s ease;
}

.card-enter-enter-from,
.card-enter-leave-to {
  opacity: 0;
}

.escenas-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* ===== Card de escena ===== */
.escena-card {
  display: block;
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: box-shadow 0.25s ease, transform 0.2s ease, border-color 0.2s ease;
}

.escena-card:hover {
  box-shadow: 0 6px 20px rgba(45, 51, 34, 0.1);
  transform: translateY(-2px);
  border-color: var(--brand-dark);
}

/* ===== Área de imagen decorativa ===== */
.escena-imagen {
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  position: relative;
}

.escena-icon-circle {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.escena-card:hover .escena-icon-circle {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.escena-icon-circle :deep(svg) {
  color: #111;
}

.escena-imagen-label {
  font-size: 0.68rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.35);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* ===== Contenido de la escena ===== */
.escena-contenido {
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Tags y chips */
.escena-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.frase-tono {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  letter-spacing: 0.03em;
}

.tono--ironico {
  background: #fef3c7;
  color: #92400e;
}

.tono--sarcastico {
  background: #fce4ec;
  color: #c62828;
}

.tono--directo {
  background: #e0f2fe;
  color: #0369a1;
}

.tono--humoristico {
  background: #d1fae5;
  color: #065f46;
}

.tono--motivacional {
  background: #ede9fe;
  color: #5b21b6;
}

.tono--neutro {
  background: #f3f4f6;
  color: #4b5563;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
  background: #f3f4f6;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

/* Expresión destacada */
.escena-expresion {
  background: #f7f9f4;
  border-radius: 8px;
  padding: 1rem 1.25rem;
}

.expresion-label,
.contexto-label,
.ejemplo-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.06em;
  display: block;
  margin-bottom: 0.35rem;
}

.expresion-texto {
  font-size: 1.15rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.expresion-traduccion {
  font-size: 0.9rem;
  color: var(--text-main);
  margin: 0.25rem 0 0;
  font-style: italic;
}

/* Contexto y ejemplo */
.escena-contexto p {
  font-size: 0.9rem;
  color: var(--text-main);
  line-height: 1.5;
  margin: 0;
}

.escena-ver {
  margin-top: 0.75rem;
  text-align: right;
}

.escena-ver span {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--brand-dark);
  transition: gap 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.escena-card:hover .escena-ver span {
  gap: 0.5rem;
}
</style>
