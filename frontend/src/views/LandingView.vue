<template>
  <div class="landing">
    <section class="hero-section" ref="heroRef">
      <div class="hero-bg" />
      <div class="hero-content">
        <div class="hero-text" :class="{ visible: heroVisible }">
          <p class="hero-badge">DESENREDA</p>
          <h1 class="hero-title">Guía del español chileno</h1>
          <p class="hero-desc">
            Traduce el lenguaje informal, la ironía y los modismos chilenos a un
            significado claro y directo.
          </p>
        </div>
        <div class="hero-scroll-hint" :class="{ visible: heroVisible }">
          <span>Descubre más</span>
          <ChevronDown :size="24" class="bounce" />
        </div>
      </div>
    </section>

    <section class="section" ref="queEsRef">
      <div class="section-inner" :class="{ visible: queEsVisible }">
        <span class="section-number">01</span>
        <h2 class="section-title">¿Qué es Desenreda?</h2>
        <p class="section-text">
          Es una herramienta digital que decodifica el <strong>lenguaje informal chileno</strong>,
          traduciendo ironías, sarcasmos, modismos y normas sociales implícitas en un
          lenguaje literal, estructurado y fácil de entender.
        </p>
        <div class="feature-grid">
          <div class="feature-item">
            <MessageSquareText :size="28" />
            <span>Traducción literal de frases</span>
          </div>
          <div class="feature-item">
            <BookOpen :size="28" />
            <span>Diccionario de modismos</span>
          </div>
          <div class="feature-item">
            <Map :size="28" />
            <span>Escenarios sociales contextualizados</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" ref="paraQuienRef">
      <div class="section-inner" :class="{ visible: paraQuienVisible }">
        <span class="section-number">02</span>
        <h2 class="section-title">¿A quién va dirigido?</h2>
        <div class="cards-row">
          <div class="persona-card">
            <div class="persona-icon">
              <Brain :size="32" />
            </div>
            <h3>Personas neurodivergentes</h3>
            <p>
              Personas con TEA, TDAH u otras condiciones que dificultan la
              interpretación de ironías, dobles sentidos y normas sociales implícitas.
            </p>
          </div>
          <div class="persona-card">
            <div class="persona-icon">
              <Globe :size="32" />
            </div>
            <h3>Extranjeros y nuevos hablantes</h3>
            <p>
              Quienes están aprendiendo español y se enfrentan al desafío del
              lenguaje coloquial chileno, lleno de modismos únicos.
            </p>
          </div>
          <div class="persona-card">
            <div class="persona-icon">
              <Heart :size="32" />
            </div>
            <h3>Cualquier persona</h3>
            <p>
              Todos los que quieran mejorar su comunicación, entender mejor a los
              demás o simplemente curiosear el fascinante mundo del habla chilena.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" ref="queHaceRef">
      <div class="section-inner" :class="{ visible: queHaceVisible }">
        <span class="section-number">03</span>
        <h2 class="section-title">¿Qué puedes hacer?</h2>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-content">
              <h3>Traducir frases</h3>
              <p>
                Ingresa cualquier frase o palabra chilena y obtén su significado
                literal, nivel de ironía y contexto de uso.
              </p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-content">
              <h3>Explorar el diccionario</h3>
              <p>
                Navega por un catálogo de modismos chilenos con ejemplos reales,
                organizados por categorías y contexto.
              </p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-content">
              <h3>Aprender con escenarios</h3>
              <p>
                Descubre cómo se usan estas expresiones en situaciones cotidianas
                como entrevistas laborales, reunionas familiares o carretes.
              </p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div class="step-content">
              <h3>Contribuir</h3>
              <p>
                Sugiere nuevas palabras o frases para ayudar a expandir la base
                de conocimiento y ayudar a más personas.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" ref="comoUsarRef">
      <div class="section-inner" :class="{ visible: comoUsarVisible }">
        <span class="section-number">04</span>
        <h2 class="section-title">¿Cómo se usa?</h2>
        <div class="usage-steps">
          <div class="usage-step">
            <div class="usage-icon">
              <Search :size="24" />
            </div>
            <div class="usage-text">
              <strong>1. Escribe</strong>
              <p>Ingresa una palabra o frase chilena en el buscador.</p>
            </div>
          </div>
          <div class="usage-arrow">
            <ArrowDown :size="20" />
          </div>
          <div class="usage-step">
            <div class="usage-icon">
              <Languages :size="24" />
            </div>
            <div class="usage-text">
              <strong>2. Traduce</strong>
              <p>Presiona "Traducir" y obtén el significado literal al instante.</p>
            </div>
          </div>
          <div class="usage-arrow">
            <ArrowDown :size="20" />
          </div>
          <div class="usage-step">
            <div class="usage-icon">
              <Lightbulb :size="24" />
            </div>
            <div class="usage-text">
              <strong>3. Aprende</strong>
              <p>Revisa el nivel de ironía, ejemplos de uso y el contexto social asociado.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section" ref="ctaRef">
      <div class="cta-inner" :class="{ visible: ctaVisible }">
        <h2 class="cta-title">¿Listo para desenredar el chileno?</h2>
        <p class="cta-text">
          Empieza a traducir cualquier frase y descubre el verdadero significado
          detrás de las palabras.
        </p>
        <router-link to="/traductor" class="cta-btn">
          <Languages :size="22" />
          Ir al Traductor
          <ArrowRight :size="22" />
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import {
  ChevronDown, MessageSquareText, BookOpen, Map,
  Brain, Globe, Heart, Search, Languages, Lightbulb,
  ArrowDown, ArrowRight
} from 'lucide-vue-next'

