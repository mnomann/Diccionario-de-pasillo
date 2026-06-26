<template>
  <div class="chat-view">
    <button class="btn-volver" @click="$router.push('/escenarios')">
      <ArrowLeft :size="18" />
      <span>Volver a escenarios</span>
    </button>

    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner" />
      <p>Cargando conversación...</p>
    </div>

    <div v-else-if="!store.fraseActual" class="error-state">
      <p>No se pudo cargar la conversación.</p>
      <button class="btn-retry" @click="cargarFrase">Reintentar</button>
    </div>

    <template v-else>
      <header class="chat-header">
        <div class="chat-header-top">
          <div class="chat-title-group">
            <h1 class="chat-title">{{ store.fraseActual.frase_original }}</h1>
            <span v-if="store.fraseActual.tono" class="tono-badge" :class="'tono--' + store.fraseActual.tono">
              {{ store.fraseActual.tono }}
            </span>
          </div>
          <p class="chat-subtitle">{{ store.fraseActual.traduccion }}</p>
        </div>
        <div class="chat-meta-bar">
          <span class="chat-escenario">{{ store.fraseActual.escenario?.nombre }}</span>
        </div>
      </header>

      <div v-if="conversacionActual" class="conversacion-container">
        <div class="chat-participantes">
          <span v-for="p in conversacionActual.participantes" :key="p" class="participante-chip">
            <span class="participante-avatar" :style="{ background: colorParaParticipante(p) }">
              {{ iniciales(p) }}
            </span>
            {{ p }}
          </span>
        </div>

        <TransitionGroup name="burbuja-enter" tag="div" class="chat-burbujas">
          <div
            v-for="(msg, i) in conversacionActual.mensajes"
            :key="i"
            class="burbuja-wrapper"
            :class="'alineacion--' + alinearMensaje(msg.emisor, i)"
            :style="{ '--b-delay': i * 0.07 + 's' }"
          >
            <div
              class="burbuja"
              :class="{
                'burbuja--modismo': msg.es_modismo,
                'burbuja--normal': !msg.es_modismo,
              }"
            >
              <div class="burbuja-header">
                <span class="burbuja-emisor">{{ msg.emisor }}</span>
                <span v-if="msg.es_modismo" class="burbuja-etiqueta">Modismo</span>
              </div>
              <p class="burbuja-texto">{{ msg.texto }}</p>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <div v-else-if="store.fraseActual.ejemplo_uso" class="sin-conversacion">
        <div class="sin-conv-icon">
          <MessageSquare :size="24" />
        </div>
        <h3 class="sin-conv-title">Ejemplo de uso</h3>
        <p class="sin-conv-texto">{{ store.fraseActual.ejemplo_uso }}</p>
      </div>

      <section v-if="store.fraseActual.explicacion" class="contexto-section">
        <h2 class="contexto-title">Contexto y explicación</h2>
        <p class="contexto-texto">{{ store.fraseActual.explicacion }}</p>
        <div v-if="store.fraseActual.intencion_real" class="intencion-box">
          <span class="intencion-label">Intención real</span>
          <p>{{ store.fraseActual.intencion_real }}</p>
        </div>
        <div class="meta-tags">
          <span class="meta-chip">
            <Briefcase :size="14" /> Formalidad {{ store.fraseActual.nivel_formalidad }}/10
          </span>
          <span v-if="store.fraseActual.nivel_ironia > 0" class="meta-chip">
            <MessageCircle :size="14" /> Ironía {{ store.fraseActual.nivel_ironia }}/10
          </span>
          <span v-if="store.fraseActual.nivel_sarcasmo > 0" class="meta-chip">
            <MessageCircle :size="14" /> Sarcasmo {{ store.fraseActual.nivel_sarcasmo }}/10
          </span>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Briefcase, MessageCircle, MessageSquare, ArrowLeft } from 'lucide-vue-next'
import { useFrasesStore } from '../store/frases'
import type { Conversacion, FraseDetail } from '../types'

const route = useRoute()
const store = useFrasesStore()

const fraseId = Number(route.params.fid)

