<template>
  <div class="frases-container">
    
    <!-- Encabezado y Botones de Acción -->
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

    <!-- Grilla de Tarjetas -->
    <div v-if="store.loading" class="loading-state">Cargando...</div>
    <div v-else class="frases-grid">
      <article 
        v-for="frase in store.frases" 
        :key="frase.id" 
        :class="['frase-card', frase.type === 'wide' ? 'wide-card' : 'normal-card']"
      >
        
        <template v-if="frase.type === 'normal'">
          <div class="card-image-placeholder">
            <span>Ilustración: {{ frase.word }}</span>
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
    </div>

    <!-- Botón Inferior -->
    <div class="bottom-action">
      <button class="btn-load-more">Cargar más frases</button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Filter, Plus, Volume2 } from 'lucide-vue-next'
import { useFrasesStore } from '../store/frases'

const store = useFrasesStore()

onMounted(() => {
  store.fetchFrases()
})
</script>

<style scoped>
.frases-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-bottom: 3rem;
}

/* Header y botones */
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
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

.btn-filter, .btn-new {
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
  border: 1px solid #ccc;
  color: #333;
}

.btn-filter:hover {
  background-color: rgba(0,0,0,0.05);
}

.btn-new {
  background-color: var(--brand-dark);
  border: 1px solid var(--brand-dark);
  color: #fff;
}

.btn-new:hover {
  opacity: 0.9;
}

/* Grilla (4 columnas) */
.frases-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

/* Tarjetas */
.frase-card {
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #eef0e8;
  display: flex;
  flex-direction: column;
}

.wide-card {
  grid-column: span 2;
  padding: 1.5rem;
  justify-content: center;
  background-color: #ffffff;
  /* Simulación sutil de la marca de agua del diseño */
  background-image: radial-gradient(circle at 70% 50%, #f7f9f4 0%, transparent 40%);
}

.normal-card {
  grid-column: span 1;
}

/* Imagen superior (Placeholder para tarjeta normal) */
.card-image-placeholder {
  height: 140px;
  background-color: #f6e6cd; /* Color crema genérico del fondo de las ilustraciones */
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8c7d6b;
  font-size: 0.8rem;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

/* Contenido tarjeta normal */
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
}

.word-meaning {
  font-size: 0.9rem;
  color: var(--text-main);
  line-height: 1.4;
  margin-bottom: 1rem;
  flex-grow: 1;
}

/* Etiquetas */
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

/* Contenido especial para tarjeta ancha */
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
  border-left: 3px solid #ccc;
  padding-left: 1rem;
  margin-bottom: 2rem;
}

.example-quote p {
  color: #666;
  font-style: italic;
  font-size: 0.95rem;
}

/* Botón cargar más */
.bottom-action {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.btn-load-more {
  background-color: #ffffff;
  border: 1px solid #ccc;
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
  border-color: #999;
}

/* Responsividad */
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