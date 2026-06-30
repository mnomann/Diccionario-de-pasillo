<template>
  <header class="top-nav">
    <div class="top-left">
      <button class="hamburger" @click="$emit('toggle-sidebar')">
        <Menu :size="20" />
      </button>
      <router-link to="/" class="logo-text">Desenreda</router-link>
    </div>

    <div class="nav-actions">
      <button class="action-btn">
        <UserCircle :size="20" />
        CUENTA
      </button>
      <button class="action-btn">
        <Settings :size="20" />
        AJUSTES
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { UserCircle, Settings, Menu } from 'lucide-vue-next'

defineEmits<{ 'toggle-sidebar': [] }>()
</script>

<style scoped>
@keyframes topBarFadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.top-nav {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  background-color: #fff;
  border-bottom: 1px solid rgba(0,0,0,0.04);
  position: relative;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  animation: topBarFadeIn 0.4s ease both;
}

.top-nav::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--brand-accent), var(--brand-sidebar-deeper));
  opacity: 0.25;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.hamburger {
  display: none;
  background: none;
  border: none;
  color: var(--brand-dark);
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 6px;
  transition: background-color 0.15s;
}

.hamburger:hover {
  background: rgba(0,0,0,0.06);
}

.logo-text {
  color: var(--brand-dark);
  font-size: 1.25rem;
  font-family: serif;
  font-style: italic;
  border-bottom: 2px solid var(--brand-sidebar-deeper);
  padding-bottom: 2px;
  text-decoration: none;
  transition: opacity 0.2s;
  cursor: pointer;
}

.logo-text:hover {
  opacity: 0.7;
}

.nav-actions {
  display: flex;
  gap: 1.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: var(--brand-sidebar-deeper);
}

@media (max-width: 768px) {
  .top-nav {
    padding: 0 1rem;
  }

  .hamburger {
    display: flex;
  }
}
</style>
