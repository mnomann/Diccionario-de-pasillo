import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../services/api'
import type { LoginResponse, UsuarioResponse, UsuarioMe } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const usuario = ref<UsuarioResponse | UsuarioMe | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, contrasena: string) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post<LoginResponse>('/auth/login', { email, contrasena })
      token.value = res.token
      usuario.value = res.usuario
      localStorage.setItem('auth_token', res.token)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al iniciar sesión'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function registro(nombre: string, email: string, contrasena: string) {
    loading.value = true
    error.value = null
    try {
      usuario.value = await api.post<UsuarioResponse>('/auth/registro', {
        nombre,
        email,
        contrasena,
      })
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error al registrarse'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchPerfil() {
    if (!token.value) return
    try {
      usuario.value = await api.get<UsuarioMe>('/usuarios/me')
    } catch {
      token.value = null
      usuario.value = null
      localStorage.removeItem('auth_token')
    }
  }

  function logout() {
    token.value = null
    usuario.value = null
    localStorage.removeItem('auth_token')
  }

  return {
    token,
    usuario,
    loading,
    error,
    isAuthenticated,
    login,
    registro,
    fetchPerfil,
    logout,
  }
})
