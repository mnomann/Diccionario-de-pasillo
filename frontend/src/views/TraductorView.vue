/**
 * TraductorView.vue
 * 
 * Componente principal para la traducción y explicación de modismos chilenos.
 * Permite a los usuarios introducir frases en español chileno para obtener
 * su significado literal, uso común, nivel de ironía y categorías asociadas.
 * 
 * Características:
 * - Barra de búsqueda para introducir frases
 * - Visualización de significado literal y uso común
 * - Indicador de nivel de ironía
 * - Sistema de etiquetas para categorización
 * - Acceso a escenarios sociales de uso
 */

<template>
  <!-- Contenedor principal del componente traductor -->
  <div class="traductor-container">
    
    <!-- Encabezado con título y subtítulo de la vista -->
    <header class="view-header">
      <h2 class="title">DESCIFRADOR DE CHILE</h2>
      <p class="subtitle">Introduce una frase para entender su contexto real.</p>
    </header>

    <!-- Barra de búsqueda y botón de traducción -->
    <div class="search-bar-container">
      <div class="search-input-wrapper">
        <!-- Campo de entrada para la frase a traducir -->
        <input class="search-input" type="text" placeholder="Ej: Estoy pato" />
      </div>
      <!-- Botón para activar la traducción -->
      <button class="translate-btn">
        <Languages :size="18" />
        TRADUCIR
      </button>
    </div>

    <!-- Layout principal con resultado y columna lateral de información -->
    <div class="results-layout">
      
      <!-- Tarjeta principal con la información de la frase -->
      <div class="main-card-white">
        <!-- Etiqueta indicando que es la frase original -->
        <span class="card-label">FRASE ORIGINAL</span>
        <!-- Texto de la frase a traducir -->
        <h1 class="phrase-text">"Estar pato"</h1>

        <!-- Sección de significado literal -->
        <div class="inner-box">
          <div class="box-header">
            <BookOpen :size="16" />
            <h3>SIGNIFICADO LITERAL</h3>
          </div>
          <p>Ser un pato (animal).</p>
        </div>

        <!-- Sección de uso común con nota informativa -->
        <div class="inner-box">
          <div class="box-header">
            <MessageSquare :size="16" />
            <h3>USO COMÚN</h3>
          </div>
          <p>No tener dinero; estar sin fondos financieros en este momento.</p>
          
          <!-- Nota oscura con información sobre seguridad de la expresión -->
          <div class="dark-note">
            <Info :size="18" class="note-icon" />
            <p>Nota: Es una expresión informal pero no es ofensiva. Segura para usar con amigos o familia.</p>
          </div>
        </div>
      </div>

      <!-- Columna lateral con información adicional sobre la frase -->
      <aside class="side-info-column">
        
        <!-- Tarjeta del nivel de ironía -->
        <div class="small-card">
          <h3 class="card-title">NIVEL DE IRONÍA</h3>
          <div class="irony-row">
            <span>Bajo</span>
            <!-- Indicador visual de barras para el nivel de ironía -->
            <div class="irony-bars">
              <div class="bar active"></div>
              <div class="bar inactive"></div>
              <div class="bar inactive"></div>
            </div>
          </div>
        </div>

        <!-- Tarjeta de etiquetas categóricas -->
        <div class="small-card">
          <h3 class="card-title">ETIQUETAS</h3>
          <div class="tags-container">
            <span class="tag">Informal</span>
            <span class="tag">Finanzas</span>
            <span class="tag">Amistad</span>
          </div>
        </div>

        <!-- Tarjeta interactiva para acceder a escenarios sociales -->
        <div class="small-card link-card">
          <div class="link-content">
            <h3 class="card-title">APRENDER ESCENARIOS SOCIALES</h3>
            <p>Ver ejemplos de cómo usar esta frase en la vida real.</p>
          </div>
          <ArrowRight :size="20" />
        </div>

      </aside>

    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Importación de iconos de lucide-vue-next
 * - Languages: Icono de traducción para el botón
 * - BookOpen: Icono de significado literal
 * - MessageSquare: Icono de uso común
 * - Info: Icono de información en notas
 * - ArrowRight: Icono de enlace/navegación en la tarjeta de escenarios
 */
