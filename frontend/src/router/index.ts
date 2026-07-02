import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import TraductorView from '../views/TraductorView.vue'
import DiccionarioView from '../views/DiccionarioView.vue'
import FrasesView from '../views/FrasesView.vue'
import EscenariosView from '../views/EscenariosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/traductor', name: 'traductor', component: TraductorView },
    { path: '/diccionario', name: 'diccionario', component: DiccionarioView },
    { path: '/frases', name: 'frases', component: FrasesView },
    { path: '/escenarios', name: 'escenarios', component: EscenariosView },
    { path: '/escenarios/:eid/frases/:fid', name: 'frase-chat', component: () => import('../views/FraseChatView.vue') },
    { path: '/reportar', name: 'reportar', component: () => import('../views/ReportFormView.vue') },
    { path: '/reportar/:entidadTipo/:entidadId?', name: 'reportar-entidad', component: () => import('../views/ReportFormView.vue') },
    { path: '/admin/reportes', name: 'admin-reportes', component: () => import('../views/AdminReportesView.vue') },
  ]
})

export default router