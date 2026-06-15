<template>
  <div class="escenarios-container">
    
    <header class="view-header">
      <h1 class="title">GUÍA DE ESCENARIOS SOCIALES</h1>
      <p class="subtitle">Explora situaciones cotidianas separadas por contexto. Toca una categoría para ver sus conversaciones y traducciones.</p>
    </header>

    <div class="categories-wrapper">
      
      <section v-for="categoria in categorias" :key="categoria.id" class="category-section">
        
        <button 
          class="category-toggle-btn" 
          @click="toggleCategoria(categoria.id)"
          :aria-expanded="categoriasAbiertas.includes(categoria.id)"
        >
          <div class="cat-title-left">
            <component :is="categoria.icono" :size="24" class="cat-icon" />
            <h2 class="category-name">{{ categoria.nombre }}</h2>
          </div>
          
          <ChevronUp v-if="categoriasAbiertas.includes(categoria.id)" :size="20" class="toggle-icon" />
          <ChevronDown v-else :size="20" class="toggle-icon" />
        </button>

        <div class="scenarios-list" v-show="categoriasAbiertas.includes(categoria.id)">
          
          <article v-for="escenario in categoria.escenarios" :key="escenario.id" class="scenario-card">
            
            <div class="scenario-image-header" :class="escenario.claseFondo">
              <div class="header-overlay">
                <h3>Escenario: {{ escenario.titulo }}</h3>
              </div>
            </div>

            <div class="scenario-body">
              
              <div class="chat-column">
                <div 
                  v-for="(mensaje, index) in escenario.chat" 
                  :key="index"
                  :class="['chat-row', mensaje.emisor === 'usuario' ? 'left' : 'right']"
                >
                  <div v-if="mensaje.emisor === 'usuario'" class="avatar user-avatar">
                    <User :size="16" />
                  </div>
                  
                  <div class="chat-bubble">
                    {{ mensaje.texto }}
                  </div>
                  
                  <div v-if="mensaje.emisor === 'otro'" class="avatar vendor-avatar">
                    <component :is="escenario.iconoOtro" :size="16" />
                  </div>
                </div>
              </div>

              <aside class="translation-column">
                <div class="interp-box">
                  <div class="box-label">
                    <Lightbulb :size="14" /> TRADUCCIÓN LITERAL VS SOCIAL
                  </div>
                  <h4>Literalmente sonaría a:</h4>
                  <p class="literal-text">"{{ escenario.traduccion.literal }}"</p>
                  
                  <h4 class="mt-3">Pero en realidad significa:</h4>
                  <p class="real-text">"{{ escenario.traduccion.real }}"</p>
                </div>

                <div class="interp-box social-note" v-if="escenario.traduccion.nota">
                  <div class="box-label">
                    <Info :size="14" /> NOTA DE CONTEXTO
                  </div>
                  <p>{{ escenario.traduccion.nota }}</p>
                </div>
              </aside>

            </div>
          </article>

        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// Importamos ChevronUp y ChevronDown para las flechitas
import { Store, User, Users, Lightbulb, Info, Utensils, ChevronDown, ChevronUp } from 'lucide-vue-next'

// Estado para controlar qué categorías están abiertas
// Aquí le decimos que por defecto el ID 'comercio' inicie abierto
const categoriasAbiertas = ref<string[]>(['comercio'])

// Función para abrir/cerrar categorías
const toggleCategoria = (id: string) => {
  const index = categoriasAbiertas.value.indexOf(id)
  if (index === -1) {
    // Si no está en la lista, la agregamos (abrimos)
    categoriasAbiertas.value.push(id)
  } else {
    // Si ya está en la lista, la sacamos (cerramos)
    categoriasAbiertas.value.splice(index, 1)
  }
}

