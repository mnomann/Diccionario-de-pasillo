<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="auth-overlay" @click.self="cerrar">
        <div class="auth-modal" role="dialog" aria-modal="true" :aria-label="tituloModal">
          <div class="auth-header">
            <h2 class="auth-title">{{ tituloModal }}</h2>
            <button class="auth-close" @click="cerrar" aria-label="Cerrar">
              <X :size="20" />
            </button>
          </div>

          <!-- === Autenticado: info de usuario === -->
          <template v-if="authStore.isAuthenticated">
            <div class="auth-user-info">
              <UserCircle :size="56" class="auth-avatar" />
              <p class="auth-user-name">{{ authStore.usuario?.nombre ?? 'Usuario' }}</p>
              <p class="auth-user-email">{{ authStore.usuario?.email ?? '' }}</p>
            </div>
            <button class="auth-btn auth-btn--logout" @click="handleLogout">
              <LogOut :size="18" />
              Cerrar Sesión
            </button>
          </template>

          <!-- === No autenticado: tabs + formularios === -->
          <template v-else>
            <div class="auth-tabs" role="tablist">
              <button
                :class="['auth-tab', { 'auth-tab--active': activeTab === 'login' }]"
                role="tab"
                :aria-selected="activeTab === 'login'"
                @click="switchTab('login')"
              >
                <LogIn :size="16" />
                Iniciar Sesión
              </button>
              <button
                :class="['auth-tab', { 'auth-tab--active': activeTab === 'register' }]"
                role="tab"
                :aria-selected="activeTab === 'register'"
                @click="switchTab('register')"
              >
                <UserPlus :size="16" />
                Registrarse
              </button>
            </div>

            <!-- Login -->
            <form v-if="activeTab === 'login'" class="auth-form" @submit.prevent="handleLogin">
              <div class="auth-field">
                <label for="login-email">Email</label>
                <div class="input-wrapper">
                  <Mail :size="16" class="input-icon" />
                  <input
                    id="login-email"
                    v-model="loginForm.email"
                    type="email"
                    placeholder="tu@email.com"
                    autocomplete="email"
                    required
                  />
                </div>
              </div>

              <div class="auth-field">
                <label for="login-password">Contraseña</label>
                <div class="input-wrapper">
                  <Lock :size="16" class="input-icon" />
                  <input
                    id="login-password"
                    v-model="loginForm.password"
                    :type="loginShowPassword ? 'text' : 'password'"
                    placeholder="••••••••"
                    autocomplete="current-password"
                    required
                  />
                  <button
                    type="button"
                    class="input-toggle"
                    :aria-label="loginShowPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    @click="loginShowPassword = !loginShowPassword"
                  >
                    <EyeOff v-if="loginShowPassword" :size="16" />
                    <Eye v-else :size="16" />
                  </button>
                </div>
              </div>

              <p v-if="authStore.error" class="auth-error">{{ authStore.error }}</p>
              <p v-if="regSuccessMessage" class="auth-success">{{ regSuccessMessage }}</p>

              <button type="submit" class="auth-btn auth-btn--primary" :disabled="authStore.loading">
                <Loader2 v-if="authStore.loading" :size="18" class="spinner" />
                <LogIn v-else :size="18" />
                {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
              </button>
            </form>

            <!-- Registro -->
            <form v-if="activeTab === 'register'" class="auth-form" @submit.prevent="handleRegister">
              <div class="auth-field">
                <label for="reg-name">Nombre</label>
                <div class="input-wrapper">
                  <UserCircle :size="16" class="input-icon" />
                  <input
                    id="reg-name"
                    v-model="regForm.name"
                    type="text"
                    placeholder="Tu nombre"
                    autocomplete="name"
                    required
                  />
                </div>
              </div>

              <div class="auth-field">
                <label for="reg-email">Email</label>
                <div class="input-wrapper">
                  <Mail :size="16" class="input-icon" />
                  <input
                    id="reg-email"
                    v-model="regForm.email"
                    type="email"
                    placeholder="tu@email.com"
                    autocomplete="email"
                    required
                  />
                </div>
              </div>

              <div class="auth-field">
                <label for="reg-password">Contraseña</label>
                <div class="input-wrapper">
                  <Lock :size="16" class="input-icon" />
                  <input
                    id="reg-password"
                    v-model="regForm.password"
                    :type="regShowPassword ? 'text' : 'password'"
                    placeholder="Mínimo 6 caracteres"
                    autocomplete="new-password"
                    required
                  />
                  <button
                    type="button"
                    class="input-toggle"
                    :aria-label="regShowPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    @click="regShowPassword = !regShowPassword"
                  >
                    <EyeOff v-if="regShowPassword" :size="16" />
                    <Eye v-else :size="16" />
                  </button>
                </div>
              </div>

              <div class="auth-field">
                <label for="reg-confirm">Confirmar Contraseña</label>
                <div class="input-wrapper">
                  <Lock :size="16" class="input-icon" />
                  <input
                    id="reg-confirm"
                    v-model="regForm.confirm"
                    :type="regShowPassword ? 'text' : 'password'"
                    placeholder="Repite la contraseña"
                    autocomplete="new-password"
                    required
                  />
                </div>
              </div>

              <p v-if="validationError" class="auth-error">{{ validationError }}</p>
              <p v-if="authStore.error && !validationError" class="auth-error">{{ authStore.error }}</p>

              <button type="submit" class="auth-btn auth-btn--primary" :disabled="authStore.loading">
                <Loader2 v-if="authStore.loading" :size="18" class="spinner" />
                <UserPlus v-else :size="18" />
                {{ authStore.loading ? 'Creando cuenta...' : 'Crear Cuenta' }}
              </button>
            </form>
          </template>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  UserCircle, LogIn, LogOut, UserPlus, X, Mail, Lock,
  Eye, EyeOff, Loader2,
} from 'lucide-vue-next'
import { useAuthStore } from '../../store/auth'

