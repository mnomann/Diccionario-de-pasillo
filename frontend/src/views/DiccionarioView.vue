<template>
  <div class="diccionario-container">
    <header class="view-header">
      <h1 class="title">DICCIONARIO DE CHILENISMOS</h1>
    </header>

    <div class="search-wrapper">
      <Search class="search-icon" :size="20" />
      <input
        type="text"
        v-model="textoBusqueda"
        placeholder="Buscar palabra..."
        class="search-input"
        @keyup.enter="buscar"
      />
    </div>

    <div class="filters-container">
      <button
        v-for="cat in store.categorias"
        :key="cat"
        :class="['filter-btn', { active: categoriaActiva === cat }]"
        @click="filtrar(cat)"
      >
        {{ cat }}
      </button>
    </div>

    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner" />
      <p>Cargando palabras...</p>
    </div>

    <TransitionGroup v-else name="card-enter" tag="div" class="words-grid">
      <article v-for="(item, idx) in store.palabras" :key="item.id" class="word-card" :style="{ '--card-delay': idx * 0.04 + 's' }">
        <h2 class="word-title">{{ item.palabra }}</h2>
        <div class="section-label">SIGNIFICADO</div>
        <p class="word-meaning">{{ item.traduccion }}</p>
        <div v-if="item.ejemplo_uso" class="example-box">
          <div class="section-label">EJEMPLO</div>
          <p class="word-example">{{ item.ejemplo_uso }}</p>
        </div>
      </article>
    </TransitionGroup>

    <div class="bottom-banner">
      <div class="banner-content">
        <h3>¿FALTA ALGO?</h3>
        <p>Ayúdanos a completar el diccionario con nuevas palabras.</p>
      </div>
      <button class="suggest-btn">
        <Send :size="18" class="send-icon" />
        SUGERIR PALABRA
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search, Send } from 'lucide-vue-next'
import { usePalabrasStore } from '../store/palabras'

const store = usePalabrasStore()

const categoriaActiva = ref('TODO')
const textoBusqueda = ref('')

onMounted(() => {
  store.fetchPalabras()
})

function filtrar(cat: string) {
  categoriaActiva.value = cat
  store.fetchPalabras({
    categoria: cat === 'TODO' ? undefined : cat.toLowerCase(),
    buscar: textoBusqueda.value || undefined,
  })
}

function buscar() {
  store.fetchPalabras({
    categoria: categoriaActiva.value === 'TODO' ? undefined : categoriaActiva.value.toLowerCase(),
    buscar: textoBusqueda.value || undefined,
  })
}
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

.diccionario-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 2rem;
  animation: viewFadeIn 0.5s ease both;
}

/* ===== Encabezado ===== */
.view-header {
  border-left: 6px solid var(--brand-dark);
  padding-left: 1.5rem;
}

.view-header .title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

/* ===== Búsqueda ===== */
.search-wrapper {
  background-color: #ffffff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 8px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  height: 54px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  width: 100%;
  max-width: 600px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-wrapper:focus-within {
  border-color: var(--brand-dark);
  box-shadow: 0 0 0 3px rgba(45, 51, 34, 0.08);
}

.search-icon {
  color: var(--text-muted);
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  height: 100%;
  font-size: 1rem;
  color: var(--text-main);
  outline: none;
}

/* ===== Filtros ===== */
.filters-container {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.filter-btn {
  background-color: #eef1e8;
  color: var(--text-muted);
  border: 1px solid transparent;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #e2e8d5;
  border-color: var(--border-color, #e2e5dc);
}

.filter-btn.active {
  background-color: var(--brand-tag);
  color: #a45a41;
  border-color: transparent;
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

/* ===== Grid de palabras ===== */
.words-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.word-card {
  background-color: #ffffff;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
  transition: box-shadow 0.25s ease, transform 0.2s ease, border-color 0.2s ease;
}

.word-card:hover {
  box-shadow: 0 6px 20px rgba(45, 51, 34, 0.08);
  transform: translateY(-2px);
  border-color: var(--brand-dark);
}

.word-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 1rem;
}

.section-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
}

.word-meaning {
  font-size: 0.95rem;
  color: #111;
  line-height: 1.4;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.example-box {
  background-color: var(--brand-card-inner);
  padding: 1rem;
  border-radius: 8px;
}

.word-example {
  font-size: 0.9rem;
  font-style: italic;
  color: #333;
  margin-top: 0.2rem;
}

/* ===== Banner inferior ===== */
.bottom-banner {
  background-color: #ccd4be;
  border-radius: 12px;
  padding: 2rem 3rem;
  margin-top: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.bottom-banner:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.banner-content h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 0.25rem;
}

.banner-content p {
  font-size: 0.95rem;
  color: #333;
}

.suggest-btn {
  background-color: #c4a495;
  color: #ffffff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: opacity 0.2s, box-shadow 0.2s;
  z-index: 1;
  flex-shrink: 0;
}

.suggest-btn:hover {
  opacity: 0.9;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .words-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .words-grid {
    grid-template-columns: 1fr;
  }
  .bottom-banner {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
}
</style>
