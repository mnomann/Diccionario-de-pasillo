<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1 class="logo-title">Desenreda</h1>
      <p class="logo-subtitle">Guía del español chileno</p>
    </div>

    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item active">
        <Languages :size="20" />
        Traductor
      </router-link>

      <router-link to="/diccionario" class="nav-item">
        <Book :size="20" />
        Diccionario
      </router-link>

      <router-link to="/escenarios" class="nav-item">
        <Map :size="20" />
        Escenarios
      </router-link>
      
      <router-link to="/frases" class="nav-item">
        <Sun :size="20" />
        Frases Frecuentes
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { Languages, Book, Map, Sun } from 'lucide-vue-next'
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100%;
  background-color: var(--brand-sidebar); 
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(0,0,0,0.05);
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.logo-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--brand-dark);
}

.logo-subtitle {
  font-size: 0.875rem;
  color: var(--brand-dark);
  opacity: 0.8;
  margin-top: 0.25rem;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: var(--brand-dark);
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s;
}

.nav-item:hover {
  background-color: rgba(0,0,0,0.05);
}

.nav-item.active {
  background-color: #94cf82; 
}
</style>