import { Languages, BookOpen, MessageSquare, Info, ArrowRight } from 'lucide-vue-next'

/**
 * TraductorView - Componente de vista para traducción de modismos chilenos
 * 
 * Utiliza composition API de Vue 3 con TypeScript.
 * 
 * Funcionalidades futuras a implementar:
 * - Reactive state para guardar la frase introducida y resultados
 * - Métodos para enviar peticiones a la API de traducción
 * - Validación del input del usuario
 * - Manejo de errores en las peticiones HTTP
 */
</script>

<style scoped>
/**
 * ESTILOS DEL COMPONENTE TraductorView
 * 
 * Arquitectura de estilos:
 * - Contenedor principal y layout
 * - Encabezado y títulos
 * - Barra de búsqueda
 * - Tarjeta principal de resultados
 * - Tarjetas secundarias de información
 * - Utilidades y estados
 */

/* ===== CONTENEDOR PRINCIPAL ===== */

/**
 * .traductor-container
 * Contenedor principal que limita el ancho máximo y organiza
 * los elementos en columna con espaciado uniforme
 */
.traductor-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ===== ENCABEZADO Y TÍTULOS ===== */

/**
 * .view-header .title
 * Título principal del componente traductor
 * Tamaño grande y peso máximo para destacar
 */
.view-header .title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
}

/**
 * .view-header .subtitle
 * Subtítulo descriptivo bajo el título
 * Proporciona instrucciones al usuario
 */
.view-header .subtitle {
  font-size: 1rem;
  color: var(--text-main);
  margin-top: 0.25rem;
}

/* ===== BARRA DE BÚSQUEDA ===== */

/**
 * .search-bar-container
 * Contenedor de la barra de búsqueda con altura fija
 * Flexbox horizontal con fondo personalizado
 */
.search-bar-container {
  width: 100%;
  height: 60px;
  background-color: #E8EAE3;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
}

/**
 * .search-input-wrapper
 * Envoltorio para el input de búsqueda
 * Fondo diferente al contenedor y bordes redondeados
 */
.search-input-wrapper {
  flex: 1;
  height: 44px;
  background-color: #CCCFB2;
  border-radius: 999px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
}

/**
 * .search-input
 * Campo de entrada para la frase a traducir
 * Sin bordes ni estilos por defecto, solo texto
 */
.search-input {
  width: 100%;
  font-size: 1rem;
  color: #111;
  font-weight: 500;
  background: none;
  border: none;
  outline: none;
}

/**
 * .search-input::placeholder
 * Estilo del texto de placeholder en el input
 */
.search-input::placeholder {
  color: #888;
}

/**
 * .translate-btn
 * Botón de traducción con iconografía
 * Altura fija para alinearse con el wrapper del input
 */
.translate-btn {
  height: 44px;
  background-color: #CCCFB2;
  color: var(--brand-dark);
  border: none;
  padding: 0 1.5rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}

/**
 * .translate-btn:hover
 * Estado hover del botón de traducción
 * Reduce opacidad para feedback visual
 */
.translate-btn:hover {
  opacity: 0.8;
}

/* ===== LAYOUT DE RESULTADOS ===== */

/**
 * .results-layout
 * Layout principal con dos columnas:
 * - Columna izquierda: tarjeta principal (2.5 partes)
 * - Columna derecha: información adicional (1 parte)
 */
