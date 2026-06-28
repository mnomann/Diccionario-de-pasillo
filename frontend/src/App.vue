<template>
  <div class="app-shell" :class="{ 'app-shell--landing': esLanding }">
    <template v-if="!esLanding">
      <SideBar :is-open="sidebarOpen" @toggle="toggleSidebar" />
      <div v-if="sidebarOpen" class="sidebar-backdrop" @click="toggleSidebar" />
    </template>

    <div class="main-container" :class="{ 'main-container--landing': esLanding }">
      <TopBar v-if="!esLanding" @toggle-sidebar="toggleSidebar" />

      <main class="content-view" :class="{ 'content-view--landing': esLanding }">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import SideBar from './components/layout/SideBar.vue'
import TopBar from './components/layout/TopBar.vue'

const route = useRoute()
const sidebarOpen = ref(false)

const esLanding = computed(() => route.name === 'landing')

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

.app-shell--landing {
  overflow: hidden;
}

.main-container--landing {
  overflow: hidden;
}

.content-view--landing {
  padding: 0;
  overflow: hidden;
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
