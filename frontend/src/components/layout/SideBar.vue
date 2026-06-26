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
  { path: '/traductor', label: 'Traductor', icon: Languages },
  { path: '/diccionario', label: 'Diccionario', icon: Book },
  { path: '/escenarios', label: 'Escenarios', icon: Map },
  { path: '/frases', label: 'Frases Frecuentes', icon: Sun },
]
</script>

<style scoped>
@keyframes navItemSlideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to   { opacity: 1; transform: translateX(0); }
}

.sidebar {
  width: 250px;
  height: 100%;
  background: linear-gradient(180deg, #4a5d35 0%, #5a6f42 100%);
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(0,0,0,0.12);
  position: relative;
  z-index: 100;
  transition: transform 0.3s ease;
  box-shadow: 2px 0 12px rgba(0,0,0,0.06);
}

.sidebar::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    90deg, transparent, transparent 2px,
    rgba(255,255,255,0.015) 2px, rgba(255,255,255,0.015) 4px
  );
  pointer-events: none;
}

.sidebar-close {
  display: none;
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: rgba(255,255,255,0.7);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.15s;
}

.sidebar-close:hover {
  background: rgba(255,255,255,0.1);
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: relative;
}

.logo-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
}

.logo-subtitle {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.6);
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
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  font-weight: 500;
  position: relative;
  overflow: hidden;
  transition: background-color 0.2s, transform 0.15s, color 0.2s;
  animation: navItemSlideIn 0.35s ease both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}

.nav-item:hover {
  background-color: rgba(255,255,255,0.08);
  transform: translateX(3px);
  color: #fff;
}

.nav-item:active {
  transform: translateX(0);
}

.nav-item :deep(svg) {
  flex-shrink: 0;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 3px;
  height: 60%;
  border-radius: 0 3px 3px 0;
  background: #a8c090;
  transition: transform 0.2s ease;
}

.nav-item.router-link-active {
  background-color: rgba(255,255,255,0.1);
  color: #fff;
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
    box-shadow: 4px 0 20px rgba(0,0,0,0.25);
  }

  .sidebar--open {
    transform: translateX(0);
  }

  .sidebar-close {
    display: block;
  }
}
</style>
