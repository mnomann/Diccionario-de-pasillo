<template>
  <div class="app-shell">
    <SideBar :is-open="sidebarOpen" @toggle="toggleSidebar" />

    <div v-if="sidebarOpen" class="sidebar-backdrop" @click="toggleSidebar" />

    <div class="main-container">
      <TopBar @toggle-sidebar="toggleSidebar" />

      <main class="content-view">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SideBar from './components/layout/SideBar.vue'
import TopBar from './components/layout/TopBar.vue'

const sidebarOpen = ref(false)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<style scoped>
.app-shell {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.content-view {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 768px) {
  .content-view {
    padding: 1.5rem;
  }

  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: 99;
  }
}
</style>
