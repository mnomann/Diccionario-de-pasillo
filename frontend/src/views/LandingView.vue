<template>
  <div class="landing">
    <div class="noise-overlay" />
    <div class="progress-bar" ref="progressBar" />

    <!-- SLIDE 1: Hero -->
    <section class="slide" id="slide-1">
      <div class="slide-bg" />
      <div class="slide-blob slide-blob--1" />
      <div class="slide-blob slide-blob--2" />
      <div class="slide-content" ref="heroRef">
        <span class="slide-badge">DESENREDA</span>
        <h1>Guía del español chileno</h1>
        <p class="slide-sub">
          Traduce el lenguaje informal, la ironía y los modismos chilenos a un
          significado claro y directo.
        </p>
        <div class="scroll-hint">
          <span>Desliza para conocer más</span>
          <ChevronDown :size="24" class="bounce" />
        </div>
      </div>
    </section>

    <!-- SLIDE 2: ¿Qué es? -->
    <section class="slide slide--light" id="slide-2" ref="queEsRef">
      <div class="slide-content slide-content--left" :class="{ visible: queEsVisible }">
        <span class="section-num">01</span>
        <h2>¿Qué es Desenreda?</h2>
        <p class="section-desc">
          Es una herramienta digital que decodifica el <strong>lenguaje informal chileno</strong>,
          traduciendo ironías, sarcasmos, modismos y normas sociales implícitas en un
          lenguaje literal, estructurado y fácil de entender.
        </p>
        <div class="feature-grid">
          <div class="feature-item" style="--d: 0.1s">
            <div class="feature-icon"><MessageSquareText :size="24" /></div>
            <span>Traducción literal de frases</span>
          </div>
          <div class="feature-item" style="--d: 0.25s">
            <div class="feature-icon"><BookOpen :size="24" /></div>
            <span>Diccionario de modismos</span>
          </div>
          <div class="feature-item" style="--d: 0.4s">
            <div class="feature-icon"><Map :size="24" /></div>
            <span>Escenarios sociales contextualizados</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 3: ¿A quién va dirigido? -->
    <section class="slide" id="slide-3" ref="paraQuienRef">
      <div class="slide-bg" />
      <div class="slide-blob slide-blob--3" />
      <div class="slide-content" :class="{ visible: paraQuienVisible }">
        <span class="section-num section-num--light">02</span>
        <h2 class="slide-title--light">¿A quién va dirigido?</h2>
        <div class="cards-row">
          <div class="persona-card" style="--d: 0.1s">
            <div class="persona-accent" />
            <div class="persona-icon"><Brain :size="26" /></div>
            <h3>Personas neurodivergentes</h3>
            <p>Personas con TEA, TDAH u otras condiciones que dificultan la interpretación de ironías, dobles sentidos y normas sociales implícitas.</p>
          </div>
          <div class="persona-card" style="--d: 0.3s">
            <div class="persona-accent" />
            <div class="persona-icon"><Globe :size="26" /></div>
            <h3>Extranjeros y nuevos hablantes</h3>
            <p>Quienes están aprendiendo español y se enfrentan al desafío del lenguaje coloquial chileno, lleno de modismos únicos.</p>
          </div>
          <div class="persona-card" style="--d: 0.5s">
            <div class="persona-accent" />
            <div class="persona-icon"><Heart :size="26" /></div>
            <h3>Cualquier persona</h3>
            <p>Todos los que quieran mejorar su comunicación, entender mejor a los demás o simplemente curiosear el fascinante mundo del habla chilena.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4: ¿Qué puedes hacer? -->
    <section class="slide slide--light" id="slide-4" ref="queHaceRef">
      <div class="slide-content slide-content--left" :class="{ visible: queHaceVisible }">
        <span class="section-num">03</span>
        <h2>¿Qué puedes hacer?</h2>
        <div class="steps">
          <div class="step" style="--d: 0.1s">
            <div class="step-num">1</div>
            <div class="step-content">
              <h3>Traducir frases</h3>
              <p>Ingresa cualquier frase o palabra chilena y obtén su significado literal, nivel de ironía y contexto de uso.</p>
            </div>
          </div>
          <div class="step" style="--d: 0.25s">
            <div class="step-num">2</div>
            <div class="step-content">
              <h3>Explorar el diccionario</h3>
              <p>Navega por un catálogo de modismos chilenos con ejemplos reales, organizados por categorías y contexto.</p>
            </div>
          </div>
          <div class="step" style="--d: 0.4s">
            <div class="step-num">3</div>
            <div class="step-content">
              <h3>Aprender con escenarios</h3>
              <p>Descubre cómo se usan estas expresiones en situaciones cotidianas como entrevistas laborales, reuniones familiares o carretes.</p>
            </div>
          </div>
          <div class="step" style="--d: 0.55s">
            <div class="step-num">4</div>
            <div class="step-content">
              <h3>Contribuir</h3>
              <p>Sugiere nuevas palabras o frases para ayudar a expandir la base de conocimiento y ayudar a más personas.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 5: ¿Cómo se usa? -->
    <section class="slide" id="slide-5" ref="comoUsarRef">
      <div class="slide-bg slide-bg--alt" />
      <div class="slide-blob slide-blob--2" />
      <div class="slide-content" :class="{ visible: comoUsarVisible }">
        <span class="section-num section-num--light">04</span>
        <h2 class="slide-title--light">¿Cómo se usa?</h2>
        <div class="usage-steps">
          <div class="usage-step" style="--d: 0.1s">
            <div class="usage-icon"><Search :size="20" /></div>
            <div class="usage-text"><strong>1. Escribe</strong><p>Ingresa una palabra o frase chilena en el buscador.</p></div>
          </div>
          <div class="usage-arrow" style="--d: 0.25s"><ArrowDown :size="18" /></div>
          <div class="usage-step" style="--d: 0.35s">
            <div class="usage-icon"><Languages :size="20" /></div>
            <div class="usage-text"><strong>2. Traduce</strong><p>Presiona "Traducir" y obtén el significado literal al instante.</p></div>
          </div>
          <div class="usage-arrow" style="--d: 0.5s"><ArrowDown :size="18" /></div>
          <div class="usage-step" style="--d: 0.6s">
            <div class="usage-icon"><Lightbulb :size="20" /></div>
            <div class="usage-text"><strong>3. Aprende</strong><p>Revisa el nivel de ironía, ejemplos de uso y el contexto social asociado.</p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 6: CTA -->
    <section class="slide" id="slide-cta" ref="ctaRef">
      <div class="slide-bg slide-bg--cta" />
      <div class="slide-content cta-content" :class="{ visible: ctaVisible }">
        <h2>¿Listo para desenredar el chileno?</h2>
        <p>Empieza a traducir cualquier frase y descubre el verdadero significado detrás de las palabras.</p>
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

