<template>
  <div class="app-shell">
    <SideBar />

    <div class="main-container">
      <TopBar />
      
      <main class="content-view">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import SideBar from './components/layout/SideBar.vue'
import TopBar from './components/layout/TopBar.vue'
</script>

<style scoped>
.app-shell {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
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
</style>