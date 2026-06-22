<template>
  <aside class="sidebar" :class="{ 'sidebar--open': isOpen }">
    <button class="sidebar-close" @click="$emit('toggle')">
      <X :size="20" />
    </button>

    <div class="sidebar-header">
      <h1 class="logo-title">Desenreda</h1>
      <p class="logo-subtitle">Guía del español chileno</p>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="(item, i) in navItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :style="{ '--i': i }"
      >
        <component :is="item.icon" :size="20" />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { Languages, Book, Map, Sun, X } from 'lucide-vue-next'
import type { Component } from 'vue'

defineProps<{ isOpen: boolean }>()
defineEmits<{ toggle: [] }>()

interface NavItem {
  path: string
  label: string
  icon: Component
}

const navItems: NavItem[] = [
  { path: '/', label: 'Traductor', icon: Languages },
  { path: '/diccionario', label: 'Diccionario', icon: Book },
  { path: '/escenarios', label: 'Escenarios', icon: Map },
  { path: '/frases', label: 'Frases Frecuentes', icon: Sun },
]
</script>

<style scoped>
@keyframes navItemSlideIn {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}

.sidebar {
  width: 250px;
  height: 100%;
  background-color: var(--brand-sidebar);
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(0,0,0,0.05);
  position: relative;
  z-index: 100;
  transition: transform 0.3s ease;
}

.sidebar-close {
  display: none;
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: var(--brand-dark);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.15s;
}

.sidebar-close:hover {
  background: rgba(0,0,0,0.06);
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
  position: relative;
  overflow: hidden;
  transition: background-color 0.2s, transform 0.15s;
  animation: navItemSlideIn 0.35s ease both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}

.nav-item:hover {
  background-color: rgba(0,0,0,0.05);
  transform: translateX(3px);
}

.nav-item:active {
  transform: translateX(0);
}

.nav-item :deep(svg) {
  flex-shrink: 0;
}

/* Active indicator: left bar */
.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 3px;
  height: 60%;
  border-radius: 0 3px 3px 0;
  background: var(--brand-dark);
  transition: transform 0.2s ease;
}

.nav-item.router-link-active {
  background-color: #94cf82;
  font-weight: 700;
}

.nav-item.router-link-active::before {
  transform: translateY(-50%) scaleY(1);
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    transform: translateX(-100%);
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
  }

  .sidebar--open {
    transform: translateX(0);
  }

  .sidebar-close {
    display: block;
  }
}
</style>