const queEsRef = ref<HTMLElement | null>(null)
const paraQuienRef = ref<HTMLElement | null>(null)
const queHaceRef = ref<HTMLElement | null>(null)
const comoUsarRef = ref<HTMLElement | null>(null)
const ctaRef = ref<HTMLElement | null>(null)
const heroRef = ref<HTMLElement | null>(null)

const queEsVisible = ref(false)
const paraQuienVisible = ref(false)
const queHaceVisible = ref(false)
const comoUsarVisible = ref(false)
const ctaVisible = ref(false)

const progressBar = ref<HTMLElement | null>(null)

const observers: IntersectionObserver[] = []

function observar(el: HTMLElement | null, target: { value: boolean }, threshold = 0.3) {
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

function onScroll() {
  if (progressBar.value) {
    const el = document.querySelector('.landing')
    if (!el) return
    const total = el.scrollHeight - el.clientHeight
    const pct = total > 0 ? (el.scrollTop / total) * 100 : 0
    progressBar.value.style.transform = `scaleX(${pct / 100})`
  }
}

onMounted(() => {
  observar(queEsRef.value, queEsVisible)
  observar(paraQuienRef.value, paraQuienVisible)
  observar(queHaceRef.value, queHaceVisible)
  observar(comoUsarRef.value, comoUsarVisible)
  observar(ctaRef.value, ctaVisible, 0.3)
  const el = document.querySelector('.landing')
  if (el) el.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  observers.forEach(o => o.disconnect())
  const el = document.querySelector('.landing')
  if (el) el.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
* { margin: 0; padding: 0; box-sizing: border-box; }

/* ===== Scroll container ===== */
.landing {
  height: 100vh;
  overflow-y: scroll;
  overflow-x: hidden;
  scroll-behavior: smooth;
  background: #2d3322;
}

/* ===== Fixed ===== */
.noise-overlay {
  position: fixed; inset: 0;
  z-index: 9999; pointer-events: none;
  opacity: 0.012;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat; background-size: 256px 256px;
}

.progress-bar {
  position: fixed; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #8a9f70, #c2d4a4);
  transform-origin: left; transform: scaleX(0);
  z-index: 10000; will-change: transform;
}

/* ===== Sticky slides ===== */
.slide {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* ===== Dark slides (hero) ===== */
.slide {
  background: linear-gradient(135deg, #3a4a32 0%, #5a7050 40%, #4a5a3a 100%);
}

.slide--light {
  background: #f4f6ed;
}

#slide-2, #slide-4 { background: #f4f6ed; }
#slide-3 { background: linear-gradient(135deg, #2d3a28 0%, #4a6040 50%, #3a5030 100%); }
#slide-5 { background: linear-gradient(135deg, #3a4530 0%, #556a48 50%, #4a5a3a 100%); }
#slide-cta { background: linear-gradient(135deg, #2d3322 0%, #4a5a3a 60%, #3a4a32 100%); }

/* Blobs */
.slide-blob {
  position: absolute; border-radius: 50%; pointer-events: none;
  animation: blobFloat 20s ease-in-out infinite;
}

.slide-blob--1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
  top: -150px; right: -100px;
}

.slide-blob--2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
  bottom: -120px; left: -80px;
  animation-delay: -7s;
}

.slide-blob--3 {
  width: 350px; height: 350px;
  background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
  top: 10%; right: 10%;
  animation-delay: -14s;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%      { transform: translate(40px, -40px) scale(1.08); }
  66%      { transform: translate(-30px, 30px) scale(0.92); }
}

/* ===== Slide content ===== */
.slide-content {
  position: relative; z-index: 1;
  text-align: center; padding: 2rem;
  max-width: 900px; width: 100%;
  color: #fff;
}

.slide-content--left {
  text-align: left;
}

/* ===== Animations on visible ===== */
.slide-content {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.slide-content.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Override: first slide always visible */
#slide-1 .slide-content {
  opacity: 1;
  transform: none;
}

/* ===== Hero typography ===== */
.slide h1 {
  font-size: 3.5rem; font-weight: 800;
  line-height: 1.1; margin-bottom: 1rem;
  text-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

.slide h2 {
  font-size: 2.5rem; font-weight: 800;
  line-height: 1.2; margin-bottom: 1.5rem;
}

.slide--light h2 {
  color: #2d3322;
}

.slide-title--light {
  color: #fff !important;
}

.slide-sub {
  font-size: 1.15rem; line-height: 1.6;
  max-width: 540px; margin: 0 auto;
  opacity: 0.9; text-shadow: 0 1px 8px rgba(0,0,0,0.25);
}

.slide-badge {
  display: inline-block;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(6px);
  color: #fff; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.15em; padding: 0.4rem 1rem;
  border-radius: 999px; margin-bottom: 1.5rem;
  border: 1px solid rgba(255,255,255,0.18);
}

.scroll-hint {
  margin-top: 4rem;
  display: flex; flex-direction: column; align-items: center; gap: 0.5rem;
  font-size: 0.85rem; font-weight: 500; opacity: 0.5;
}

@keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(8px); } }
.bounce { animation: bounce 1.5s ease infinite; }

/* ===== Section number ===== */
.section-num {
  font-size: 0.8rem; font-weight: 700;
  color: rgba(45,51,34,0.25);
  letter-spacing: 0.12em; margin-bottom: 0.5rem; display: block;
  font-variant-numeric: tabular-nums;
}

.section-num--light {
  color: rgba(255,255,255,0.35) !important;
}

.section-desc {
  font-size: 1.1rem; color: #3a4030;
  line-height: 1.7; margin-bottom: 2.5rem; max-width: 700px;
}

/* ===== Feature Grid ===== */
.feature-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}

.feature-item {
  background: linear-gradient(145deg, #ffffff, #f0f5e6);
  border: 1px solid rgba(45,51,34,0.06);
  border-radius: 14px; padding: 2rem 1.5rem;
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
  text-align: center; font-weight: 600; font-size: 0.95rem;
  color: #2d3322;
  box-shadow: 0 2px 8px rgba(45,51,34,0.04);
  opacity: 0; transform: translateY(30px) scale(0.95);
  transition: opacity 0.5s ease var(--d,0s), transform 0.5s ease var(--d,0s),
              box-shadow 0.3s, border-color 0.3s;
}

.slide-content.visible .feature-item {
  opacity: 1; transform: translateY(0) scale(1);
}

.feature-item:hover {
  box-shadow: 0 8px 24px rgba(45,51,34,0.08);
  transform: translateY(-3px) !important;
  border-color: rgba(45,51,34,0.12);
}

.feature-icon {
  width: 52px; height: 52px; border-radius: 14px;
  background: linear-gradient(135deg, #dae5c8, #c2d4a4);
  display: flex; align-items: center; justify-content: center;
  color: #3d4e2e;
  box-shadow: inset 0 1px 2px rgba(255,255,255,0.5), 0 1px 2px rgba(45,51,34,0.06);
}

/* ===== Persona Cards ===== */
.cards-row {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}

.persona-card {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px; padding: 2rem;
  position: relative; overflow: hidden;
  opacity: 0; transform: translateY(40px) scale(0.9);
  transition: opacity 0.5s ease var(--d,0s), transform 0.5s ease var(--d,0s),
              box-shadow 0.3s, border-color 0.3s;
}

.slide-content.visible .persona-card {
  opacity: 1; transform: translateY(0) scale(1);
}

.persona-card:hover {
  background: rgba(255,255,255,0.12);
  transform: translateY(-3px) !important;
  border-color: rgba(255,255,255,0.2);
}

.persona-accent {
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, rgba(255,255,255,0.3), rgba(255,255,255,0.1));
  border-radius: 14px 14px 0 0;
}

.persona-icon {
  width: 52px; height: 52px; border-radius: 14px;
  background: rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.25rem; color: #fff;
}

.persona-card h3 { font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
.persona-card p { font-size: 0.9rem; color: rgba(255,255,255,0.75); line-height: 1.6; }

/* ===== Steps ===== */
.steps { display: flex; flex-direction: column; gap: 1rem; }

.step {
  display: flex; gap: 1.5rem; align-items: flex-start;
  background: linear-gradient(145deg, #ffffff, #f0f5e6);
  border: 1px solid rgba(45,51,34,0.06); border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(45,51,34,0.03);
  opacity: 0; transform: translateX(-40px);
  transition: opacity 0.5s ease var(--d,0s), transform 0.5s ease var(--d,0s),
              box-shadow 0.3s, border-color 0.3s;
}

.slide-content.visible .step { opacity: 1; transform: translateX(0); }

.step:hover {
  box-shadow: 0 6px 20px rgba(45,51,34,0.07);
  transform: translateX(5px) !important;
  border-color: rgba(45,51,34,0.1);
}

.step-num {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, #4a5a3a, #2d3322);
  color: #fff; font-weight: 800; font-size: 1.1rem;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; box-shadow: 0 2px 6px rgba(45,51,34,0.15);
}

.step-content h3 { font-size: 1.1rem; font-weight: 700; color: #2d3322; margin-bottom: 0.25rem; }
.step-content p { font-size: 0.95rem; color: #4a4a4a; line-height: 1.5; }

/* ===== Usage Steps ===== */
.usage-steps { display: flex; flex-direction: column; align-items: center; gap: 1rem; }

.usage-step {
  display: flex; gap: 1rem; align-items: center;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px; padding: 1.25rem 1.5rem;
  width: 100%; max-width: 500px;
  opacity: 0; transform: scale(0.9) translateY(20px);
  transition: opacity 0.5s ease var(--d,0s), transform 0.5s ease var(--d,0s);
}

.slide-content.visible .usage-step { opacity: 1; transform: scale(1) translateY(0); }

.usage-step:hover {
  background: rgba(255,255,255,0.12);
  transform: scale(1.02) !important;
  border-color: rgba(255,255,255,0.2);
}

.usage-icon {
  width: 48px; height: 48px; border-radius: 12px;
  background: rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; color: #fff;
}

.usage-text strong { display: block; font-size: 1rem; color: #fff; margin-bottom: 0.15rem; }
.usage-text p { font-size: 0.9rem; color: rgba(255,255,255,0.75); line-height: 1.4; }

.usage-arrow {
  color: rgba(255,255,255,0.25);
  opacity: 0; transform: translateY(-10px);
  transition: opacity 0.4s ease var(--d,0s), transform 0.4s ease var(--d,0s);
}
.slide-content.visible .usage-arrow { opacity: 1; transform: translateY(0); }

/* ===== CTA ===== */
.cta-content {
  text-align: center;
  max-width: 600px;
}

.cta-content h2 {
  font-size: 2.5rem; font-weight: 800; color: #fff;
  margin-bottom: 1rem; text-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

.cta-content p {
  font-size: 1.1rem; color: rgba(255,255,255,0.8);
  line-height: 1.6; margin-bottom: 2.5rem;
}

.cta-btn {
  display: inline-flex; align-items: center; gap: 0.75rem;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(6px);
  color: #fff; font-size: 1.1rem; font-weight: 700;
  padding: 1rem 2rem; border-radius: 999px; text-decoration: none;
  border: 1px solid rgba(255,255,255,0.2);
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
}

.cta-btn:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* ===== Responsive ===== */
@media (max-width: 900px) {
  .slide {
    position: relative;
    height: auto;
    min-height: 100vh;
    padding: 3rem 0;
  }

  .slide-content {
    padding: 1rem 1.25rem;
    transform: none !important;
    opacity: 1 !important;
  }

  .slide h1 { font-size: 2rem; }
  .slide h2, .cta-content h2 { font-size: 1.5rem; margin-bottom: 0.75rem; }
  .slide-sub { font-size: 0.9rem; }

  .feature-grid, .cards-row { grid-template-columns: 1fr; gap: 0.75rem; }
  .step { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
  .usage-step { flex-direction: column; text-align: center; }
  .usage-arrow { transform: rotate(90deg) !important; }

  .feature-item { padding: 1rem 0.875rem; }
  .persona-card { padding: 1rem; }
  .step { padding: 1rem; }
  .usage-step { padding: 0.875rem 1rem; }

  .feature-item { opacity: 1 !important; transform: none !important; }
  .persona-card { opacity: 1 !important; transform: none !important; }
  .step { opacity: 1 !important; transform: none !important; }
  .usage-step { opacity: 1 !important; transform: none !important; }
  .usage-arrow { opacity: 1 !important; }

  .section-num { margin-bottom: 0.25rem; }
  .section-desc { margin-bottom: 1rem; }
  .scroll-hint { margin-top: 1.5rem; }

  .persona-icon { width: 40px; height: 40px; margin-bottom: 0.5rem; }
  .persona-icon :deep(svg) { width: 20px; height: 20px; }
  .feature-icon { width: 40px; height: 40px; }
  .feature-icon :deep(svg) { width: 18px; height: 18px; }
  .usage-icon { width: 36px; height: 36px; }
  .usage-icon :deep(svg) { width: 16px; height: 16px; }
}
</style>