// Datos de las categorías
const categorias = [
  {
    id: 'comercio',
    nombre: 'Comercio y Servicios',
    icono: Store,
    escenarios: [
      {
        id: 1,
        titulo: 'En la Panadería',
        claseFondo: 'bg-panaderia',
        iconoOtro: Store,
        chat: [
          { emisor: 'usuario', texto: '"Hola vecino, ¿me da una hallulla calientita? ¡Ojalá que no esté dura como palo!"' },
          { emisor: 'otro', texto: '"¡Al tiro jefe! Están recién salidas. Estas vuelan a esta hora."' }
        ],
        traduccion: {
          literal: 'Hola persona que vive al lado. Ojalá el pan no sea un trozo de madera. / ¡Inmediatamente jefe de la empresa! Estos panes tienen alas y vuelan.',
          real: 'Hola vendedor. Ojalá el pan esté fresco. / ¡Enseguida señor! Están recién horneados. Se venden muy rápido a esta hora.',
          nota: 'Llamar "vecino" o "jefe" al vendedor es una muestra de cordialidad casual, no implica que vivan cerca ni que haya un contrato de trabajo.'
        }
      }
    ]
  },
  {
    id: 'amigos',
    nombre: 'Juntas y Amigos',
    icono: Users,
    escenarios: [
      {
        id: 2,
        titulo: 'Llegando tarde a la junta',
        claseFondo: 'bg-amigos',
        iconoOtro: Utensils,
        chat: [
          { emisor: 'usuario', texto: '"Oye, voy un poco atrasado, me pilló un taco infernal."' },
          { emisor: 'otro', texto: '"Ya po, apúrate que estamos todos patos y tú traes las lucas."' }
        ],
        traduccion: {
          literal: 'Me atrapó un zapato de mujer del infierno. / Apresúrate que somos aves acuáticas y tú traes a un hombre llamado Lucas.',
          real: 'Voy retrasado por culpa de un tráfico vehicular muy denso. / Apresúrate que no tenemos dinero y tú traes el efectivo para comprar.',
          nota: '"Taco" significa embotellamiento. "Estar pato" es estar sin dinero. "Lucas" se refiere a los billetes de mil pesos.'
        }
      }
    ]
  }
]
</script>

<style scoped>
.escenarios-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-bottom: 3rem;
}

/* Encabezado */
.view-header {
  border-left: 6px solid var(--brand-dark);
  padding-left: 1.5rem;
  margin-bottom: 1rem;
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

/* --- BOTÓN DESPLEGABLE DE CATEGORÍA --- */
.category-section {
  margin-bottom: 1.5rem;
}

.category-toggle-btn {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border: 1px solid var(--border-color);
  padding: 1.2rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.01);
}

.category-toggle-btn:hover {
  background-color: #fcfcfc;
  border-color: #d1dbbd; /* Ilumina el borde con tu verde claro al pasar el mouse */
}

/* Si la categoría está abierta, le damos un estilo sutilmente diferente al botón */
.category-toggle-btn[aria-expanded="true"] {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom: 2px solid var(--brand-input);
  background-color: #fbfcf9;
}

.cat-title-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.category-name {
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--brand-dark);
  margin: 0;
}

.cat-icon {
  color: #a45a41;
}

.toggle-icon {
  color: var(--text-muted);
}

/* --- LISTA DE ESCENARIOS --- */
.scenarios-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  /* El contenido se "adhiere" al botón de arriba */
  background-color: transparent;
  padding-top: 1.5rem; 
}

/* Tarjeta del Escenario */
.scenario-card {
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  overflow: hidden;
}

/* Imagen de Cabecera */
.scenario-image-header {
  height: 120px;
  display: flex;
  align-items: flex-end;
  padding: 1.5rem;
}

.bg-panaderia {
  background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), #8b6d4f;
}

.bg-amigos {
  background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.7)), #4f738b;
}

.header-overlay h3 {
  color: #ffffff;
  font-size: 1.4rem;
  font-weight: 800;
}

/* Cuerpo: Chat + Traducción */
.scenario-body {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 2rem;
  padding: 1.5rem;
}

/* Columna Chat */
.chat-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chat-row {
  display: flex;
  gap: 1rem;
  max-width: 90%;
}

.chat-row.left { align-self: flex-start; }
.chat-row.right { align-self: flex-end; justify-content: flex-end; }

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar { background-color: #e5e7eb; color: #555; }
.vendor-avatar { background-color: var(--brand-dark); color: #fff; }

.chat-bubble {
  background-color: var(--brand-card-inner);
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #111;
  line-height: 1.4;
}

.chat-row.left .chat-bubble { border-top-left-radius: 4px; }
.chat-row.right .chat-bubble { border-top-right-radius: 4px; background-color: #f4f5f1; border: 1px solid #ebece6; }

/* Columna Traducción */
.translation-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.interp-box {
  background-color: #fdfdfb;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.2rem;
}

.social-note {
  background-color: var(--brand-sidebar);
  border: none;
}

.social-note p {
  color: var(--brand-dark);
}

.box-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--text-muted);
  margin-bottom: 1rem;
  letter-spacing: 0.05em;
}

.social-note .box-label {
  color: var(--brand-dark);
}

.interp-box h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 0.25rem;
}

.mt-3 {
  margin-top: 1rem;
}

.literal-text {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.real-text {
  font-size: 0.95rem;
  color: #111;
  font-weight: 500;
}

.interp-box p {
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Responsividad */
@media (max-width: 850px) {
  .scenario-body {
    grid-template-columns: 1fr;
  }
  .chat-row { max-width: 100%; }
}
</style>