function generarConversacion(frase: FraseDetail): Conversacion {
  const emisor1 = 'Carlos'
  const emisor2 = 'María'
  const f = frase.frase_original
  const t = frase.traduccion

  const mensajes: { emisor: string; texto: string; es_modismo: boolean }[] = [
    {
      emisor: emisor1,
      texto: `Oye, anoche un amigo chileno me dijo "${f}" y me quedé pillo sin saber qué responder.`,
      es_modismo: true,
    },
    {
      emisor: emisor2,
      texto: 'Jaja, te entiendo. Acá usan esas frases todo el tiempo.',
      es_modismo: false,
    },
    {
      emisor: emisor2,
      texto: `"${f}" significa "${t[0].toLowerCase() + t.slice(1)}".`,
      es_modismo: false,
    },
  ]

  if (frase.explicacion) {
    mensajes.push({
      emisor: emisor1,
      texto: `Ah, tiene sentido. O sea que ${frase.explicacion[0].toLowerCase() + frase.explicacion.slice(1)}`,
      es_modismo: false,
    })
  }

  if (frase.ejemplo_uso) {
    mensajes.push({
      emisor: emisor2,
      texto: `Exacto. Por ejemplo: "${frase.ejemplo_uso}"`,
      es_modismo: false,
    })
  }

  mensajes.push(
    {
      emisor: emisor1,
      texto: `Ya, ahora si alguien me suelta un "${f}" voy a cachar altiro.`,
      es_modismo: true,
    },
    {
      emisor: emisor2,
      texto: 'Ahí está la weá buena, ya estai hablando como chileno jaja.',
      es_modismo: false,
    },
  )

  return { participantes: [emisor1, emisor2], mensajes }
}

const conversacionActual = computed<Conversacion | null>(() => {
  if (store.fraseActual?.conversacion) return store.fraseActual.conversacion
  if (store.fraseActual) return generarConversacion(store.fraseActual)
  return null
})

const coloresParticipantes = [
  '#2d3322', '#5b6647', '#92400e', '#065f46',
  '#0369a1', '#5b21b6', '#c62828', '#1e40af',
]

