<template>
  <header class="top-nav">
    <div class="top-left">
      <button class="hamburger" @click="$emit('toggle-sidebar')">
        <Menu :size="20" />
      </button>
      <div class="logo-text">Desenreda</div>
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
  background-color: transparent;
  animation: topBarFadeIn 0.4s ease both;
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
  background: rgba(0,0,0,0.05);
}

.logo-text {
  color: var(--brand-dark);
  font-size: 1.25rem;
  font-family: serif;
  font-style: italic;
  border-bottom: 2px solid var(--brand-dark);
  padding-bottom: 2px;
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
  color: var(--brand-dark);
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