const heroRef = ref<HTMLElement | null>(null)
const queEsRef = ref<HTMLElement | null>(null)
const paraQuienRef = ref<HTMLElement | null>(null)
const queHaceRef = ref<HTMLElement | null>(null)
const comoUsarRef = ref<HTMLElement | null>(null)
const ctaRef = ref<HTMLElement | null>(null)

const heroVisible = ref(false)
const queEsVisible = ref(false)
const paraQuienVisible = ref(false)
const queHaceVisible = ref(false)
const comoUsarVisible = ref(false)
const ctaVisible = ref(false)

const observers: IntersectionObserver[] = []

function observar(el: HTMLElement | null, target: { value: boolean }, threshold = 0.2) {
  if (!el) return
  const obs = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        target.value = true
        obs.disconnect()
      }
    },
    { threshold }
  )
  obs.observe(el)
  observers.push(obs)
}

onMounted(() => {
  heroVisible.value = true
  observar(queEsRef.value, queEsVisible)
  observar(paraQuienRef.value, paraQuienVisible)
  observar(queHaceRef.value, queHaceVisible)
  observar(comoUsarRef.value, comoUsarVisible)
  observar(ctaRef.value, ctaVisible)
})

onUnmounted(() => {
  observers.forEach(o => o.disconnect())
})
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(8px); }
}

.landing {
  width: 100%;
}

/* ===== Hero ===== */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #e8ece0 0%, #d4dcc4 50%, #cdd5bf 100%);
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  max-width: 720px;
}

.hero-text {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.hero-text.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-badge {
  display: inline-block;
  background-color: var(--brand-dark);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  padding: 0.4rem 1rem;
  border-radius: 999px;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--brand-dark);
  line-height: 1.1;
  margin-bottom: 1rem;
}

.hero-desc {
  font-size: 1.2rem;
  color: #4a4a4a;
  line-height: 1.6;
  max-width: 540px;
  margin: 0 auto;
}

.hero-scroll-hint {
  margin-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 500;
  opacity: 0;
  transition: opacity 1s ease 1s;
}

.hero-scroll-hint.visible {
  opacity: 1;
}

.bounce {
  animation: bounce 1.5s ease infinite;
}

/* ===== Sections ===== */
.section {
  padding: 6rem 2rem;
  display: flex;
  justify-content: center;
}

.section-alt {
  background-color: #eef1e8;
}

.section-inner {
  max-width: 900px;
  width: 100%;
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.section-inner.visible {
  opacity: 1;
  transform: translateY(0);
}

.section-number {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
  display: block;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--brand-dark);
  margin-bottom: 1.5rem;
}

.section-text {
  font-size: 1.1rem;
  color: #4a4a4a;
  line-height: 1.7;
  margin-bottom: 2.5rem;
}

/* ===== Feature Grid ===== */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.feature-item {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--brand-dark);
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s, transform 0.2s;
}

.feature-item:hover {
  box-shadow: 0 4px 12px rgba(45, 51, 34, 0.06);
  transform: translateY(-2px);
}

.feature-item svg {
  color: var(--brand-note);
}

/* ===== Persona Cards ===== */
.cards-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.persona-card {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s, transform 0.2s;
}

.persona-card:hover {
  box-shadow: 0 6px 20px rgba(45, 51, 34, 0.08);
  transform: translateY(-3px);
}

.persona-icon {
  width: 56px;
  height: 56px;
  background-color: var(--brand-card-inner);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  color: var(--brand-note);
}

.persona-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin-bottom: 0.5rem;
}

.persona-card p {
  font-size: 0.9rem;
  color: #4a4a4a;
  line-height: 1.5;
}

/* ===== Steps ===== */
.steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s, transform 0.2s;
}

.step:hover {
  box-shadow: 0 4px 12px rgba(45, 51, 34, 0.06);
  transform: translateX(4px);
}

.step-num {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: var(--brand-dark);
  color: #fff;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--brand-dark);
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.95rem;
  color: #4a4a4a;
  line-height: 1.5;
}

/* ===== Usage Steps ===== */
.usage-steps {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.usage-step {
  display: flex;
  gap: 1rem;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s, transform 0.2s;
}

.usage-step:hover {
  box-shadow: 0 4px 12px rgba(45, 51, 34, 0.06);
  transform: scale(1.02);
}

.usage-icon {
  width: 48px;
  height: 48px;
  background-color: var(--brand-card-inner);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--brand-note);
}

.usage-text strong {
  display: block;
  font-size: 1rem;
  color: var(--brand-dark);
  margin-bottom: 0.15rem;
}

.usage-text p {
  font-size: 0.9rem;
  color: #4a4a4a;
}

.usage-arrow {
  color: var(--text-muted);
}

/* ===== CTA ===== */
.cta-section {
  padding: 6rem 2rem;
  display: flex;
  justify-content: center;
  text-align: center;
}

.cta-inner {
  max-width: 600px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.cta-inner.visible {
  opacity: 1;
  transform: translateY(0);
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--brand-dark);
  margin-bottom: 1rem;
}

.cta-text {
  font-size: 1.1rem;
  color: #4a4a4a;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background-color: var(--brand-dark);
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  padding: 1rem 2rem;
  border-radius: 999px;
  text-decoration: none;
  transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(45, 51, 34, 0.15);
}

.cta-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 51, 34, 0.2);
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }

  .hero-desc {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .cards-row {
    grid-template-columns: 1fr;
  }

  .section {
    padding: 4rem 1.5rem;
  }

  .step {
    flex-direction: column;
    align-items: flex-start;
  }

  .usage-step {
    flex-direction: column;
    text-align: center;
  }

  .cta-title {
    font-size: 1.8rem;
  }
}
</style>
