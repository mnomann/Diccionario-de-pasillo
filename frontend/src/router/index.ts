import { createRouter, createWebHistory } from 'vue-router'
import TraductorView from '../views/TraductorView.vue'
import DiccionarioView from '../views/DiccionarioView.vue'
import FrasesView from '../views/FrasesView.vue'
import EscenariosView from '../views/EscenariosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'traductor', component: TraductorView },
    { path: '/diccionario', name: 'diccionario', component: DiccionarioView },
    { path: '/frases', name: 'frases', component: FrasesView },
    { path: '/escenarios', name: 'escenarios', component: EscenariosView },
  ]
})

export default router