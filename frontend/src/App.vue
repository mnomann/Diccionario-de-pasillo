<template>
  <div class="app-shell" :class="{ 'app-shell--landing': esLanding }">
    <transition name="sidebar">
      <SideBar v-if="!esLanding" :is-open="sidebarOpen" @toggle="toggleSidebar" />
    </transition>
    <transition name="backdrop">
      <div v-if="!esLanding && sidebarOpen" class="sidebar-backdrop" @click="toggleSidebar" />
    </transition>

    <div class="main-container" :class="{ 'main-container--landing': esLanding }">
      <transition name="topbar">
        <TopBar v-if="!esLanding" key="topbar" @toggle-sidebar="toggleSidebar" />
      </transition>

      <main class="content-view" :class="{ 'content-view--landing': esLanding }">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
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

.page-enter-active,
.page-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.page-enter-from {
  opacity: 0;
  transform: scale(0.97);
}

.page-leave-to {
  opacity: 0;
  transform: scale(1.03);
}

.topbar-enter-active,
.topbar-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.topbar-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}

.topbar-enter-from {
  opacity: 0;
  transform: translateY(-100%);
}

.sidebar-enter-active,
.sidebar-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.sidebar-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.sidebar-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}

.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.3s ease;
}

.backdrop-leave-to,
.backdrop-enter-from {
  opacity: 0;
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
