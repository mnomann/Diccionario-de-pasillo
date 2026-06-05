<template>
  <header class="top-nav">
    <div class="logo-area">
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
import { UserCircle, Settings } from 'lucide-vue-next'
</script>

<style scoped>
.top-nav {
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  background-color: transparent; 
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
</style>