defineProps<{ isOpen: boolean }>()
const emit = defineEmits<{ close: [] }>()

const authStore = useAuthStore()

const activeTab = ref<'login' | 'register'>('login')
const loginShowPassword = ref(false)
const regShowPassword = ref(false)
const validationError = ref<string | null>(null)
const regSuccessMessage = ref<string | null>(null)

const loginForm = ref({ email: '', password: '' })
const regForm = ref({ name: '', email: '', password: '', confirm: '' })

const tituloModal = computed(() => {
  if (authStore.isAuthenticated) return 'Mi Cuenta'
  return activeTab.value === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta'
})

watch(
  () => authStore.isAuthenticated,
  (auth) => {
    if (auth) activeTab.value = 'login'
  },
)

watch(
  () => authStore.error,
  (err) => {
    if (err) validationError.value = null
  },
)

function cerrar() {
  authStore.error = null
  validationError.value = null
  regSuccessMessage.value = null
  emit('close')
}

function switchTab(tab: 'login' | 'register') {
  activeTab.value = tab
  authStore.error = null
  validationError.value = null
  regSuccessMessage.value = null
}

function resetForms() {
  loginForm.value = { email: '', password: '' }
  regForm.value = { name: '', email: '', password: '', confirm: '' }
  validationError.value = null
  regSuccessMessage.value = null
  authStore.error = null
  loginShowPassword.value = false
  regShowPassword.value = false
}

async function handleLogin() {
  if (!loginForm.value.email || !loginForm.value.password) return

  try {
    await authStore.login(loginForm.value.email, loginForm.value.password)
    await authStore.fetchPerfil()
    cerrar()
  } catch {
    /* error ya seteado en authStore.error */
  }
}

async function handleRegister() {
  validationError.value = null
  authStore.error = null

  if (!regForm.value.name || !regForm.value.email || !regForm.value.password || !regForm.value.confirm) {
    validationError.value = 'Todos los campos son obligatorios.'
    return
  }

  if (regForm.value.password.length < 6) {
    validationError.value = 'La contraseña debe tener al menos 6 caracteres.'
    return
  }

  if (regForm.value.password !== regForm.value.confirm) {
    validationError.value = 'Las contraseñas no coinciden.'
    return
  }

  try {
    await authStore.registro(regForm.value.name, regForm.value.email, regForm.value.password)
    regSuccessMessage.value = 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.'
    activeTab.value = 'login'
    loginForm.value.email = regForm.value.email
    regForm.value = { name: '', email: '', password: '', confirm: '' }
  } catch {
    /* error ya seteado en authStore.error */
  }
}

