<template>
  <div class="frases-container">
    <header class="view-header">
      <div class="header-text">
        <h1 class="title">Frases Frecuentes</h1>
        <p class="subtitle">Aprende y practica las frases más usadas en Chile.</p>
      </div>
      <div class="header-actions">
        <button class="btn-filter">
          <Filter :size="16" />
          Filtrar
        </button>
        <button class="btn-new">
          <Plus :size="16" />
          Nueva Frase
        </button>
      </div>
    </header>

    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner" />
      <p>Cargando frases...</p>
    </div>

    <TransitionGroup v-else name="card-enter" tag="div" class="frases-grid">
      <article
        v-for="(frase, idx) in store.frases"
        :key="frase.id"
        :class="['frase-card', frase.type === 'wide' ? 'wide-card' : 'normal-card']"
        :style="{ '--card-delay': idx * 0.04 + 's' }"
      >
        <template v-if="frase.type === 'normal'">
          <div class="card-image-placeholder">
            <div class="placeholder-icon">
              <MessageSquare :size="24" />
            </div>
            <span class="placeholder-text">{{ frase.word }}</span>
          </div>
          <div class="card-content">
            <div class="card-top-row">
              <h2 class="word-title">{{ frase.word }}</h2>
              <Volume2 :size="18" class="speaker-icon" />
            </div>
            <p class="word-meaning">{{ frase.meaning }}</p>

            <div v-if="frase.tags" class="tags-row">
              <span v-for="tag in frase.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </template>

        <template v-else>
          <div class="wide-content-wrapper">
            <div class="wide-header">
              <div>
                <h2 class="word-title">{{ frase.word }}</h2>
                <p class="word-meaning">{{ frase.meaning }}</p>
              </div>
              <Volume2 :size="20" class="speaker-icon" />
            </div>

            <div class="example-quote">
              <p>{{ frase.example }}</p>
            </div>

            <div class="tags-row">
              <span v-for="tag in frase.tags" :key="tag" class="tag dark-tag">{{ tag }}</span>
            </div>
          </div>
        </template>
      </article>
    </TransitionGroup>

    <div class="bottom-action">
      <button class="btn-load-more">Cargar más frases</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Filter, Plus, Volume2, MessageSquare } from 'lucide-vue-next'
import { useFrasesStore } from '../store/frases'

const store = useFrasesStore()

onMounted(() => {
  store.fetchFrases()
})
</script>

<style scoped>
@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes cardFadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.frases-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-bottom: 3rem;
  animation: viewFadeIn 0.5s ease both;
}

/* ===== Header ===== */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-left: 6px solid var(--brand-accent);
  padding-left: 1.5rem;
}

.title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 0.25rem;
}

.subtitle {
  font-size: 1rem;
  color: var(--text-main);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn-filter,
.btn-new {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-filter {
  background-color: transparent;
  border: 1px solid var(--border-color, #e2e5dc);
  color: #333;
}

.btn-filter:hover {
  background-color: rgba(0,0,0,0.04);
  border-color: #bbb;
}

.btn-new {
  background-color: var(--brand-dark);
  border: 1px solid var(--brand-dark);
  color: #fff;
}

.btn-new:hover {
  opacity: 0.9;
  box-shadow: 0 2px 6px rgba(45, 51, 34, 0.15);
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

/* ===== TransitionGroup: entrada escalonada ===== */
.card-enter-enter-active {
  animation: cardFadeSlideUp 0.35s ease both;
  animation-delay: var(--card-delay, 0s);
}

.card-enter-leave-active {
  transition: opacity 0.2s ease;
}

.card-enter-enter-from,
.card-enter-leave-to {
  opacity: 0;
}

/* ===== Grilla ===== */
.frases-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

/* ===== Tarjetas ===== */
.frase-card {
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-color, #e2e5dc);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.25s ease, transform 0.2s ease, border-color 0.2s ease;
}

.frase-card:hover {
  box-shadow: 0 6px 20px rgba(45, 51, 34, 0.08);
  transform: translateY(-2px);
  border-color: var(--brand-dark);
}

.wide-card {
  grid-column: span 2;
  padding: 1.5rem;
  justify-content: center;
  background-color: #ffffff;
  background-image: radial-gradient(circle at 70% 50%, #f7f9f4 0%, transparent 40%);
}

.normal-card {
  grid-column: span 1;
}

/* ===== Placeholder de imagen ===== */
.card-image-placeholder {
  height: 140px;
  background: linear-gradient(135deg, #dae0c8, #c8d2b0);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  color: #5a6f42;
}

.placeholder-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  transition: transform 0.25s ease;
}

.frase-card:hover .placeholder-icon {
  transform: scale(1.1);
}

.placeholder-text {
  font-size: 0.75rem;
  font-weight: 600;
  font-style: italic;
  opacity: 0.7;
}

/* ===== Contenido tarjeta normal ===== */
.card-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.word-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #111;
}

.speaker-icon {
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.15s;
  flex-shrink: 0;
}

.speaker-icon:hover {
  color: var(--brand-dark);
}

.word-meaning {
  font-size: 0.9rem;
  color: var(--text-main);
  line-height: 1.4;
  margin-bottom: 1rem;
  flex-grow: 1;
}

/* ===== Tags ===== */
.tags-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: auto;
}

.tag {
  background-color: #f1f3ed;
  color: #555;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
}

.dark-tag {
  background-color: #717d5e;
  color: #ffffff;
}

/* ===== Contenido tarjeta ancha ===== */
.wide-content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.wide-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.wide-header .word-title {
  font-size: 1.8rem;
  margin-bottom: 0.25rem;
}

.wide-header .word-meaning {
  font-size: 1rem;
  margin-bottom: 0;
}

.example-quote {
  border-left: 3px solid var(--border-color, #e2e5dc);
  padding-left: 1rem;
  margin-bottom: 2rem;
}

.example-quote p {
  color: #666;
  font-style: italic;
  font-size: 0.95rem;
}

/* ===== Botón cargar más ===== */
.bottom-action {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.btn-load-more {
  background-color: #ffffff;
  border: 1px solid var(--border-color, #e2e5dc);
  color: #333;
  padding: 0.75rem 2rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-load-more:hover {
  background-color: #f9f9f9;
  border-color: var(--brand-dark);
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .frases-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .frases-grid {
    grid-template-columns: 1fr;
  }
  .wide-card {
    grid-column: span 1;
  }
}
</style>