.results-layout {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

/* ===== TARJETA PRINCIPAL ===== */

/**
 * .main-card-white
 * Tarjeta principal con fondo blanco
 * Contiene frase, significado literal y uso común
 */
.main-card-white {
  flex: 2.5;
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

/**
 * .card-label
 * Etiqueta pequeña y mayúscula sobre contenido
 * Usado para "FRASE ORIGINAL", "SIGNIFICADO LITERAL", etc.
 */
.card-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
}

/**
 * .phrase-text
 * Texto grande de la frase a traducir
 * Destaca el contenido principal de la tarjeta
 */
.phrase-text {
  font-size: 2.2rem;
  font-weight: 800;
  color: #111;
  margin: 0.5rem 0 2rem 0;
}

/**
 * .inner-box
 * Caja interna para secciones de información
 * Fondo diferente al de la tarjeta padre
 */
.inner-box {
  background-color: var(--brand-card-inner);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

/**
 * .box-header
 * Encabezado de las cajas internas
 * Contiene icono y título de la sección
 */
.box-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

/**
 * .box-header h3
 * Título del encabezado de caja
 * Pequeño, en mayúscula y con espaciado entre letras
 */
.box-header h3 {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

/**
 * .inner-box p
 * Párrafos dentro de las cajas internas
 * Tamaño estándar con peso medio
 */
.inner-box p {
  font-size: 1rem;
  font-weight: 500;
  color: #111;
}

/**
 * .dark-note
 * Nota oscura/destacada con información importante
 * Usada para advertencias o aclaraciones
 */
.dark-note {
  background-color: var(--brand-note);
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

/**
 * .dark-note p, .note-icon
 * Texto e iconos dentro de la nota oscura
 * Texto blanco para contraste con fondo oscuro
 */
.dark-note p, .note-icon {
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1.4;
}

/* ===== COLUMNA LATERAL DE INFORMACIÓN ===== */

/**
 * .side-info-column
 * Columna derecha con tarjetas de información adicional
 * Distribuye las tarjetas verticalmente
 */
.side-info-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/**
 * .small-card
 * Tarjeta pequeña de información
 * Fondo claro para diferenciarse de la tarjeta principal
 */
.small-card {
  background-color: #f7f9f4;
  border-radius: 12px;
  padding: 1.5rem;
}

/**
 * .card-title
 * Título de las tarjetas pequeñas
 * Consistente con otros títulos de sección
 */
.card-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

/* ===== NIVEL DE IRONÍA ===== */

/**
 * .irony-row
 * Fila que contiene el nivel de ironía y las barras indicadoras
 */
.irony-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

/**
 * .irony-bars
 * Contenedor de las barras indicadoras del nivel de ironía
 * Tres barras que se rellenan según el nivel
 */
.irony-bars {
  display: flex;
  gap: 4px;
}

/**
 * .bar
 * Barra individual del indicador de ironía
 * Puede ser activa (rellena) o inactiva (vacía)
 */
.bar {
  width: 20px;
  height: 6px;
  border-radius: 99px;
}

/**
 * .bar.active / .bar.inactive
 * Estados de las barras:
 * - active: color verde (#6da34d)
 * - inactive: color gris claro (#e2e8d5)
 */
.bar.active { background-color: #6da34d; }
.bar.inactive { background-color: #e2e8d5; }

/* ===== ETIQUETAS (TAGS) ===== */

/**
 * .tags-container
 * Contenedor flexible para etiquetas
 * Distribuye las etiquetas en filas con espaciado
 */
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

/**
 * .tag
 * Etiqueta individual de categorización
 * Fondo personalizado y color de texto distintivo
 */
.tag {
  background-color: var(--brand-tag);
  color: #a45a41; 
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
}

/**
 * .link-card
 * Tarjeta interactiva con enlace a escenarios sociales
 * Fondo diferente y layout para mostrar contenido + ícono de flecha
 * Incluye sombra para profundidad y cursor pointer para indicar interactividad
 */
.link-card {
  background-color: #E2E3DD;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

/**
 * .link-content p
 * Párrafo descriptivo dentro de la tarjeta de enlace
 * Tamaño pequeño y color atenuado
 */
.link-content p {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}
</style>