function handleLogout() {
  authStore.logout()
  cerrar()
}
</script>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== Overlay ===== */
.auth-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

/* ===== Modal ===== */
.auth-modal {
  background: #fff;
  border-radius: 16px;
  max-width: 420px;
  width: 100%;
  padding: 2rem;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

/* ===== Header ===== */
.auth-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.auth-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--brand-dark);
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.auth-close {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.35rem;
  border-radius: 6px;
  transition: background-color 0.15s, color 0.15s;
}

.auth-close:hover {
  background: rgba(0, 0, 0, 0.06);
  color: var(--brand-dark);
}

/* ===== Tabs ===== */
.auth-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color, #e2e5dc);
}

.auth-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: color 0.2s, border-color 0.2s;
}

.auth-tab:hover {
  color: var(--brand-dark);
}

.auth-tab--active {
  color: var(--brand-accent);
  border-bottom-color: var(--brand-accent);
}

/* ===== Formularios ===== */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.auth-field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.auth-field label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 0.9rem;
  color: var(--text-muted);
  pointer-events: none;
  flex-shrink: 0;
}

.input-wrapper input {
  width: 100%;
  padding: 0.7rem 0.9rem 0.7rem 2.6rem;
  border: 1px solid var(--border-color, #e2e5dc);
  border-radius: 8px;
  font-size: 0.9rem;
  color: var(--text-main);
  font-family: inherit;
  outline: none;
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-wrapper input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px rgba(74, 93, 53, 0.12);
}

.input-wrapper input::placeholder {
  color: #aaa;
}

.input-toggle {
  position: absolute;
  right: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 4px;
  transition: color 0.15s;
}

.input-toggle:hover {
  color: var(--brand-dark);
}

/* ===== Botones ===== */
.auth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background-color 0.2s, box-shadow 0.2s, opacity 0.2s, color 0.2s, border-color 0.2s;
}

.auth-btn--primary {
  background: var(--brand-accent);
  color: #fff;
}

.auth-btn--primary:hover:not(:disabled) {
  background: #3d4f30;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.auth-btn--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-btn--logout {
  width: 100%;
  background: transparent;
  border: 1px solid var(--border-color, #e2e5dc);
  color: var(--text-muted);
  margin-top: 0.5rem;
}

.auth-btn--logout:hover {
  border-color: #e74c3c;
  color: #e74c3c;
  background: rgba(231, 76, 60, 0.04);
}

/* ===== Estados: error / éxito ===== */
.auth-error {
  font-size: 0.85rem;
  color: #c62828;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  background: #fce4ec;
  border-radius: 6px;
  margin: 0;
}

.auth-success {
  font-size: 0.85rem;
  color: #065f46;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  background: #d1fae5;
  border-radius: 6px;
  margin: 0;
}

/* ===== Info de usuario (autenticado) ===== */
.auth-user-info {
  text-align: center;
  padding: 0.5rem 0 1rem;
}

.auth-avatar {
  color: var(--brand-accent);
  margin-bottom: 0.75rem;
}

.auth-user-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--brand-dark);
}

.auth-user-email {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

/* ===== Spinner ===== */
.spinner {
  animation: spin 0.7s linear infinite;
}

/* ===== Transiciones ===== */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-active .auth-modal,
.modal-fade-leave-active .auth-modal {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.modal-fade-enter-from {
  opacity: 0;
}

.modal-fade-enter-from .auth-modal {
  transform: scale(0.95);
  opacity: 0;
}

.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-leave-to .auth-modal {
  transform: scale(0.95);
  opacity: 0;
}

/* ===== Responsive ===== */
@media (max-width: 480px) {
  .auth-modal {
    padding: 1.5rem;
    border-radius: 12px;
  }

  .auth-tab {
    font-size: 0.8rem;
    padding: 0.6rem 0.5rem;
  }
}
</style>