function hashString(s: string): number {
  let hash = 0
  for (let i = 0; i < s.length; i++) {
    hash = ((hash << 5) - hash) + s.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(hash)
}

function colorParaParticipante(nombre: string): string {
  return coloresParticipantes[hashString(nombre) % coloresParticipantes.length]
}

function iniciales(nombre: string): string {
  return nombre.split(/\s+/).map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

function alinearMensaje(emisor: string, _index: number): 'izquierda' | 'derecha' {
  if (!conversacionActual.value) return 'izquierda'
  const primerEmisor = conversacionActual.value.participantes[0]
  return emisor === primerEmisor ? 'izquierda' : 'derecha'
}

function cargarFrase() {
  if (!isNaN(fraseId)) {
    store.fetchFrase(fraseId)
  }
}

onMounted(cargarFrase)
</script>

<style scoped>
/* ===== Animations ===== */
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes bubbleSlideIn {
  from { opacity: 0; transform: translateY(12px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chat-view {
  max-width: 700px;
  margin: 0 auto;
  padding-bottom: 3rem;
  animation: viewFadeIn 0.4s ease both;
}

/* ===== Botón volver ===== */
.btn-volver {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: none;
  border: none;
  color: var(--brand-accent);
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.4rem 0.6rem;
  margin-bottom: 1.25rem;
  border-radius: 6px;
  transition: background-color 0.15s, color 0.15s;
}

.btn-volver:hover {
  background: rgba(var(--brand-note-rgb), 0.1);
  color: var(--brand-dark);
}

/* ===== Estados ===== */
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
  border-top-color: var(--brand-accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.error-state {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--text-muted);
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: var(--brand-accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-retry:hover {
  background: #3d4f30;
}

/* ===== Header ===== */
.chat-header {
  margin-bottom: 2rem;
  padding-left: 1.25rem;
  border-left: 4px solid var(--brand-accent);
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
}

.chat-header-top {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.chat-title-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.chat-title {
  font-size: 1.8rem;
  font-weight: 900;
  color: #111;
  margin: 0;
}

.tono-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  letter-spacing: 0.03em;
}

.chat-subtitle {
  font-size: 1rem;
  color: var(--text-main);
  font-style: italic;
  margin: 0;
}

.chat-meta-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
}

.chat-escenario {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--brand-accent);
  background: rgba(var(--brand-note-rgb), 0.1);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
}

/* ===== Participantes ===== */
.chat-participantes {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.participante-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  background: var(--brand-sidebar-deeper);
  padding: 0.35rem 0.85rem 0.35rem 0.35rem;
  border-radius: 999px;
}

.participante-avatar {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.65rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

/* ===== Burbujas de chat ===== */
.conversacion-container {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  animation: slideUp 0.5s ease both;
  animation-delay: 0.15s;
}

.chat-burbujas {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* TransitionGroup: entrada escalonada */
.burbuja-enter-enter-active {
  animation: bubbleSlideIn 0.3s ease both;
  animation-delay: var(--b-delay, 0s);
}

.burbuja-enter-leave-active {
  transition: opacity 0.2s ease;
}

.burbuja-enter-enter-from,
.burbuja-enter-leave-to {
  opacity: 0;
}

.burbuja-wrapper {
  display: flex;
}

.alineacion--izquierda {
  justify-content: flex-start;
}

.alineacion--derecha {
  justify-content: flex-end;
}

.burbuja {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 14px;
  position: relative;
}

.burbuja--normal {
  background: var(--brand-sidebar);
  color: #111;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

.alineacion--izquierda .burbuja--normal {
  border-bottom-left-radius: 4px;
}

.alineacion--derecha .burbuja--normal {
  border-bottom-right-radius: 4px;
}

.burbuja--modismo {
  background: #fef3c7;
  color: #111;
  border: 1px solid #fde68a;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.alineacion--izquierda .burbuja--modismo {
  border-bottom-left-radius: 4px;
}

.alineacion--derecha .burbuja--modismo {
  border-bottom-right-radius: 4px;
}

.burbuja-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.burbuja-emisor {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.burbuja-etiqueta {
  font-size: 0.55rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #92400e;
  background: rgba(0,0,0,0.05);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
}

.burbuja-texto {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.45;
}

/* ===== Sin conversación estructurada ===== */
.sin-conversacion {
  background: rgba(var(--brand-note-rgb), 0.06);
  border: 1px solid rgba(var(--brand-note-rgb), 0.12);
  border-radius: 14px;
  padding: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  animation: slideUp 0.5s ease both;
  animation-delay: 0.15s;
}

.sin-conv-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(var(--brand-note-rgb), 0.15);
  color: var(--brand-accent);
  margin-bottom: 0.25rem;
}

.sin-conv-title {
  font-size: 1rem;
  font-weight: 800;
  color: #111;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.sin-conv-texto {
  font-size: 0.95rem;
  color: var(--text-main);
  font-style: italic;
  line-height: 1.5;
  max-width: 500px;
  margin: 0;
}

/* ===== Sección de contexto ===== */
.contexto-section {
  background: #fff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  animation: slideUp 0.5s ease both;
  animation-delay: 0.3s;
}

.contexto-title {
  font-size: 1rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.contexto-texto {
  font-size: 0.9rem;
  color: var(--text-main);
  line-height: 1.6;
  margin: 0;
}

.intencion-box {
  background: rgba(var(--brand-note-rgb), 0.06);
  border-left: 3px solid var(--brand-accent);
  padding: 0.75rem 1rem;
  margin-top: 1rem;
  border-radius: 0 8px 8px 0;
}

.intencion-label {
  display: block;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
  text-transform: uppercase;
}

.intencion-box p {
  margin: 0;
  font-size: 0.9rem;
  color: #444;
}

.meta-tags {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color, #e2e5dc);
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand-note);
  background: rgba(var(--brand-note-rgb), 0.08);
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
}

/* ===== Reuso tonos ===== */
.tono--ironico { background: #fef3c7; color: #92400e; }
.tono--sarcastico { background: #fce4ec; color: #c62828; }
.tono--directo { background: #e0f2fe; color: #0369a1; }
.tono--humoristico { background: #d1fae5; color: #065f46; }
.tono--motivacional { background: #ede9fe; color: #5b21b6; }
.tono--neutro { background: #f3f4f6; color: #4b5563; }
</style>
