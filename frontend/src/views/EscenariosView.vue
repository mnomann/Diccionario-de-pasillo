<template>
  <div class="escenarios-container">
    
    <!-- Encabezado con borde lateral -->
    <header class="view-header">
      <h1 class="title">GUÍA DE ESCENARIOS SOCIALES</h1>
      <p class="subtitle">Navega situaciones cotidianas con calma. Explora interacciones comunes y descubre los significados ocultos tras el lenguaje figurado chileno.</p>
    </header>

    <!-- Grilla Principal de 3 Columnas -->
    <div class="escenarios-grid">
      
      <!-- Fila 1: Entrevista (Ancha) y Amigos (Normal) -->
      <article class="card wide-card gradient-profesional">
        <div class="card-badge">PROFESIONAL</div>
        <div class="profesional-content">
          <div class="tag-header">
            <Briefcase :size="16" />
            <span>ÁREA PROFESIONAL</span>
          </div>
          <h2>Entrevista de trabajo</h2>
          <p>Aprende a decodificar preguntas como "¿Cuál es tu pretensión de sueldo?" o el uso de modismos en entornos formales.</p>
          <a href="#" class="action-link">Comenzar práctica <ArrowRight :size="16" /></a>
        </div>
        <!-- El fondo de la persona se maneja por CSS o imagen absoluta en el futuro -->
      </article>

      <article class="card normal-card">
        <div class="image-placeholder dog-placeholder">
          <div class="icon-badge"><Utensils :size="14" /></div>
        </div>
        <div class="card-content">
          <h3>Junta con amigos</h3>
          <p>¿Qué significa cuando alguien dice "ya, po"? Navega el caos social de las reuniones grupales.</p>
        </div>
      </article>

      <!-- Fila 2: Panadería (Ancha) y Guía (Normal) -->
      <article class="card wide-card no-padding">
        <div class="image-placeholder bread-placeholder">
          <div class="scenario-title-overlay">
            <Store :size="18" />
            <h2>Escenario: En la Panadería</h2>
          </div>
        </div>
        
        <div class="chat-container">
          <!-- Mensaje Izquierda (Usuario) -->
          <div class="chat-row left">
            <div class="avatar user-avatar"><User :size="16" /></div>
            <div class="chat-bubble">
              "Hola vecino, ¿me da una hallulla calientita? ¡Ojalá que no esté dura como palo!"
            </div>
          </div>
          
          <!-- Mensaje Derecha (Vendedor) -->
          <div class="chat-row right">
            <div class="chat-bubble">
              "¡Al tiro jefe! Están recién salidas. Estas vuelan a esta hora."
            </div>
            <div class="avatar vendor-avatar"><Store :size="16" /></div>
          </div>

          <!-- Botones de Acción del Chat -->
          <div class="chat-actions">
            <button class="chat-btn"><Play :size="14" /> Escuchar Audio</button>
            <button class="chat-btn"><History :size="14" /> Ver Variaciones</button>
          </div>
        </div>
      </article>

      <article class="card normal-card interpretation-card">
        <div class="interp-header">
          <Lightbulb :size="16" />
          <span>GUÍA DE INTERPRETACIÓN</span>
        </div>
        
        <div class="interp-box">
          <div class="box-label">
            <ScanText :size="14" /> LITERAL VS. SOCIAL
          </div>
          <h4>"Vuelan a esta hora"</h4>
          <p>No significa que el pan tenga alas. Significa que se venden muy rápido.</p>
        </div>

        <div class="interp-box social-suggestion">
          <div class="box-label">
            <Info :size="14" /> SUGERENCIA SOCIAL
          </div>
          <h4>El uso de "Vecino/Jefe"</h4>
          <p>Son términos de cercanía casual en Chile. No implican una relación laboral.</p>
        </div>
      </article>

      <!-- Fila 3: Tarjetas pequeñas de utilidad -->
      <article class="card small-action-card">
        <div class="icon-wrapper"><Bookmark :size="20" /></div>
        <div>
          <h4>ESCENARIOS SUGERIDOS</h4>
          <p>Basados en tu historial</p>
        </div>
      </article>

      <article class="card small-action-card dashed-border">
        <div class="new-scenario-content">
          <h4>¿Tienes un escenario nuevo?</h4>
          <p>Ayúdanos a expandir la biblioteca.</p>
          <button class="btn-suggest">SUGERIR ESCENARIO</button>
        </div>
      </article>

      <article class="card small-action-card disabled-card">
        <div class="coming-soon-content">
          <PlusCircle :size="24" class="muted-icon" />
          <h4>PRÓXIMAMENTE</h4>
          <p>Realidad Aumentada</p>
        </div>
      </article>

    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { 
  Briefcase, Utensils, Store, User, Play, 
  History, Lightbulb, Bookmark, PlusCircle, 
  ArrowRight, Info, ScanText 
} from 'lucide-vue-next'
import { useEscenariosStore } from '../store/escenarios'

