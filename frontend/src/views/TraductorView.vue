<template>
  <div class="traductor-container">
    <header class="view-header">
      <h2 class="title">DESCIFRADOR DE CHILE</h2>
      <p class="subtitle">Introduce una frase para entender su contexto real.</p>
    </header>

    <div class="search-bar-container">
      <div class="search-input-wrapper">
        <input
          class="search-input"
          type="text"
          v-model="store.query"
          placeholder="Ej: Estoy pato"
          @keyup.enter="buscar"
        />
      </div>
      <button class="translate-btn" @click="buscar" :disabled="store.loading">
        <Languages :size="18" />
        {{ store.loading ? 'BUSCANDO...' : 'TRADUCIR' }}
      </button>
    </div>

    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner" />
      <p>Buscando...</p>
    </div>

    <div v-if="store.resultado" class="results-layout">
      <transition name="result-enter">
        <div class="results-inner">
          <div class="main-card-white">
            <span class="card-label">FRASE ORIGINAL</span>
            <h1 class="phrase-text">"{{ store.resultado.fraseOriginal }}"</h1>

            <div class="inner-box">
              <div class="box-header">
                <BookOpen :size="16" />
                <h3>SIGNIFICADO LITERAL</h3>
              </div>
              <p>{{ store.resultado.significadoLiteral }}</p>
            </div>

            <div class="inner-box">
              <div class="box-header">
                <MessageSquare :size="16" />
                <h3>USO COMÚN</h3>
              </div>
              <p>{{ store.resultado.usoComun }}</p>

              <div class="dark-note">
                <Info :size="18" class="note-icon" />
                <p>{{ store.resultado.nota }}</p>
              </div>
            </div>
          </div>

          <aside class="side-info-column">
            <div class="small-card">
              <h3 class="card-title">NIVEL DE IRONÍA</h3>
              <div class="irony-row">
                <span>{{ store.resultado.nivelIronia }}</span>
                <div class="irony-bars">
                  <div class="bar" :class="ironiaClase(1)"></div>
                  <div class="bar" :class="ironiaClase(2)"></div>
                  <div class="bar" :class="ironiaClase(3)"></div>
                </div>
              </div>
            </div>

            <div class="small-card">
              <h3 class="card-title">ETIQUETAS</h3>
              <div class="tags-container">
                <span v-for="tag in store.resultado.etiquetas" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>

            <router-link to="/escenarios" class="small-card link-card" style="text-decoration: none;">
              <div class="link-content">
                <h3 class="card-title">APRENDER ESCENARIOS SOCIALES</h3>
                <p>Ver ejemplos de cómo usar esta frase en la vida real.</p>
              </div>
              <ArrowRight :size="20" />
            </router-link>
          </aside>
        </div>
      </transition>
    </div>

    <div v-else-if="store.query && !store.loading" class="no-results">
      <p>No se encontraron resultados para "{{ store.query }}".</p>
    </div>

    <div v-else-if="!store.loading" class="empty-state">
      <p>Introduce una frase chilena para obtener su significado y contexto.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Languages, BookOpen, MessageSquare, Info, ArrowRight } from 'lucide-vue-next'
import { useTraductorStore } from '../store/traductor'

const store = useTraductorStore()

function buscar() {
  if (store.query.trim()) {
    store.traducir(store.query.trim())
  }
}

function ironiaClase(barIndex: number): string {
  if (!store.resultado) return 'inactive'
  const niveles: Record<string, number> = { Bajo: 1, Medio: 2, Alto: 3 }
  const nivel = niveles[store.resultado.nivelIronia] || 0
  return barIndex <= nivel ? 'active' : 'inactive'
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

.traductor-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  animation: viewFadeIn 0.5s ease both;
}

/* ===== Encabezado ===== */
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

/* ===== Barra de búsqueda ===== */
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
  border-top-color: var(--brand-dark);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

/* ===== Transición de resultados ===== */
.result-enter-enter-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.result-enter-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

/* ===== Layout de resultados ===== */
.results-layout {
  /* outer wrapper for transition v-if */
}

.results-inner {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

/* ===== Tarjeta principal ===== */
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

/* ===== Columna lateral ===== */
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

/* Ironía */
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

/* Tags */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background-color: var(--brand-tag);
  color: #a45a41;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
}

/* Link card */
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

/* Estados vacío / sin resultados */
.loading-state,
.no-results,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  font-size: 1rem;
}
</style>
