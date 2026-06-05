<!-- 
  DiccionarioView.vue
  
  Vista principal para mostrar un diccionario interactivo de palabras chilenas.
  Permite a los usuarios buscar, filtrar por categoría y explorar chilenismos
  con sus significados y ejemplos de uso.
  
  Componentes utilizados:
  - Search (lucide-vue-next): Icono para la búsqueda
  - Send (lucide-vue-next): Icono para sugerir nuevas palabras
  
  Funcionalidades:
  - Búsqueda de palabras
  - Filtrado por categorías (TODO, AMIGOS, TRABAJO, CALLE, COMIDA)
  - Grid responsive de tarjetas con palabras
  - Banner para sugerir nuevas palabras
-->
<template>
  <div class="diccionario-container">
    
    <!-- Encabezado con título principal -->
    <header class="view-header">
      <h1 class="title">DICCIONARIO DE CHILENISMOS</h1>
    </header>

    <!-- Barra de búsqueda -->
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

    <!-- Filtros por categoría -->
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

    <!-- Grid de tarjetas -->
    <div v-if="store.loading" class="loading-state">Cargando...</div>
    <div v-else class="words-grid">
      <article v-for="item in store.palabras" :key="item.id" class="word-card">
        <h2 class="word-title">{{ item.palabra }}</h2>
        <div class="section-label">SIGNIFICADO</div>
        <p class="word-meaning">{{ item.traduccion }}</p>
        <div v-if="item.ejemplo_uso" class="example-box">
          <div class="section-label">EJEMPLO</div>
          <p class="word-example">{{ item.ejemplo_uso }}</p>
        </div>
      </article>
    </div>

    <!-- Banner inferior con CTA para sugerir nuevas palabras -->
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
/* =====================================================
   ESTRUCTURA PRINCIPAL
   ===================================================== */

.diccionario-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 2rem;
}

/* =====================================================
   ENCABEZADO Y TÍTULO
   ===================================================== */

/* Título principal del diccionario */
.view-header .title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #111;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

/* =====================================================
   BARRA DE BÚSQUEDA
   ===================================================== */

.search-wrapper {
  background-color: #ffffff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  height: 54px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  width: 100%;
  max-width: 600px;
}

.search-icon {
  color: var(--text-muted);
  margin-right: 0.75rem;
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

/* =====================================================
   FILTROS POR CATEGORÍA
   ===================================================== */

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
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #e2e8d5;
}

.filter-btn.active {
  background-color: var(--brand-tag); 
  color: #a45a41; 
}

/* =====================================================
   GRID DE PALABRAS Y TARJETAS
   ===================================================== */

/* Layout de 3 columnas para las tarjetas de palabras */
.words-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* Tarjeta individual con información de una palabra */
.word-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

/* Nombre de la palabra -->
.word-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 1rem;
}

/* Etiqueta para secciones (SIGNIFICADO, EJEMPLO) */
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

/* Caja contenedora del ejemplo */
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

/* 
   *
   BANNER INFERIOR - CTA PARA SUGERIR PALABRAS
    *
    */

/* Banner con llamada a la acción para sugerir palabras nuevas */
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
  transition: opacity 0.2s;
  z-index: 1; 
}

.suggest-btn:hover {
  opacity: 0.9;
}

/* =====================================================
   DISEÑO RESPONSIVO
   ===================================================== */

/* Tablets: cambiar a 2 columnas */
@media (max-width: 1024px) {
  .words-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Móviles: cambiar a 1 columna */
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