const store = useEscenariosStore()

onMounted(() => {
  store.fetchEscenarios()
})
</script>

<style scoped>
.escenarios-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding-bottom: 3rem;
}

/* Header con barra lateral */
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
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1rem;
  color: var(--text-main);
  max-width: 800px;
  line-height: 1.5;
}

/* Grilla de 3 columnas */
.escenarios-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* Base de Tarjetas */
.card {
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.wide-card {
  grid-column: span 2;
}

.normal-card {
  grid-column: span 1;
}

/* Tarjeta Profesional */
.gradient-profesional {
  background: linear-gradient(135deg, #f9fbf7 0%, #edf1e6 100%);
  padding: 2rem;
  justify-content: center;
}

.card-badge {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background-color: #e2e8d5;
  color: #555f44;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.profesional-content {
  max-width: 60%;
  z-index: 1;
}

.tag-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(255,255,255,0.8);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  width: fit-content;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin-bottom: 1rem;
}

.profesional-content h2 {
  font-size: 1.8rem;
  font-weight: 800;
  color: #111;
  margin-bottom: 0.75rem;
}

.profesional-content p {
  font-size: 0.95rem;
  color: #444;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.action-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #111;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.9rem;
}

/* Tarjeta Junta con Amigos */
.image-placeholder {
  height: 160px;
  background-color: #2c2c2c; 
  position: relative;
  border-radius: 8px;
  margin: 1rem 1rem 0 1rem;
}

.icon-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background-color: #ffffff;
  padding: 0.4rem;
  border-radius: 6px;
  display: flex;
}

.card-content {
  padding: 1.5rem;
}

.card-content h3 {
  font-size: 1.2rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.card-content p {
  font-size: 0.9rem;
  color: var(--text-main);
  line-height: 1.4;
}

.no-padding {
  padding: 0;
}

.bread-placeholder {
  margin: 0;
  border-radius: 0;
  height: 120px;
  background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.6)), #8b6d4f;
  display: flex;
  align-items: flex-end;
  padding: 1.5rem;
}

.scenario-title-overlay {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ffffff;
}

.scenario-title-overlay h2 {
  font-size: 1.4rem;
  font-weight: 700;
}

.chat-container {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.chat-row {
  display: flex;
  gap: 1rem;
  max-width: 80%;
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
.vendor-avatar { background-color: #555f44; color: #fff; }

.chat-bubble {
  background-color: #f4f5f1;
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #111;
  line-height: 1.4;
  border: 1px solid #ebece6;
}

.chat-row.left .chat-bubble { border-top-left-radius: 4px; }
.chat-row.right .chat-bubble { border-top-right-radius: 4px; }

.chat-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.chat-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #ffffff;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  color: #333;
}

/* Tarjeta Guía de Interpretación */
.interpretation-card {
  padding: 1.5rem;
}

.interp-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.75rem;
}

.interp-box {
  background-color: #f6f8f2;
  border-radius: 8px;
  padding: 1.2rem;
  margin-bottom: 1rem;
}

.social-suggestion {
  background-color: #eceee6;
}

.box-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.65rem;
  font-weight: 800;
  color: #666;
  margin-bottom: 0.5rem;
  letter-spacing: 0.05em;
}

.interp-box h4 {
  font-size: 0.95rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  color: #111;
}

.interp-box p {
  font-size: 0.85rem;
  color: #444;
  line-height: 1.4;
}

/* Tarjetas Pequeñas Inferiores */
.small-action-card {
  padding: 1.5rem;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  background-color: #f6f8f2;
}

.icon-wrapper {
  background-color: #e2e8d5;
  padding: 0.75rem;
  border-radius: 8px;
  color: var(--brand-dark);
}

.small-action-card h4 {
  font-size: 0.9rem;
  font-weight: 800;
  color: #111;
}

.small-action-card p {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.dashed-border {
  border: 2px dashed #ccd4be;
  background-color: #ffffff;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.btn-suggest {
  margin-top: 0.5rem;
  background-color: #e2e8d5;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--brand-dark);
  cursor: pointer;
}

.disabled-card {
  background-color: #eceef0;
  justify-content: center;
  text-align: center;
  border: none;
}

.coming-soon-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  opacity: 0.5;
}

.muted-icon {
  color: #999;
  margin-bottom: 0.25rem;
}

/* Responsividad */
@media (max-width: 1024px) {
  .escenarios-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .wide-card, .normal-card, .small-action-card {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .escenarios-grid {
    grid-template-columns: 1fr;
  }
  .chat-row { max-width: 95%; }
  .profesional-content { max-width: 100%; }
}
</style>